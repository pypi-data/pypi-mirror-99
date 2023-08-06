"""
Polaris Graph class
"""

import json

import numpy as np

from polaris.common import constants
from polaris.common.json_serializable import JsonSerializable
from polaris.dataset.metadata import PolarisMetadata


class PolarisGraph(dict, JsonSerializable):
    """Class for Polaris Graphs
    """

    DEFAULT_GRAPH_LINK_THRESHOLD = 0.1

    # The original format looked like this:
    #
    # {"nodes": [ ...], "links": [ ... ]}
    #
    # This was to match what is needed by the ForceGraph3D library.
    # We'll designate that format as '0'.
    DATA_FORMAT_VERSION = 1

    def __init__(self, metadata=None, **kwargs):
        """Initialize a new object

        :param **kwargs: optional dictionary giving names for building the keys
        to the graph
        """
        dict.__init__(self)
        JsonSerializable.__init__(self)

        self._nodes_key = kwargs.get('nodes', "nodes")
        self._links_key = kwargs.get('links', "links")
        self._target_key = kwargs.get('target', "target")
        self._source_key = kwargs.get('source', "source")
        self._value_key = kwargs.get('value', "value")
        self.metadata = PolarisMetadata(metadata)
        self.graph = {
            'data_format_version': self.DATA_FORMAT_VERSION,
            self._nodes_key: [],
            self._links_key: []
        }

    def from_heatmap(self,
                     heatmap,
                     graph_link_threshold=DEFAULT_GRAPH_LINK_THRESHOLD):
        """Load from heatmap

        :param heatmap: The map to transform to graph
        :param graph_link_threshold: Only keeps links with value greater
        than this threshold.
        """
        if heatmap is None:
            return

        self._add_nodes(heatmap)
        self._add_links(heatmap, graph_link_threshold)

    def _add_links(self,
                   heatmap,
                   graph_link_threshold=DEFAULT_GRAPH_LINK_THRESHOLD):
        """Add links as appropriate
        """
        # Adding all edges to graph
        mdict = heatmap.to_dict("dict")
        for source in heatmap.to_dict("dict"):
            for target in mdict[source]:
                if target == source:
                    continue
                if (np.isnan(mdict[source][target])
                        or isinstance(mdict[source][target], str)):
                    continue
                if mdict[source][target] >= graph_link_threshold:
                    self.graph[self._links_key].append({
                        self._source_key:
                        source,
                        self._target_key:
                        target,
                        self._value_key:
                        mdict[source][target]
                    })

    def _add_nodes(self, heatmap):
        """Add nodes as appropriate
        """
        for col in heatmap.columns:
            self.graph[self._nodes_key].append({
                "id": col,
                "name": col,
                "group": 0
            })

    def __repr__(self):
        return {"metadata": self.metadata, "graph": self.graph}

    def __str__(self):
        return json.dumps(self.__repr__(), indent=constants.JSON_INDENT)

    def to_json(self):
        """Write a dataset object to JSON.
        """
        return json.dumps(self.__repr__(), indent=constants.JSON_INDENT)
