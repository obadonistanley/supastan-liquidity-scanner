def get_timeframes(symbol):

    if symbol in FOREX:
        return ["D1", "H4", "H1"]

    if symbol in DERIV:
        return ["H4", "H1", "M5"]

    if symbol in INDICES:
        return ["H4", "H1"]

    return ["H1"]
