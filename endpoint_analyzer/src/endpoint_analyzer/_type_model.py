from collections import defaultdict
from .logging import get_logger
from ._type import Type


class TypeModel:
    """A nondeterministic finite automaton derived from type traces."""

    def __init__(self, type_traces):
        self.logger = get_logger(__name__)
        self.logger.info(f"Creating type model with {len(type_traces)} type traces...")
        self.type_traces = type_traces
        self.state_map = self._derive_state_map(type_traces)
        self.states = self.state_map.values()
        self.initial_state = 0
        self.transitions = self._derive_transitions(type_traces)
        self.symbols = self._derive_symbols(type_traces)
        self.final_states = self._derive_final_states(type_traces)
        self._minimize()

    def _minimize(self):
        """Remove unreachable states."""
        codomain = set()
        for _, transition in self.transitions.items():
            for _, destination in transition.items():
                codomain = codomain.union(destination)
        self.states = codomain.union(set([self.initial_state]))

    def predict(self, value_trace):
        """For a given value trace predict the corresponding type traces."""
        """ The traces are sorted from most generalized to least generalized """
        current_states = set([self.initial_state])
        for value in value_trace:
            exact_type, _ = Type.exact(value)
            deduced_type, _ = Type.deduce(value)
            new_current_states = set()
            for state in current_states:
                dest_states_exact = self.transitions[state][exact_type]
                dest_states_derived = self.transitions[state][deduced_type]
                dest_states = dest_states_exact.union(dest_states_derived)
                new_current_states = new_current_states.union(dest_states)
            current_states = new_current_states
        accepting_states = current_states.intersection(self.final_states)
        predictions = [self._type_trace_for(state) for state in accepting_states]
        # Sort type traces by number of generalized types
        predictions.sort(key=lambda p: sum(1 for s in p if Type.is_exact(s)))
        return predictions

    def accept(self, value_trace):
        """True if the automaton can determine a matching type_trace"""
        return len(self.predict(value_trace)) > 0

    def _type_trace_for(self, lookup_state):
        """Returns the matching type trace for given state"""
        for type_trace, state in self.state_map.items():
            if state == lookup_state:
                return type_trace

    def _derive_state_map(self, type_traces):
        """Create a state for each partial trace and return the mapping."""
        states = dict()
        states[()] = 0
        state = 1
        for type_trace in type_traces:
            for i in range(len(type_trace)):
                partial_trace = type_trace[: i + 1]
                if partial_trace not in states:
                    states[partial_trace] = state
                    state += 1
        return states

    def _derive_transitions(self, type_traces):
        """Create a transitions based on provided type traces"""
        """ Each transtion uses the type name as symbol to reach the next node """
        transitions = defaultdict(lambda: defaultdict(set))
        for type_trace in type_traces:
            for i in range(len(type_trace)):
                partial_trace = type_trace[:i]
                type_name = type_trace[i]
                source_state = self.state_map[partial_trace]
                destination_state = self.state_map[(*partial_trace, type_name)]
                transitions[source_state][type_name].add(destination_state)
        return transitions

    def _derive_symbols(self, type_traces):
        """Symbols match the type names of the provided type traces"""
        symbols = set()
        for type_trace in type_traces:
            for type_name in type_trace:
                symbols.add(type_name)
        return symbols

    def _derive_final_states(self, type_traces):
        """Final states correspond to the full length type traces"""
        final_states = set()
        for type_trace in type_traces:
            final_states.add(self.state_map[type_trace])
        return final_states
