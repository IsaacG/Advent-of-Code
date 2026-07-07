"""
Logic Mill implementation.

This module provides a simple implementation of a Turing machine.

LICENSE: MIT
"""

RIGHT = "R"
LEFT = "L"
BLANK = "_"
COMMENT_PREFIX = "//"


TransitionType = tuple[str, str, str, str, str]


def parse_transition_rules(transition_rules_str: str) -> list[TransitionType]:
    """
    Parse a string into a list of transition rules.

    Args:
        transition_rules_str: A string containing transition rules, with each rule on a new line.
            Each rule should be space-separated values in the format:
            currentState currentSymbol newState newSymbol moveDirection

    Returns:
        A list of transition tuples, where each tuple contains:
        (currentState, currentSymbol, newState, newSymbol, moveDirection)

    """
    transitions_list = []
    for raw_line in transition_rules_str.split("\n"):
        line = raw_line.strip()
        if not line:
            continue

        # Skip whole-line comment
        if line.startswith(COMMENT_PREFIX):
            continue

        # Skip comment after the transition rule
        line = line.split(COMMENT_PREFIX, 1)[0].strip()

        values = []
        for raw_val in line.split(" "):
            val = raw_val.strip()
            if not val:
                continue
            values.append(val)

        transitions_list.append(tuple(values))
    return transitions_list


class InvalidTransitionError(Exception):
    """Exception raised when a transition is invalid (parsing)."""


class MissingTransitionError(Exception):
    """Exception raised when a transition is missing (parsing)."""


class InvalidSymbolError(Exception):
    """Exception raised when a symbol is invalid (parsing)."""


