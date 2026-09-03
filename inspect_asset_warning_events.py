import pandas as pd


data = pd.read_csv(
    "data/asset_warning_event_returns.csv"
)


print()
print("RECESSION RADAR — INDIVIDUAL WARNING EVENTS")
print("=" * 100)


assets = [
    "SPY",
    "IWM",
    "GLD",
    "USO",
    "UUP",
    "TLT"
]


for asset in assets:

    print()
    print(asset)
    print("-" * 100)

    sample = data[
        data["asset"] == asset
    ].copy()

    pivot = sample.pivot(
        index="event_month",
        columns="horizon_months",
        values="forward_return"
    )

    pivot = pivot.rename(
        columns={
            1: "1m",
            3: "3m",
            6: "6m",
            12: "12m"
        }
    )

    print(
        pivot.round(2).to_string()
    )