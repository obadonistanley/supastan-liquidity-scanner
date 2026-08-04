from utils.trend import TrendFilter
from smc.liquidity import LiquiditySweep
from smc.market_structure import MarketStructure
from smc.order_blocks import OrderBlock


class Scanner:

    def __init__(self):

        self.trend = TrendFilter()
        self.liquidity = LiquiditySweep()
        self.market = MarketStructure()
        self.order_block = OrderBlock()



    def scan(self, candles):

        results = []


        trend = self.trend.detect(candles)

        liquidity_signal = self.liquidity.detect(candles)

        structure_signal = self.market.detect(candles)

        order_block_signal = self.order_block.detect(candles)



        if liquidity_signal:
            results.append(liquidity_signal)


        if structure_signal:
            results.append(structure_signal)


        if order_block_signal:
            results.append(order_block_signal)



        buy = results.count("BUY")

        sell = results.count("SELL")



        score = 0



        if trend == "BULLISH":
            score += 1


        elif trend == "BEARISH":
            score -= 1



        score += buy

        score -= sell



        # Calculate confidence

        confidence = abs(score) * 20


        if confidence > 100:
            confidence = 100



        # Final signal

        if score >= 3:

            signal = "BUY"

            reason = (
                "Bullish alignment: "
                "trend + SMC confirmations"
            )


        elif score <= -3:

            signal = "SELL"

            reason = (
                "Bearish alignment: "
                "trend + SMC confirmations"
            )


        else:

            signal = "NO TRADE"

            missing = []


            if not liquidity_signal:
                missing.append("Liquidity Sweep")


            if not structure_signal:
                missing.append("Market Structure")


            if not order_block_signal:
                missing.append("Order Block")


            if missing:

                reason = (
                    "Waiting for: "
                    + ", ".join(missing)
                )

            else:

                reason = "Confirmation not aligned"



        return {

            "signal": signal,

            "confidence": f"{confidence}%",

            "reason": reason,

            "trend": trend,

            "liquidity": liquidity_signal,

            "structure": structure_signal,

            "order_block": order_block_signal,

            "score": score

        }
