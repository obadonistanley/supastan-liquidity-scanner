signals = []


def add_signal(signal):

    global signals

    signals.insert(0, signal)

    # Keep only the latest 100 signals
    signals = signals[:100]


def get_signals():

    return signals
