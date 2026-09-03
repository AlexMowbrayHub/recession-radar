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


radar[
    "observation_date"
] = pd.to_datetime(
    radar[
        "observation_date"
    ]
)


prices[
    "observation_date"
] = pd.to_datetime(
    prices[
        "observation_date"
    ]
)


# ============================================================
# ALIGN TO MONTH-END
# ============================================================

radar[
    "month"
] = (
    radar[
        "observation_date"
    ]
    .dt.to_period("M")
)


prices[
    "month"
] = (
    prices[
        "observation_date"
    ]
    .dt.to_period("M")
)


data = radar.merge(
    prices.drop(
        columns=[
            "observation_date"
        ]
    ),
    on="month",
    how="inner"
)


# ============================================================
# ASSETS / HORIZONS
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


# ============================================================
# FORWARD RETURNS
# ============================================================

for asset in assets:

    for horizon in horizons:

        column = (
            f"{asset}_fwd_{horizon}m"
        )


        data[
            column
        ] = (
            data[
                asset
            ].shift(
                -horizon
            )
            /
            data[
                asset
            ]
            - 1
        ) * 100


# ============================================================
# REGIME ANALYSIS
# ============================================================

rows = []


for asset in assets:

    for horizon in horizons:

        return_column = (
            f"{asset}_fwd_{horizon}m"
        )


        for warning_state in [
            0,
            1
        ]:

            sample = data[
                data[
                    "warning"
                ]
                ==
                warning_state
            ].dropna(
                subset=[
                    return_column
                ]
            )


            rows.append({
                "asset":
                    asset,

                "horizon_months":
                    horizon,

                "warning":
                    warning_state,

                "observations":
                    len(sample),

                "mean_forward_return":
                    sample[
                        return_column
                    ].mean(),

                "median_forward_return":
                    sample[
                        return_column
                    ].median(),

                "positive_return_rate":
                    (
                        sample[
                            return_column
                        ]
                        > 0
                    ).mean()
                    * 100
            })


results = pd.DataFrame(
    rows
)


print(
    "\nRECESSION RADAR — ASSET RESPONSE"
)

print("=" * 110)


print(
    results.to_string(
        index=False,
        formatters={
            "mean_forward_return":
                "{:.2f}".format,

            "median_forward_return":
                "{:.2f}".format,

            "positive_return_rate":
                "{:.1f}".format
        }
    )
)


results.to_csv(
    "data/asset_response_results.csv",
    index=False
)