class LogicMill:
    """Logic Mill implementation."""

    def __init__(
        self,
        transitions_list: list[TransitionType],
        initial_state: str = "INIT",
        halt_state: str = "HALT",
        blank_symbol: str = BLANK,
    ) -> None:
        """Initialize the Logic Mill."""
        self.transitions = self._parse_transitions_list(
            transitions_list,
            initial_state,
            halt_state,
        )
        self.initial_state = initial_state
        self.halt_state = halt_state
        self.blank_symbol = blank_symbol

        self._set_tape("")

    def _validate_transition(self, transition: TransitionType) -> TransitionType:
        if len(transition) != 5:  # noqa: PLR2004
            msg = (
                f"Invalid transition: {transition}. "
                "Must be in the format (currentState, currentSymbol, newState, newSymbol, moveDirection)"
            )
            raise InvalidTransitionError(
                msg,
            )

        current_state, current_symbol, new_state, new_symbol, move_direction = transition

        if move_direction not in [LEFT, RIGHT]:
            msg = f"Invalid moveDirection: {move_direction}. Must be L or R"
            raise InvalidTransitionError(
                msg,
            )

        if len(current_symbol) != 1:
            msg = f"Invalid current symbol {current_symbol}. Must be a single character."
            raise InvalidSymbolError(
                msg,
            )

        if len(new_symbol) != 1:
            msg = f"Invalid new symbol {new_symbol}. Must be a single character."
            raise InvalidSymbolError(
                msg,
            )

        return current_state, current_symbol, new_state, new_symbol, move_direction

    def _parse_transitions_list(
        self,
        transitions_list: list[TransitionType],
        initial_state: str,
        halt_state: str,
    ) -> dict[str, dict[str, tuple[str, str, str]]]:
        transitions = {}
        has_halt_state = False
        for transition in transitions_list:
            current_state, current_symbol, new_state, new_symbol, move_direction = self._validate_transition(transition)

            if current_state not in transitions:
                transitions[current_state] = {}

            if current_symbol in transitions[current_state]:
                msg = f"Duplicate transition for state {current_state} and symbol {current_symbol}"
                raise InvalidTransitionError(
                    msg,
                )

            transitions[current_state][current_symbol] = (
                new_state,
                new_symbol,
                move_direction,
            )

            if new_state == halt_state:
                has_halt_state = True

        if initial_state not in transitions:
            msg = f"Initial state {initial_state} not found in the transitions"
            raise InvalidTransitionError(
                msg,
            )

        if not has_halt_state:
            msg = f"Halt state {halt_state} not found in the transitions"
            raise InvalidTransitionError(
                msg,
            )

        if len(transitions) > 2**16:
            msg = f"Too many states: {len(transitions)}. Maximum is 65536."
            raise InvalidTransitionError(
                msg,
            )

        return transitions

    def _set_tape(self, input_tape: str) -> None:
        if " " in input_tape:
            msg = "Input tape must not contain spaces"
            raise InvalidSymbolError(
                msg,
            )

        self.tape = {i: symbol for i, symbol in enumerate(input_tape) if symbol != self.blank_symbol}
        self.head_position = 0
        self.current_state = self.initial_state

    def _render_tape(self, *, strip_blank: bool = True) -> str:
        min_pos, max_pos = self._get_min_max_pos()
        tape_str = ""
        for i in range(min_pos, max_pos + 1):
            tape_str += self.tape.get(i, self.blank_symbol)

        if strip_blank:
            tape_str = tape_str.strip(self.blank_symbol)

        return tape_str

    def _get_min_max_pos(self, window: int = 10) -> tuple[int, int]:
        """Get the minimum and maximum positions of the tape."""
        min_pos = min(self.tape.keys()) if self.tape else self.head_position - window
        max_pos = max(self.tape.keys()) if self.tape else self.head_position + window

        min_pos = min(min_pos, self.head_position - window)
        max_pos = max(max_pos, self.head_position + window)

        return min_pos, max_pos

    def _print_tape(self) -> None:
        """Print the current state of the tape."""
        min_pos, _ = self._get_min_max_pos()

        head_pos_in_window = self.head_position - min_pos

        print(self._render_tape(strip_blank=False))
        print(" " * head_pos_in_window + "^")
        print(self.current_state)
        print()

    def _step(self) -> bool:
        """
        Perform a single step of the Logic Mill.

        Returns a boolean indicating whether the step was successful.
        """
        current_symbol = self.tape.get(self.head_position, self.blank_symbol)

        state_transitions = self.transitions.get(self.current_state)
        if not state_transitions:
            msg = f"No transitions for state {self.current_state}"
            raise MissingTransitionError(msg)

        transition = state_transitions.get(current_symbol)
        if not transition:
            msg = f"No transition for symbol {current_symbol or self.blank_symbol} in state {self.current_state}"
            raise MissingTransitionError(
                msg,
            )

        new_state, new_symbol, move_direction = transition

        if new_symbol == self.blank_symbol:
            if self.head_position in self.tape:
                del self.tape[self.head_position]
        else:
            self.tape[self.head_position] = new_symbol

        self.current_state = new_state

        if move_direction == LEFT:
            self.head_position -= 1
        elif move_direction == RIGHT:
            self.head_position += 1

        return True

    def run(
        self,
        input_tape: str,
        max_steps: int = 1_000_000,
        *,
        verbose: bool = False,
    ) -> tuple[str, int]:
        """
        Run the Logic Mill with the given input string.

        Returns a tuple containing the final tape content and the number of steps taken.
        """
        self._set_tape(input_tape)

        if verbose:
            self._print_tape()

        steps_count = 0
        while steps_count < max_steps:
            if self.current_state == self.halt_state:
                if verbose:
                    print(f"HALTED after {steps_count} steps")
                return (self._render_tape(), steps_count)

            self._step()
            steps_count += 1

            if verbose:
                self._print_tape()

        msg = f"Max steps reached: {max_steps}"
        raise RuntimeError(msg)

if __name__ == "__main__":
    transition_rules = parse_transition_rules(SOLUTIONS[-1])
    mill = LogicMill(transition_rules)
    result, steps = mill.run("11", verbose=True)
    print(f"Result: {result}")
    print(f"Steps: {steps}")
