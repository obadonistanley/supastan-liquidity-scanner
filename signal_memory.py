import time


class SignalMemory:

    def __init__(self):

        self.memory = {}

        self.expiry = 4 * 60 * 60  # 4 hours


    def is_new(self, symbol, timeframe, signal):

        key = f"{symbol}_{timeframe}_{signal}"

        now = time.time()

        if key in self.memory:

            if now - self.memory[key] < self.expiry:

                return False

        self.memory[key] = now

        return True
