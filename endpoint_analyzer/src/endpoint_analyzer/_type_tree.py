from collections import defaultdict
from .logging import get_logger
from ._type import Type
from ._type_model import TypeModel


class TypeTree:
    """Arranges values in a tree structure to deduces the node types and build a type model."""

    def __init__(self, separator, root_repr, *, value=None):
        self.logger = get_logger(__name__)
        self.separator = separator
        self.root_repr = root_repr
        self.value = value
        self.children = dict()
        self.parent = None
        self.type_name = None
        self.type_predicate = None

    def add_child(self, value):
        """Adds a new child node if the value does not already exist."""
        if value in self.children:
            return self.children[value]
        new_node = TypeTree(self.separator, self.root_repr, value=value)
        new_node.parent = self
        self.children[value] = new_node
        return new_node

    def update_types(self):
        """Deduces types for all child nodes without updating own type."""
        group = self._group_children_deduced()
        for type_name, children in group.items():
            for child, type_predicate in children:
                child.type_name = type_name
                child.type_predicate = type_predicate
                child.update_types()

    def accept(self, visitor):
        visitor.visit(self)

    def type_model(self):
        """Builds a type model based on node types by collecting traces from root to leaf."""
        type_traces = set()
        for trace in self._traces():
            # Each trace starts with the root node which doesn't have a type
            type_traces.add(tuple(trace[1:]))
        return TypeModel(type_traces)

    def optimize_types(self):
        if self.parent and len(self.parent.children) == 1:
            self.type_name, self.type_predicate = Type.deduce(self.value)
        for child in self.children:
            child.optimize_types()

    def _group_children_deduced(self):
        """Group children based on deduced types (instead of node type)"""
        group = defaultdict(set)
        for child in self.children.values():
            type_name, type_predicate = Type.deduce(child.value)
            group[type_name].add((child, type_predicate))
        return group

    def _traces(self):
        """Collect type traces from root node to all leaf nodes"""
        res = []
        if not self.children:
            return [[self.type_name]]
        for child in self.children.values():
            for child_res in child._traces():
                res.append([self.type_name] + child_res)
        return res

    def __str__(self, level=0):
        res = "  " * level
        res += repr(self)
        res += "\n"
        for child in self.children.values():
            res += child.__str__(level + 1)
        return res

    def __repr__(self):
        if not self.value and not self.parent:
            return self.root_repr
        return f"{str(self.value)}:{self.type_name}"

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.value == other.value

    def __hash__(self):
        return hash(self.value)
