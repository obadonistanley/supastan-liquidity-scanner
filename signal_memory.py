class SignalMemory:

    def __init__(self):
        self.alerted = {}

    def is_new(self, symbol, order_block_id):

        last = self.alerted.get(symbol)

        if last == order_block_id:
            return False

        self.alerted[symbol] = order_block_id
        return True
