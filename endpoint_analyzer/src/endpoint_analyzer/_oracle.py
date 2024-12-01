from collections import defaultdict
from ._type_tree import TypeTree
from .logging import get_logger


class Oracle:
    """The oracle keeps a type tree and model for each trace depth."""

    """ It is used to predict type_traces from value_traces. """

    def __init__(self, value_traces, separator, root_repr):
        self.logger = get_logger(__name__)
        self.type_trees = defaultdict(lambda: TypeTree(separator, root_repr))
        self.type_models = dict()
        self.depth_heuristics = defaultdict(list)
        self.general_heuristics = []
        self.update(value_traces)

    def register_heuristic(self, heuristic):
        self.general_heuristics.append(heuristic)

    def register_depth_heuristic(self, depth, heuristic):
        self.depth_heuristics[depth].append(heuristic)

    def update(self, value_traces):
        """Update the oracle based on provided value traces"""
        self.logger.info(f"Updating oracle with {len(value_traces)} new value traces")
        self._update_type_trees(value_traces)
        self.type_models = dict()
        for depth, type_tree in self.type_trees.items():
            self.type_models[depth] = type_tree.type_model()

    def type_traces(self):
        """Returns all type traces captured by type trees of all depths"""
        traces = []
        for model in self.type_models.values():
            traces.extend(model.type_traces)
        return traces

    def _update_type_trees(self, value_traces):
        """Initializes the type trees based on the provided value traces"""
        for value_trace in value_traces:
            # Start with the root of the type tree for the correct depth
            type_tree = self.type_trees[len(value_trace)]
            for value in value_trace:
                # Insert each value at the current node within the type tree
                type_tree = type_tree.add_child(value)
        for depth, type_tree in self.type_trees.items():
            type_tree.update_types()
            # Apply registered heuristics
            for heuristic in self.depth_heuristics[depth]:
                type_tree.accept(heuristic)
            for heuristic in self.general_heuristics:
                type_tree.accept(heuristic)

    def predict(self, value_traces):
        """Predict sorted list of type traces for each value trace."""
        if isinstance(value_traces, str):
            value_trace = [value_traces]
            self.logger.warn(
                "Provided single value trace instead of iterable of value traces."
            )
        type_predictions = dict()
        for value_trace in value_traces:
            trace_depth = len(value_trace)
            type_predictions[value_trace] = None
            if trace_depth in self.type_models:
                predicted_endpoint = self.type_models[trace_depth].predict(value_trace)
                type_predictions[value_trace] = predicted_endpoint
        return type_predictions
