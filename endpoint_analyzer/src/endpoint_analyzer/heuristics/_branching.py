from .._type import Type


class BranchingHeuristic:
    def __init__(self, *, num_branches=3):
        self.num_branches = num_branches

    def visit(self, type_node):
        group = type_node._group_children_deduced()
        for type_name, children in group.items():
            for child, _ in children:
                if (
                    len(type_node.children) <= self.num_branches
                    and not Type.is_resource(type_name)
                    and not Type.is_number(type_name)
                ):
                    child.type_name, child.type_predicate = Type.exact(child.value)
                child.accept(self)
