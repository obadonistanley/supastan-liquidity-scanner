import asyncio

from strategy import Strategy
from config import MARKETS
from signal_memory import SignalMemory


strategy = Strategy()

memory = SignalMemory()



async def auto_scan():

    while True:

        print("🔎 Supastan AI Auto Scan Running...")


        for symbol in MARKETS:


            for timeframe in [

                "D1",

                "H4",

                "H1",

                "M5"

            ]:


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


        print(

            "⏳ Waiting 60 seconds..."

        )


        await asyncio.sleep(60)
