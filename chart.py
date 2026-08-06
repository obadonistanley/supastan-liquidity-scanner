
import mplfinance as mpf
import pandas as pd


def create_chart(candles, signal_data):

    symbol = signal_data.get("symbol", "MARKET")
    timeframe = signal_data.get("timeframe", "")

    filename = "signal_chart.png"

    df = pd.DataFrame(candles)

    df["time"] = pd.to_datetime(df["time"], unit="s")

    df.set_index("time", inplace=True)

    df = df.rename(
        columns={
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close"
        }
    )


    liquidity = signal_data.get("liquidity", {})

    level = liquidity.get("level")


    addplots = []


    if level:

        sweep_line = pd.Series(
            [level] * len(df),
            index=df.index
        )

        addplots.append(
            mpf.make_addplot(
                sweep_line,
                color="red"
            )
        )


    mpf.plot(
        df,
        type="candle",
        style="charles",
        title=f"{symbol} {timeframe} Liquidity Sweep",
        addplot=addplots,
        savefig=filename
    )


    return filename
