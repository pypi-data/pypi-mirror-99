class printer:
    """Add effects to the printed output."""

    def __init__(self, text="white", style="no", background="black"):
        """Initialize values and assign corrispondent numbers."""
        textRe = {
            "black": 30,
            "red": 31,
            "green": 32,
            "yellow": 33,
            "blue": 34,
            "purple": 35,
            "cyan": 36,
            "white": 37
        }
        styleRe = {
            "no": 0,
            "bold": 1,
            "italic": 3,
            "negative": 5
        }
        backgroundRe = {
            "black": 40,
            "red": 41,
            "green": 42,
            "yellow": 43,
            "blue": 44,
            "purple": 45,
            "cyan": 46,
            "white": 47
        }
        try:
            self.text = textRe[text.lower()]
        except KeyError:
            self.text = 47
        try:
            self.style = styleRe[style.lower()]
        except KeyError:
            self.style = 0
        try:
            self.background = backgroundRe[background.lower()]
        except KeyError:
            self.background = 40

    def print(self, *contents):
        """Emphasize text."""
        for content in contents:
            print(
                f"\033[{self.style};{self.text};{self.background}m{content}\033[37;0;40m",
                end=" "
            )
        print()
