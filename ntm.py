from collections import deque
from typing import Dict, Set, List, Tuple, Any
from dataclasses import dataclass

@dataclass
class TMConfiguration:
    state: str
    tape1: List[str]
    tape2: List[Tuple]
    tape3: List[str]
    head1: int
    head2: int
    head3: int

class MultiTapeNTM:
    def __init__(self, transitions: Dict[str, Dict[str, Set[str]]], 
                 initial_state: str, 
                 accept_states: Set[str]):
        self.transitions = transitions
        self.initial_state = initial_state
        self.accept_states = accept_states
        self.max_steps = 1000  # Prevent infinite loops
        
    def _encode_transitions(self) -> List[Tuple[str, str, str]]:
        encoded = []
        for state in self.transitions:
            for symbol in self.transitions[state]:
                for next_state in self.transitions[state][symbol]:
                    encoded.append((state, symbol, next_state))
        return encoded
    
    def _get_next_configurations(self, config: TMConfiguration) -> List[TMConfiguration]:
        if config.head1 >= len(config.tape1):
            return []
            
        current_state = config.tape3[config.head3]
        current_symbol = config.tape1[config.head1]
        
        next_configs = []
        
        # Find all matching transitions
        for next_state in self.transitions.get(current_state, {}).get(current_symbol, set()):
            # Create new configuration for each possible transition
            new_tape3 = config.tape3.copy()
            new_tape3.append(next_state)
            
            next_configs.append(TMConfiguration(
                state=next_state,
                tape1=config.tape1,
                tape2=config.tape2,
                tape3=new_tape3,
                head1=config.head1 + 1,
                head2=config.head2,
                head3=config.head3 + 1
            ))
            
        return next_configs
    
    def accepts(self, input_string: str) -> bool:
        # Initialize the first configuration
        initial_config = TMConfiguration(
            state=self.initial_state,
            tape1=list(input_string),
            tape2=self._encode_transitions(),
            tape3=[self.initial_state],
            head1=0,
            head2=0,
            head3=0
        )
        
        # Use BFS to explore all possible computation paths
        queue = deque([initial_config])
        steps = 0
        
        while queue and steps < self.max_steps:
            steps += 1
            current_config = queue.popleft()
            
            # Check if this configuration is accepting
            if (current_config.head1 >= len(current_config.tape1) and 
                current_config.state in self.accept_states):
                return True
            
            # Add all possible next configurations to the queue
            queue.extend(self._get_next_configurations(current_config))
        
        return False

if __name__ == "__main__":
    ntm_transitions = {
        'q0': {
            'a': {'q1', 'q0'},
            'b': {'q0'},
            'c': {'q0'}
        },
        'q1': {
            'a': {'q1'},
            'b': {'q2', 'q1'},
            'c': {'q1'}
        },
        'q2': {
            'a': {'q2'},
            'b': {'q2'},
            'c': {'q2'}
        }
    }
    
    initial_state = 'q0'
    accept_states = {'q2'}
    
    ntm = MultiTapeNTM(ntm_transitions, initial_state, accept_states)
    
    test_strings = [
        'ab',       # Should accept
        'acb',      # Should accept
        'cccacccb', # Should accept
        'b',        # Should reject
        'a',        # Should reject
        'ba',       # Should reject
    ]
    
    for s in test_strings:
        result = ntm.accepts(s)
        print(f"String '{s}': {'Accepted' if result else 'Rejected'}")
