class ThreeTapeTM:
    def __init__(self, dfa_transitions, dfa_initial_state, dfa_accept_states):
        self.transitions = dfa_transitions
        self.initial_state = dfa_initial_state
        self.accept_states = accept_states
        
        # Initialize the three tapes
        self.tape1 = []
        self.tape2 = self._encode_transitions()
        self.tape3 = [self.initial_state]
        
        # Head positions for each tape
        self.head1 = 0
        self.head2 = 0
        self.head3 = 0
    
    def _encode_transitions(self):
        encoded = []
        for state in self.transitions:
            for symbol in self.transitions[state]:
                encoded.append((state, symbol, self.transitions[state][symbol]))
        return encoded
    
    def step(self):
        if self.head1 >= len(self.tape1):
            return False
            
        current_state = self.tape3[self.head3]
        current_symbol = self.tape1[self.head1]
        
        # Search tape 2 for matching transition
        for i, (state, symbol, next_state) in enumerate(self.tape2):
            if state == current_state and symbol == current_symbol:
                # Update current state on tape 3
                self.tape3[self.head3] = next_state
                # Move input head right
                self.head1 += 1
                return True
                
        return False
    
    def run(self, input_string):
        self.tape1 = list(input_string)
        self.head1 = 0
        self.head3 = 0
        self.tape3[0] = self.initial_state
        
        while self.step():
            pass
            
        # Check if final state is accepting
        return self.tape3[self.head3] in self.accept_states

if __name__ == "__main__":
    dfa_transitions = {
        'q0': {'a': 'q1', 'b': 'q0'},
        'q1': {'a': 'q1', 'b': 'q2'},
        'q2': {'a': 'q1', 'b': 'q0'}
    }
    initial_state = 'q0'
    accept_states = {'q2'}
    
    tm = ThreeTapeTM(dfa_transitions, initial_state, accept_states)
    
    test_strings = ['ab', 'abb', 'aab', 'b']
    for s in test_strings:
        result = tm.run(s)
        print(f"String '{s}': {'Accepted' if result else 'Rejected'}")
