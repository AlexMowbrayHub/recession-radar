import pandas as pd
from pathlib import Path


EVENT_FILE = Path("data/asset_warning_event_returns.csv")
OUTPUT_FILE = Path("data/asset_context.csv")


data = pd.read_csv(EVENT_FILE)


def summarise_asset(asset):

    sample = data[
        data["asset"] == asset
    ].copy()

    rows = []

    for horizon in [3, 6, 12]:

        h = sample[
            sample["horizon_months"] == horizon
        ]

        if h.empty:
            continue

        rows.append({
            "asset": asset,
            "horizon_months": horizon,
            "events": len(h),
            "mean_return": h["forward_return"].mean(),
            "median_return": h["forward_return"].median(),
            "positive_rate": (
                (h["forward_return"] > 0).mean() * 100
            )
        })

    return rows


rows = []

for asset in [
    "SPY",
    "IWM",
    "GLD",
    "USO",
    "UUP",
    "TLT"
]:

    rows.extend(
        summarise_asset(asset)
    )


result = pd.DataFrame(rows)


result.to_csv(
    OUTPUT_FILE,
    index=False
)


print()
print("RECESSION RADAR — ASSET CONTEXT")
print("=" * 90)

print(
    result.to_string(
        index=False,
        formatters={
            "mean_return": "{:.2f}".format,
            "median_return": "{:.2f}".format,
            "positive_rate": "{:.1f}".format
        }
    )
)

print()
print("Saved:")
print(OUTPUT_FILE)