import asyncio

from strategy import Strategy
from config import MARKETS
from signal_memory import SignalMemory
from signals_store import add_signal


strategy = Strategy()

memory = SignalMemory()


FOREX = [

    "GBPUSD",
    "GBPJPY",
    "EURJPY",
    "NZDJPY",
    "EURUSD",
    "USDCAD",
    "GBPNZD",
    "XAUUSD",
    "BTCUSD"

]


DERIV = [

    "R_10",
    "R_10_1S",
    "R_25",
    "R_25_1S",
    "R_50",
    "R_75",
    "R_75_1S",
    "R_100",
    "R_150_1S"

]


INDICES = [

    "US30",
    "NAS"

]


def get_timeframes(symbol):

    if symbol in FOREX:

        return [

            "D1",

            "H4",

            "H1"

        ]


    if symbol in DERIV:

        return [

            "H4",

            "H1",

            "M5"

        ]


    if symbol in INDICES:

        return [

            "H4",

            "H1"

        ]


    return [

        "H1"

    ]



async def auto_scan():

    while True:

        print("🔎 Supastan AI Auto Scan Running...")


        for symbol in MARKETS:

            for timeframe in get_timeframes(symbol):

                try:

                    result = strategy.run(

                        symbol,

                        timeframe

                    )


                    if result["signal"] in [

                        "BUY",

                        "SELL"

                    ]:

                        if memory.is_new(

                            result["symbol"],

                            result["timeframe"],

                            result["signal"]

                        ):

                            add_signal(result)

                            print(

                                "✅ NEW SIGNAL:",

                                result

                            )

                        else:

                            print(

                                "⏭ Duplicate skipped:",

                                result["symbol"],

                                result["timeframe"],

                                result["signal"]

                            )


                except Exception as e:

                    print(

                        "❌ Scan error:",

                        symbol,

                        timeframe,

                        e

                    )

        print("⏳ Waiting 60 seconds...")

        await asyncio.sleep(60)
