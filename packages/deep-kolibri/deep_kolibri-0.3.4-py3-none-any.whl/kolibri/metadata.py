import datetime
import os

from kolibri import utils
from kolibri import version as ver
from kolibri.config import component_config_from_pipeline
from kolibri.errors import *


class Metadata(object):
    """Captures all information about a model to load and prepare it."""

    @staticmethod
    def load(model_dir):
        """Loads the metadata from a models directory.

        Args:
            model_dir (str): the directory where the model is saved.
        Returns:
            Metadata: A metadata object describing the model
        """
        try:
            metadata_file = os.path.join(model_dir, 'metadata.json')
            data = utils.file.read_json_file(metadata_file)
            return Metadata(data, model_dir)
        except Exception as e:
            abspath = os.path.abspath(os.path.join(model_dir, 'metadata.json'))
            raise InvalidProjectError("Failed to load model metadata "
                                      "from '{}'. {}".format(abspath, e))

    def __init__(self, metadata, model_dir):

        self.metadata = metadata
        self.model_dir = model_dir

    def get(self, property_name, default=None):
        return self.metadata.get(property_name, default)

    @property
    def component_classes(self):
        if self.get('pipeline'):
            return [c.get("label") for c in self.get('pipeline', [])]
        else:
            return []

    def for_component(self, name, defaults=None):
        return component_config_from_pipeline(name,
                                              self.get('pipeline', []),
                                              defaults)

    @property
    def language(self):
        """Language of the underlying model"""

        return self.get('language')

    def persist(self, model_dir):
        """Persists the metadata of a model to a given directory."""

        metadata = self.metadata.copy()

        metadata.update({
            "trained_at": datetime.datetime.now().strftime('%Y%m%d-%H%M%S'),
            "kolibri_nlu_version": ver.__version__,
        })

        filename = os.path.join(model_dir, 'metadata.json')
        utils.write_json_to_file(filename, metadata, indent=4)
