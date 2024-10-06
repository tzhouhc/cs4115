import logging
from utils.token import Token, TokenType

logger = logging.getLogger(__name__)


class SimpleAutomata:
    """
    A simple automata class that can be used to tokenize input strings based
    on a given table of transitions.

    Attributes:
    - table (dict[str, dict[str, str]): A dictionary representing the
      transition table for the automata.
    - current (str): The current state of the automata.
    - last (str): The last state of the automata.
    - matched (str): The string that has been matched so far.

    Methods:
    - paths() -> dict[str, str]: Returns the possible transitions from the
      current state.
    - is_letter(char: str) -> bool: Static method to check if a character is a
      letter.
    - is_digit(char: str) -> bool: Static method to check if a character is a
      digit.
    - can_return() -> bool: Checks if the automata can return a token.
    - do_return() -> Token: Returns a token based on the current state.
    - reset() -> None: Resets the automata to its initial state.
    - step(char: str) -> None: Takes a step in the automata based on the input
      character.

    """

    def __init__(self, table: dict[str, dict[str, str]]) -> None:
        """
        Initialize the SimpleAutomata with the given transition table.

        Args:
        - table (dict[str, dict[str, str]): A dictionary representing the
          transition table for the automata.

        Returns:
        - None
        """
        self.table = table
        self.current = "start"
        self.last = "start"
        self.matched = ""

    def paths(self) -> dict[str, str]:
        """
        Returns the possible transitions from the current state.

        Returns:
        - dict[str, str]: A dictionary representing the possible transitions
          from the current state.
        """
        return self.table[self.current]

    @staticmethod
    def is_letter(char: str) -> bool:
        """
        Check if a character is a letter.

        Args:
        - char (str): The character to check.

        Returns:
        - bool: True if the character is a letter, False otherwise.
        """
        return (char >= "a" and char <= "z") or (char >= "A" and char <= "Z")

    @staticmethod
    def is_digit(char: str) -> bool:
        """
        Check if a character is a digit.

        Args:
        - char (str): The character to check.

        Returns:
        - bool: True if the character is a digit, False otherwise.
        """
        return char >= "0" and char <= "9"

    def can_return(self) -> bool:
        """
        Check if the automata can return a token.

        Returns:
        - bool: True if the automata can return a token, False otherwise.
        """
        return "DONE" in self.paths()

    def do_return(self) -> Token:
        """
        Return a token based on the current state.

        Returns:
        - Token: A token object based on the current state.
        """
        match = self.matched
        res = Token(self.paths()["DONE"], match)
        self.reset()
        return res

    def do_error(self) -> Token:
        """
        Return an error token based on the current state.

        Returns:
        - Token: A token object wrapping around an error.
        """
        match = self.matched
        res = Token(TokenType.ERROR, match)
        self.reset()
        return res

    def reset(self) -> None:
        """
        Reset the automata to its initial state.

        Returns:
        - None
        """
        self.matched = ""
        self.current = "start"
        self.last = "start"

    def step(self, char: str) -> None:
        """
        Take a step in the automata based on the input character.

        Args:
        - char (str): The input character to process.

        Returns:
        - None

        Raises:
        - ValueError: If there are no paths to move for the current state and
          input character.
        """
        self.last = self.current
        if char in self.paths():
            self.matched += char
            self.current = self.paths()[char]
            logger.info(f"Consumed '{char}' and moving to state "
                        "'{self.current}'")
        elif "LETTER" in self.paths() and SimpleAutomata.is_letter(char):
            self.matched += char
            self.current = self.paths()["LETTER"]
            logger.info(f"Consumed '{char}' and moving to state "
                        "'{self.current}'")
        elif "DIGIT" in self.paths() and SimpleAutomata.is_digit(char):
            self.matched += char
            self.current = self.paths()["DIGIT"]
            logger.info(f"Consumed '{char}' and moving to state "
                        "'{self.current}'")
        else:
            raise ValueError(
                f"No paths to move for state {self.current} and char {char}")
