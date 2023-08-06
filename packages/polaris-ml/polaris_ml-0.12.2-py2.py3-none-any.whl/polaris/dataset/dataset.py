"""This module holds the PolarisDataset class
"""

import json

import pandas as pd

from polaris.common import constants
from polaris.common.json_serializable import JsonSerializable
from polaris.dataset.frame import PolarisFrame
from polaris.dataset.metadata import PolarisMetadata


class PolarisDataset(dict, JsonSerializable):
    """Class for dataset frames
    """
    def __init__(self, metadata=None, frames=None):
        """Initialize a PolarisDataset object

        :param metadata: dict of metadata
        :param frames: list of frames
        """
        dict.__init__(self)
        JsonSerializable.__init__(self)
        self.metadata = PolarisMetadata(metadata)
        if isinstance(frames, list):
            self.frames = [PolarisFrame(frame) for frame in frames]
        else:
            self.frames = [PolarisFrame(frames)]

    def __repr__(self):
        return {"metadata": self.metadata, "frames": self.frames}

    def __str__(self):
        return json.dumps(self.__repr__(), indent=constants.JSON_INDENT)

    def from_json(self, json_string):
        """Load a dataset object from a JSON string.

        This will initialize the object using the data loaded from
        JSON.

        :param json_string: a string of JSON to read from.

        """
        _obj = json.loads(json_string)
        self.__init__(metadata=_obj['metadata'], frames=_obj['frames'])

    def to_json(self):
        """Write a dataset object to JSON.
        """
        return json.dumps(self.__repr__(), indent=constants.JSON_INDENT)

    def to_pandas_dataframe(self):
        """Convert Polaris dataset to panda dataframe.
        """
        records = []
        for frame in self.frames:
            fields = {}
            for field in frame['fields']:
                fields[field] = frame['fields'][field]['value']

            if "time" not in fields:
                fields['time'] = pd.to_datetime(frame['time']).timestamp()

            records.append(fields)

        return pd.DataFrame(records)
