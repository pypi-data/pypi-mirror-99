"""
Autocompletion in the terminal.

Use the `input2` function with the `autocomplete` parameter instead of using this module
directly.

Author: Ian Fisher (iafisher@fastmail.com)
Version: October 2020
"""
import sys
import termios
import tty

UP = (91, 65)
DOWN = (91, 66)
RIGHT = (91, 67)
LEFT = (91, 68)
HOME = (91, 72)
END = (91, 70)
BACKSPACE = chr(127)
ESCAPE = chr(27)
CTRL_D = chr(4)
CTRL_L = chr(12)
ENTER = "\n"
TAB = "\t"


class Autocomplete:
    """
    Autocompletion in the terminal.

    Use it like this:

        with Autocomplete(sys.stdout, sys.stdin, completer) as ac:
            response = ac.input("? ")

    Autocompletion requires changing some terminal settings. The context manager will
    automatically restore the previous settings on exit.

    If you don't use the context manager, make sure you call `Autocomplete.close` before
    you try to write to or read from the terminal, and note that the terminal settings
    are changed as soon as Autocomplete is initialized.

    The only method that should be considered public on this class are `input` and
    `close`.
    """

    def __init__(self, stdout, stdin, completer, *, max_options=20, min_chars=1):
        self.stdout = stdout
        self.stdin = stdin
        self.completer = completer
        self.max_options = max_options
        self.min_chars = min_chars

        self.prompt = None
        self.cursor = 0
        self.chars = []
        self.suggestions = []
        # The index of the currently selected choice. If no choice is selected, then
        # `self.selected` is None.
        self.selected = None

        self.printer = Printer(stdout, stdin)

    def close(self):
        self.printer.close()

    def input(self, prompt):
        self.prompt = prompt
        self.chars.clear()
        self.printer.print_line(self.prompt)

        while True:
            # Each iteration of this loop is responsible for setting the following
            # fields:
            #
            #   self.cursor - the position of the cursor, as an index into `self.chars`
            #   self.chars - the characters to display after the prompt
            #   self.suggestions - the list of suggestions to display
            #   self.selected - the index of the suggestion to be highlighted, if any
            #
            # and calling `self.sync_display()` to update the terminal based on their
            # values.
            c = self.stdin.read(1)
            if c == ENTER:
                self.choose_selection()
                break

            force_suggestions = False
            if c == BACKSPACE:
                self.handle_backspace()
            elif c == ESCAPE:
                force_suggestions = self.handle_special_key()
            elif c == TAB:
                self.handle_tab()
            elif c == CTRL_D:
                raise EOFError
            elif c == CTRL_L:
                self.printer.clear_screen()
            else:
                self.handle_char(c)

            if self.selected is None:
                if len(self.chars) > self.min_chars or force_suggestions:
                    self.suggestions = self.get_suggestions("".join(self.chars))
                else:
                    self.suggestions.clear()

            self.sync_display()

        self.printer.clear_below_cursor()
        self.printer.cursor_down_and_start()
        return "".join(self.chars)

    def sync_display(self):
        """
        Synchronize the terminal display with the object's internal state.
        """
        if self.selected is None:
            chars = "".join(self.chars)
        else:
            chars = self.suggestions[self.selected]

        self.printer.print_line(self.prompt + chars)
        if self.selected is not None:
            self.printer.hide_cursor()
        else:
            self.printer.show_cursor()
            self.printer.set_cursor(len(self.prompt) + self.cursor)

        self.printer.print_lines_below_cursor(self.suggestions, highlight=self.selected)

    def handle_backspace(self):
        self.choose_selection()
        if self.chars and self.cursor > 0:
            self.chars.pop(self.cursor - 1)
            self.cursor -= 1

    def handle_tab(self):
        if self.selected is not None:
            self.choose_selection()
        else:
            suggestions = self.get_suggestions("".join(self.chars))
            if suggestions:
                self.chars = list(suggestions[0])
                self.cursor = len(self.chars)

    def handle_special_key(self):
        """
        Handles a special key (i.e., an escape sequence).

        The return value is a boolean indicating whether suggestions should be forced
        even if the user hasn't typed any characters yet.
        """
        c2, c3 = self.stdin.read(2)
        sequence = (ord(c2), ord(c3))
        if sequence == UP:
            self.select_up()
        elif sequence == DOWN:
            self.select_down()
            # If the user presses the Down key, force suggestions even if they haven't
            # entered any characters.
            return True
        elif sequence == RIGHT:
            if self.cursor < len(self.chars):
                self.cursor += 1

            return False
        elif sequence == LEFT:
            if self.cursor > 0:
                self.cursor -= 1

            return False
        elif sequence == HOME:
            self.cursor = 0
            return False
        elif sequence == END:
            self.cursor = len(self.chars)
            return False

        # By default, don't force suggestions.
        return False

    def handle_char(self, c):
        # If a character is typed while a suggestion is selected, that suggestion will
        # automatically be accepted.
        self.choose_selection()

        self.chars.insert(self.cursor, c)
        self.cursor += 1

    def choose_selection(self):
        if self.selected is not None:
            self.chars = list(self.suggestions[self.selected])
            self.cursor = len(self.chars)
            self.selected = None
            self.suggestions.clear()

    def select_up(self):
        if self.selected is None:
            return

        if self.selected == 0:
            self.selected = None
            return

        self.selected -= 1

    def select_down(self):
        if self.selected is not None and self.selected >= len(self.suggestions) - 1:
            return

        if not self.suggestions:
            return

        if self.selected is None:
            self.selected = 0
        else:
            self.selected += 1

    def get_suggestions(self, chars):
        options = self.completer(chars)

        if self.max_options is not None:
            return options[: self.max_options]
        else:
            return options

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.printer.clear_below_cursor()
        self.close()


