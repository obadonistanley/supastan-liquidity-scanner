class SequenceValidator:

    def __init__(self):
        pass

    def validate(

        self,

        liquidity,

        structure,

        rectangle,

        retest

    ):

        # ==========================
        # STEP 1
        # Liquidity Sweep
        # ==========================

        if liquidity is None:

            return {

                "valid": False,

                "signal": "NO TRADE",

                "reason": "Liquidity Sweep missing"

            }

        # ==========================
        # STEP 2
        # BOS / CHOCH
        # ==========================

        if structure is None:

            return {

                "valid": False,

                "signal": "NO TRADE",

                "reason": "BOS / CHOCH missing"

            }

        # ==========================
        # STEP 3
        # Fresh Order Block
        # ==========================

        if rectangle is None:

            return {

                "valid": False,

                "signal": "NO TRADE",

                "reason": "Fresh Order Block missing"

            }

        if rectangle["status"] != "FRESH":

            return {

                "valid": False,

                "signal": "NO TRADE",

                "reason": "Order Block already mitigated"

            }

        # ==========================
        # STEP 4
        # First Retest
        # ==========================

        if retest is None:

            return {

                "valid": False,

                "signal": "NO TRADE",

                "reason": "Waiting for First Retest"

            }

        # ==========================
        # STEP 5
        # Direction Agreement
        # ==========================

        direction = structure["signal"]

        if liquidity != direction:

            return {

                "valid": False,

                "signal": "NO TRADE",

                "reason": "Liquidity direction mismatch"

            }

        if rectangle["signal"] != direction:

            return {

                "valid": False,

                "signal": "NO TRADE",

                "reason": "Order Block direction mismatch"

            }

        if retest["signal"] != direction:

            return {

                "valid": False,

                "signal": "NO TRADE",

                "reason": "Retest direction mismatch"

            }

        # ==========================
        # COMPLETE SEQUENCE
        # ==========================

        return {

            "valid": True,

            "signal": direction,

            "reason": "Liquidity Sweep → BOS → CHOCH → Fresh Order Block → First Retest"

        }
