import asyncio

from strategy import Strategy
from config import MARKETS


strategy = Strategy()



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


                        print(

                            "SIGNAL FOUND:",

                            result

                        )


                except Exception as e:


                    print(

                        "Scan error:",

                        symbol,

                        timeframe,

                        e

                    )



        print(
            "Waiting 60 seconds..."
        )


        await asyncio.sleep(60)