def sequence_to_autocomplete(sequence, *, fuzzy=False):
    """
    Converts a sequence into an autocomplete function.

    By default, matching is at the front only, i.e. if I type 'Af' it will suggest
    'Afghanistan' but not 'Central African Republic'. To match anywhere in the input,
    set the `fuzzy` parameter to True.

    Matching is case-insensitive.
    """
    sequence = [x.lower() for x in sequence]

    def autocomplete(chars):
        chars = chars.lower()
        prefix_matches = []
        substring_matches = []
        for x in sequence:
            if x.startswith(chars):
                prefix_matches.append(x)
            elif fuzzy and chars in x:
                substring_matches.append(x)

        return prefix_matches + substring_matches

    return autocomplete


class Printer:
    """
    A class to handle low-level output control.
    """

    def __init__(self, stdout, stdin):
        self.stdout = stdout
        self.stdin = stdin
        self.cursor_pos = 0
        self.lines_below_cursor = 0

        # Initialize the terminal.
        fileno = self.stdout.fileno()
        # This check allows us to pass in a fake stdout instance for tests.
        if fileno is not None:
            self.old_settings = termios.tcgetattr(fileno)
            tty.setcbreak(fileno)

    def close(self):
        fileno = self.stdout.fileno()
        # This check allows us to pass in a fake stdout instance for tests.
        if fileno is not None:
            termios.tcsetattr(fileno, termios.TCSADRAIN, self.old_settings)

    def print_line(self, line):
        self.clear_line()
        self.return_to_start()
        self.stdout.write(line)
        self.stdout.flush()
        self.cursor_pos = len(line)

    def set_cursor(self, pos):
        self.return_to_start()
        self.cursor_right(pos)
        self.cursor_pos = pos

    def print_lines_below_cursor(self, lines, *, highlight=None):
        """
        Prints the lines below the cursor.

        The cursor is returned to its initial position.
        """
        # Make sure there's no output already below the cursor before printing more.
        self.clear_below_cursor()

        if not lines:
            return

        self.hide_cursor()
        # It's important to write newlines instead of using `cursor_down` here, because
        # `cursor_down` will have no effect if we are already at the bottom of the
        # window, whereas newlines will automatically scroll the window.
        self.stdout.write("\n")
        for i, choice in enumerate(lines):
            if i == highlight:
                self.stdout.write("\033[7m")
                self.stdout.write(choice + "\n")
                self.stdout.write("\033[0m")
            else:
                self.stdout.write(choice + "\n")

        self.lines_below_cursor = len(lines)

        self.cursor_up(len(lines) + 1)
        self.cursor_right(self.cursor_pos)
        self.show_cursor()

    def clear_below_cursor(self):
        """
        Clears all previous output below the cursor.

        The cursor is returned to its initial position.
        """
        if self.lines_below_cursor == 0:
            return

        self.hide_cursor()
        # We don't have to worry about using `cursor_down` like we do in
        # `print_lines_below_cursor` because we know that everything below the cursor
        # is within the window, so `cursor_down` will never fail.
        self.cursor_down()
        for _ in range(self.lines_below_cursor):
            self.clear_line()
            self.cursor_down()

        self.cursor_up(self.lines_below_cursor + 1)
        self.lines_below_cursor = 0
        self.show_cursor()

    def clear_line(self):
        self.csi("2K")

    def clear_screen(self):
        self.csi("2J")
        # Move the cursor to the top left corner.
        self.csi(";H")

    def return_to_start(self):
        self.csi("G")

    def cursor_down(self):
        self.csi("B")

    def cursor_left(self, n=1):
        self.csi(str(n) + "D")

    def cursor_right(self, n=1):
        self.csi(str(n) + "C")

    def cursor_up_and_start(self):
        self.csi("F")

    def cursor_down_and_start(self):
        self.csi("E")

    def cursor_up(self, n=1):
        self.csi(str(n) + "A")

    def hide_cursor(self):
        self.csi("?25l")

    def show_cursor(self):
        self.csi("?25h")

    def csi(self, code):
        self.stdout.write("\x1b[" + code)
        self.stdout.flush()


def d(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    sys.stderr.flush()
