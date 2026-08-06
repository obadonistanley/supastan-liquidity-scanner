signals = []


def add_signal(signal):
    global signals

    # Remove duplicate
    signals = [
        s for s in signals
        if not (
            s["symbol"] == signal["symbol"]
            and s["timeframe"] == signal["timeframe"]
            and s["signal"] == signal["signal"]
        )
    ]

    signals.insert(0, signal)

    # Keep latest 100 signals
    signals = signals[:100]


def get_signals():
    return signals
