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

        if liquidity is None:

            return {

                "valid": False,

                "reason": "Liquidity Sweep missing"

            }

        if structure is None:

            return {

                "valid": False,

                "reason": "BOS / CHOCH missing"

            }

        if rectangle is None:

            return {

                "valid": False,

                "reason": "Fresh Order Block missing"

            }

        if rectangle["status"] != "FRESH":

            return {

                "valid": False,

                "reason": "Order Block already used"

            }

        if retest is None:

            return {

                "valid": False,

                "reason": "Waiting for first retest"

            }

        if liquidity != structure["signal"]:

            return {

                "valid": False,

                "reason": "Liquidity and Structure disagree"

            }

        if structure["signal"] != rectangle["signal"]:

            return {

                "valid": False,

                "reason": "Structure and Order Block disagree"

            }

        if rectangle["signal"] != retest["signal"]:

            return {

                "valid": False,

                "reason": "Retest direction mismatch"

            }

        return {

            "valid": True,

            "reason": "Complete SMC sequence confirmed"

        }
