

import numpy as np

from kolibri.dnn import is_tf_available, is_torch_available
from kolibri import ModelConfig, ModelTrainer, ModelLoader
from kolibri.classical.tasks.classification.auto.models import models
from kolibri.data.text.corpus.file_stream import FileStream
from pathlib import Path

class TextClassifierPipeline():
    """
    Text classification pipeline

    """

    def __init__(self, name):

        self.model_name=name
        if name in models:
            self.model_data=models[name]
            self.trainer = None
        else:
            raise Exception('Model '+name+' was not found!')

    def __call__(self, data,  save_path, **kwargs):
        """
        Builds a model based on data.

        """

        if Path(data).suffix not in ['.csv', '.txt']:
            raise Exception('Bad File format. Only the following fromats are accepted: csv, tab, txt, json')

        self.model_data['configs']['output-folder'] = save_path
        if "language" in kwargs:
            self.model_data['configs']['language'] = kwargs['language']
        self.trainer=ModelTrainer(ModelConfig(self.model_data['configs']))
        #    confg['retrain-bigram'] = True
        min_class_count=0
        if 'content' in kwargs:
            x_col= kwargs['content']
        if 'targets' in kwargs:
            y_cols = kwargs['targets']
        if "min_class_count" in kwargs:
            min_class_count=kwargs['min_class_count']

        stream = FileStream(data, content_col=x_col,
                            target_cols=y_cols)

        stream.prepare(min_class_count=min_class_count)
        X, y = stream.get_data()

        self.trainer.fit(X, y)


        model_directory = self.trainer.persist(save_path, fixed_model_name="current")

        return model_directory



class TextClassifierModel():
    """
    Loads and used Text classification model

    """

    def __init__(self, name_or_path, full_response=False):

        self.model_name=name_or_path
        model_path=name_or_path
        self.model_interpreter = ModelLoader.load(model_path)
        self.full_response=full_response

    def __call__(self, text):
        """
        Builds a model based on data.

        """

        response=None
        if self.model_interpreter is not None:
            response=self.model_interpreter.process(text)
        else:
            raise Exception('Model not loaded')

        if response is not None:
            response=response['target_ranking']
        if not  self.full_response:
            response=response[0]

        return response


