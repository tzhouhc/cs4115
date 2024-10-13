import logging
from utils.token import Token, TokenType
from typing import Optional

logger = logging.getLogger(__name__)


class EOL(Exception):
    pass


class NoPaths(Exception):
    pass


class UnknownChar(Exception):
    pass


class SimpleAutomata:
    """
    A simple automata class that can be used to tokenize input strings based on
    a given table.

    Attributes:
    - table (dict[str, dict[str, str]): A dictionary representing the
      transition table of the automata.
    - current (str): The current state of the automata.
    - last (str): The last state of the automata.
    - matched (str): The string that has been matched so far.

    Methods:
    - paths() -> dict[str, str]: Returns the possible paths from the current
      state.
    - is_letter(char: str) -> bool: Static method to check if a character is a
      letter.
    - is_digit(char: str) -> bool: Static method to check if a character is a
      digit.
    - can_return() -> bool: Checks if the automata can return a token.
    - do_return() -> Optional[Token]: Returns a token if the automata is in an
      accepting state.
    - reset() -> None: Resets the automata to its initial state.
    - step(char: str) -> None: Takes a step in the automata based on the input
      character.

    Exceptions:
    - EOL: Raised when the end of the input string is reached.
    - UnknownChar: Raised when there are no paths to move from the start state
      with a given character.
    - NoPaths: Raised when there are no paths to move from the current state
      with a given character.
    """

    def __init__(self, table: dict[str, dict[str, str]]) -> None:
        """
        Initializes the SimpleAutomata with the given transition table.

        Args:
        - table (dict[str, dict[str, str]): A dictionary representing the
          transition table of the automata.
        """
        self.table = table
        self.current = "start"
        self.last = "start"
        self.matched = ""

    def paths(self) -> dict[str, str]:
        """
        Returns the possible paths from the current state.

        Returns:
        - dict[str, str]: A dictionary representing the possible paths from the
          current state.
        """
        return self.table[self.current]

    @staticmethod
    def is_letter(char: str) -> bool:
        """
        Static method to check if a character is a letter.

        Args:
        - char (str): The character to check.

        Returns:
        - bool: True if the character is a letter, False otherwise.
        """
        return (char >= "a" and char <= "z") or (char >= "A" and char <= "Z")

    @staticmethod
    def is_digit(char: str) -> bool:
        """
        Static method to check if a character is a digit.

        Args:
        - char (str): The character to check.

        Returns:
        - bool: True if the character is a digit, False otherwise.
        """
        return char >= "0" and char <= "9"

    def can_return(self) -> bool:
        """
        Checks if the automata can return a token.

        Returns:
        - bool: True if the automata can return a token, False otherwise.
        """
        return "DONE" in self.paths()

    def do_return(self) -> Optional[Token]:
        """
        Returns a token if the automata is in an accepting state.

        Returns:
        - Optional[Token]: A Token object if the automata is in an accepting
          state, None otherwise.
        """
        match = self.matched
        if "DONE" in self.paths():
            logger.debug(f"In an accepting state {self.current}, can return")
            res = Token(self.paths()["DONE"], match)
        elif match != "":
            logger.debug(
                f"In a non-accepting state {self.current}, cannot return")
            res = Token(TokenType.ERROR, match)
        else:
            # Nothing to handle, still need to reset, trivially return
            return None
        self.reset()
        return res

    def reset(self) -> None:
        """
        Resets the automata to its initial state.
        """
        self.matched = ""
        self.current = "start"
        self.last = "start"

    def step(self, char: str) -> None:
        """
        Takes a step in the automata based on the input character.

        Args:
        - char (str): The input character to process.

        Raises:
        - EOL: If the end of the input string is reached.
        - UnknownChar: If there are no paths to move from the start state with
          the given character.
        - NoPaths: If there are no paths to move from the current state with
          the given character.
        """
        self.last = self.current
        # EOL
        if not char:
            raise EOL("Reached EOL.")

        if char in self.paths():
            self.matched += char
            self.current = self.paths()[char]
            logger.info(f"Consumed '{char}' and moving to state "
                        f"'{self.current}'")
        elif "LETTER" in self.paths() and SimpleAutomata.is_letter(char):
            self.matched += char
            self.current = self.paths()["LETTER"]
            logger.info(f"Consumed '{char}' and moving to state "
                        f"'{self.current}'")
        elif "DIGIT" in self.paths() and SimpleAutomata.is_digit(char):
            self.matched += char
            self.current = self.paths()["DIGIT"]
            logger.info(f"Consumed '{char}' and moving to state "
                        f"'{self.current}'")
        elif "ANYTHING_BUT_QUOTE" in self.paths() and char != "\"":
            self.matched += char
            self.current = self.paths()["ANYTHING_BUT_QUOTE"]
            logger.info(f"Consumed '{char}' and moving to state "
                        f"'{self.current}'")
        elif "ANYTHING" in self.paths():
            self.matched += char
            self.current = self.paths()["ANYTHING"]
            logger.info(f"Consumed '{char}' and moving to state "
                        f"'{self.current}'")
        elif self.current == "start":
            self.matched += char
            raise UnknownChar(
                f"No paths to move from start with char {char}."
            )
        else:
            raise NoPaths(
                f"No paths to move for state {self.current} and char {char}")
