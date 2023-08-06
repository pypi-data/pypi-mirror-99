import os

import joblib
import numpy as np
from scipy.sparse import vstack

from kolibri import settings
from kolibri.classical.tasks.classification.models import get_model, get_online_model
from kolibri.data.samplers import get_sampler
from kolibri.evaluation.evaluator import ClassifierEvaluator
from kolibri.kolibri_component import Component
from kolibri.logger import get_logger

logger = get_logger(__name__)

KOLIBRI_MODEL_FILE_NAME = "classifier_kolibri.pkl"


def _sklearn_numpy_warning_fix():
    """Fixes unecessary warnings emitted by sklearns use of numpy.

    Sklearn will fix the warnings in their next release in ~ August 2018.

    based on https://stackoverflow.com/questions/49545947/sklearn-deprecationwarning-truth-text-of-an-array"""
    import warnings

    warnings.filterwarnings(module='sklearn*', action='ignore',
                            category=DeprecationWarning)


class Estimator(Component):
    """classifier using the sklearn framework"""

    _estimator_type = 'estimator'

    provides = ["classification", "target_ranking"]

    requires = ["text_features"]

    defaults = {

        # the models used in the classifier if several models are given they will be combined
        "models": "logreg",
        "base-estimator": None,
        "explain": False,
        "sampler": None,
        "priors-thresolding": False,
        'voting_type': 'soft',
        'weights': None,
        'evaluate-performance': False
    }

    def __init__(self, component_config=None, classifier=None, indexer=None):
        from kolibri.indexers import LabelIndexer
        """Construct a new class classifier using the sklearn framework."""
        super().__init__(component_config=component_config)

        if indexer is not None:
            self.indexer = indexer
        else:
            self.indexer = LabelIndexer(multi_label=False)

        _sklearn_numpy_warning_fix()
        if classifier:
            clf = get_model(classifier)
            if not clf:
                clf = get_online_model(classifier)
            if clf:
                self.clf = clf
            else:
                raise Exception('Cannot find classifier ' + classifier)

        elif 'models' in self.component_config:
            self.clf = get_model(self.component_config['models'], weights=self.component_config['weights'],
                                 voting_type=self.component_config['voting_type'])

        if not self.clf:
            raise Exception(
                'The classification model: "' + str(self.component_config['models']) + '" could not be created.')

        if hasattr(self.clf, 'base_estimator') and self.component_config['base-estimator'] is not None:
            self.clf.base_estimator = get_model(self.component_config['base-estimator'])

        self.sampler = None

        if self.component_config['sampler']:
            self.sampler = get_sampler(self.component_config['sampler'])

        self.class_priors = None
        self.performace_scores = "Not computed"

    @classmethod
    def required_packages(cls):
        return ["sklearn"]

    def evaluate(self, X_val=None, y_val=None):

        if X_val is not None and y_val is not None:
            pred = self.predict(X_val)

            self.performace_scores = ClassifierEvaluator().get_performance_report(y_true=y_val, y_pred=pred)

    def compute_priors(self, y):
        unique, counts = np.unique(y, return_counts=True)
        self.class_priors = dict(zip(unique, counts))

        total = sum(self.class_priors.values(), 0.0)
        self.class_priors = {k: v / total for k, v in self.class_priors.items()}

    def transform(self, document):

        return self.clf.transform(document, )

    def predict_prob(self, X):
        """Given a bow vector of an input text, predict the class label.

        Return probabilities for all y_values.

        :param X: bow of input text
        :return: vector of probabilities containing one entry for each label"""

        pred_result = self.clf.predict_proba(X)
        # sort the probabilities retrieving the indices of
        # the elements in sorted order
        sorted_indices = np.fliplr(np.argsort(pred_result, axis=1))

        return pred_result, sorted_indices, pred_result[:, sorted_indices]

    def fit(self, X, y, X_val=None, y_val=None):
        if self.component_config['evaluate-performance']:
            self.performace_scores = ClassifierEvaluator(estimator=self.clf, X=X, y=y, labels=list(
                self.indexer.vocab2idx.keys())).get_performance_report()
        return self

    def predict(self, X):
        """Given a bow vector of an input text, predict most probable label.

        Return only the most likely label.

        :param X: bow of input text
        :return: tuple of first, the most probable label and second,
                 its probability."""

        if self.component_config["priors-thresolding"]:
            predictions = None
            try:
                predictions = self.clf.predict_proba(X)
            except Exception as e:
                pass
            if not predictions is None:
                try:
                    priors = np.array([v for v in self.class_priors.values()])
                    predictions = (predictions.T - priors[:, None]) / priors[:, None]
                    predictions = np.argmax(predictions.T, axis=1)
                except Exception as e:
                    print(e)
            else:
                predictions = self.clf.predict(X)
            return self.indexer.inverse_transform(predictions)

        return self.indexer.inverse_transform(self.clf.predict(X))

    def train(self, training_data, **kwargs):

        y = self.indexer.inverse_transform([document.label for document in training_data])
        X = vstack([document.vector for document in training_data])
        self.fit(X, y)

    def process(self, document, **kwargs):
        """Return the most likely class and its probability for a document."""

        if not self.clf:
            # component is either not trained or didn't
            # receive enough training texts
            target = None
            target_ranking = []
        else:
            X = document.vector
            raw_results, class_ids, probabilities = self.predict_prob(X)
            classes = self.indexer.inverse_transform(np.ravel(class_ids))
            # `predict` returns a matrix as it is supposed
            # to work for multiple examples as well, hence we need to flatten
            classes, probabilities = classes, probabilities.flatten()

            if len(classes) > 0 and probabilities.size > 0:
                ranking = list(zip(list(classes),
                                   list(probabilities)))[:settings.modeling['TARGET_RANKING_LENGTH']]

                target = {"name": classes[0], "confidence": probabilities[0]}

                target_ranking = [{"name": class_name, "confidence": score}
                                  for class_name, score in ranking]
            else:
                target = {"name": None, "confidence": 0.0}
                target_ranking = []
        #            self.clf.classes_ = self.indexer.la

        document.label = target
        document.raw_prediction_results = raw_results
        document.set_output_property("raw_prediction_results")
        document.set_output_property("label")
        document.target_ranking = target_ranking
        document.set_output_property("target_ranking")

    @classmethod
    def load(cls, model_dir=None, model_metadata=None, cached_component=None, **kwargs):

        meta = model_metadata.for_component(cls.name)
        file_name = meta.get("classifier_file", KOLIBRI_MODEL_FILE_NAME)
        classifier_file = os.path.join(model_dir, file_name)

        if os.path.exists(classifier_file):
            model = joblib.load(classifier_file)
            return model
        else:
            return cls(meta)

    def persist(self, model_dir):
        """Persist this model into the passed directory."""

        classifier_file = os.path.join(model_dir, KOLIBRI_MODEL_FILE_NAME)
        joblib.dump(self, classifier_file)

        return {
            "classifier_file": KOLIBRI_MODEL_FILE_NAME,
            "performace_scores": self.performace_scores,
        }
