import pandas as pd
import numpy as np


# ============================================================
# LOAD DATA
# ============================================================

radar = pd.read_csv(
    "data/recession_radar_history_v1.csv"
)

prices = pd.read_csv(
    "data/asset_monthly_prices.csv"
)


radar["observation_date"] = pd.to_datetime(
    radar["observation_date"]
)

prices["observation_date"] = pd.to_datetime(
    prices["observation_date"]
)


# ============================================================
# MONTH ALIGNMENT
# ============================================================

radar["month"] = radar["observation_date"].dt.to_period("M")
prices["month"] = prices["observation_date"].dt.to_period("M")


data = radar.merge(
    prices.drop(columns=["observation_date"]),
    on="month",
    how="inner"
)

data = data.sort_values("month").reset_index(drop=True)


# ============================================================
# IDENTIFY WARNING ACTIVATIONS
# ============================================================

data["warning"] = data["warning"].astype(int)

data["warning_activation"] = (
    (data["warning"] == 1)
    &
    (data["warning"].shift(1).fillna(0) == 0)
)


activation_indices = data.index[
    data["warning_activation"]
].tolist()


print()
print("RECESSION RADAR — WARNING ACTIVATION EVENTS")
print("=" * 90)

for i in activation_indices:

    print(
        data.loc[i, "month"],
        "Score:",
        round(
            data.loc[i, "radar_score"],
            2
        )
    )


# ============================================================
# ASSET EVENT RETURNS
# ============================================================

assets = [
    "SPY",
    "IWM",
    "GLD",
    "USO",
    "UUP",
    "TLT"
]

horizons = [
    1,
    3,
    6,
    12
]


rows = []


for i in activation_indices:

    event_month = data.loc[i, "month"]
    event_score = data.loc[i, "radar_score"]

    for asset in assets:

        if pd.isna(
            data.loc[i, asset]
        ):
            continue

        entry_price = data.loc[i, asset]

        for horizon in horizons:

            future_i = i + horizon

            if future_i >= len(data):
                continue

            exit_price = data.loc[
                future_i,
                asset
            ]

            if pd.isna(exit_price):
                continue

            forward_return = (
                exit_price
                /
                entry_price
                - 1
            ) * 100

            rows.append({
                "event_month":
                    str(event_month),

                "event_score":
                    event_score,

                "asset":
                    asset,

                "horizon_months":
                    horizon,

                "forward_return":
                    forward_return
            })


events = pd.DataFrame(rows)


# ============================================================
# SAVE EVENT DETAIL
# ============================================================

events.to_csv(
    "data/asset_warning_event_returns.csv",
    index=False
)


# ============================================================
# SUMMARY
# ============================================================

summary = (
    events
    .groupby(
        [
            "asset",
            "horizon_months"
        ]
    )
    .agg(
        events=(
            "forward_return",
            "count"
        ),

        mean_return=(
            "forward_return",
            "mean"
        ),

        median_return=(
            "forward_return",
            "median"
        ),

        positive_rate=(
            "forward_return",
            lambda x:
                (x > 0).mean() * 100
        ),

        worst_return=(
            "forward_return",
            "min"
        ),

        best_return=(
            "forward_return",
            "max"
        )
    )
    .reset_index()
)


print()
print("ASSET PERFORMANCE AFTER RADAR WARNING ACTIVATION")
print("=" * 110)

print(
    summary.to_string(
        index=False,
        formatters={
            "mean_return":
                "{:.2f}".format,

            "median_return":
                "{:.2f}".format,

            "positive_rate":
                "{:.1f}".format,

            "worst_return":
                "{:.2f}".format,

            "best_return":
                "{:.2f}".format
        }
    )
)


summary.to_csv(
    "data/asset_warning_event_summary.csv",
    index=False
)

print()
print("Saved:")
print("data/asset_warning_event_returns.csv")
print("data/asset_warning_event_summary.csv")