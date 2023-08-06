def castVals(value, precision):
    """Cast every value"""
    try:
        value = float(value)
    except (ValueError, TypeError):
        value = 0.0
    try:
        precision = float(int)
    except (ValueError, TypeError):
        precision = 2
    return {
        "value": value,
        "precision": precision
    }


def usd(value, precision=2):
    """Format value as USD."""
    casted = castVals(value, precision)
    value = casted["value"]
    precision = casted["precision"]
    return f"${value:,.{precision}f}"


def eur(value, precision=2):
    """Format value as EUR"""
    tmp = usd(value, precision=precision)
    new = ""
    for char in tmp:
        if char == "$":
            new += "€"
        elif char == ",":
            new += "."
        elif char == ".":
            new += ","
        else:
            new += char
    return new


class locale:
    """Format numbers as values in a specified locale"""

    def __init__(self, value, precision=2):
        """Cast values"""
        casted = castVals(value, precision)
        self.value = casted["value"]
        self.precision = casted["precision"]

    def toUSD(self):
        """Format value as USD."""
        return usd(self.value, self.precision)

    def toEUR(self):
        """Format value as EUR"""
        return eur(self.value, self.precision)
