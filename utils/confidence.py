class Confidence:

    def calculate(

        self,

        trend,

        liquidity,

        structure,

        rectangle,

        retest

    ):

        score = 0

        reasons = []

        # Trend
        if trend in ["BULLISH", "BEARISH"]:
            score += 20
            reasons.append("Trend")

        # Liquidity Sweep
        if liquidity:
            score += 20
            reasons.append("Liquidity Sweep")

        # BOS / CHOCH
        if structure:
            score += 20
            reasons.append("Market Structure")

        # Fresh Order Block
        if rectangle and rectangle["status"] == "FRESH":
            score += 20
            reasons.append("Fresh Order Block")

        # First Retest
        if retest:
            score += 20
            reasons.append("First Retest")

        if score >= 80:
            quality = "A+"

        elif score >= 60:
            quality = "A"

        elif score >= 40:
            quality = "B"

        else:
            quality = "C"

        return {

            "score": score,

            "confidence": f"{score}%",

            "quality": quality,

            "confirmed": reasons

        }
