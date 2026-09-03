import pandas as pd
import numpy as np


# ============================================================
# LOAD
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


radar["month"] = radar["observation_date"].dt.to_period("M")
prices["month"] = prices["observation_date"].dt.to_period("M")


data = radar.merge(
    prices.drop(columns=["observation_date"]),
    on="month",
    how="inner"
)


data = data.sort_values(
    "month"
).reset_index(drop=True)


# ============================================================
# SCORE BANDS
# ============================================================

data["score_band"] = pd.cut(
    data["radar_score"],
    bins=[
        -np.inf,
        9.65,
        28.74,
        35.0,
        50.0,
        75.0,
        np.inf
    ],
    labels=[
        "<9.65",
        "9.65-28.74",
        "28.74-35",
        "35-50",
        "50-75",
        "75+"
    ],
    right=False
)


assets = [
    "SPY",
    "IWM",
    "GLD",
    "USO",
    "UUP",
    "TLT"
]

horizons = [
    3,
    6,
    12
]


# ============================================================
# FORWARD RETURNS
# ============================================================

for asset in assets:

    for horizon in horizons:

        data[
            f"{asset}_{horizon}m"
        ] = (
            data[asset].shift(-horizon)
            /
            data[asset]
            - 1
        ) * 100


# ============================================================
# ANALYSIS
# ============================================================

rows = []


for asset in assets:

    for horizon in horizons:

        return_column = (
            f"{asset}_{horizon}m"
        )

        for band in data[
            "score_band"
        ].cat.categories:

            sample = data[
                data["score_band"] == band
            ].dropna(
                subset=[return_column]
            )

            if len(sample) == 0:
                continue

            rows.append({
                "asset":
                    asset,

                "horizon_months":
                    horizon,

                "score_band":
                    str(band),

                "observations":
                    len(sample),

                "mean_return":
                    sample[
                        return_column
                    ].mean(),

                "median_return":
                    sample[
                        return_column
                    ].median(),

                "positive_rate":
                    (
                        sample[
                            return_column
                        ] > 0
                    ).mean() * 100
            })


results = pd.DataFrame(rows)


print()
print("RECESSION RADAR — ASSET RETURNS BY SCORE BAND")
print("=" * 110)

print(
    results.to_string(
        index=False,
        formatters={
            "mean_return":
                "{:.2f}".format,

            "median_return":
                "{:.2f}".format,

            "positive_rate":
                "{:.1f}".format
        }
    )
)


results.to_csv(
    "data/asset_score_band_results.csv",
    index=False
)