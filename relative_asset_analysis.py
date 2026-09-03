import pandas as pd


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
# RELATIVE ASSET PAIRS
# ============================================================

pairs = [
    ("GLD", "SPY"),
    ("TLT", "SPY"),
    ("SPY", "IWM"),
    ("GLD", "USO"),
    ("UUP", "SPY")
]


horizons = [
    3,
    6,
    12
]


rows = []


for long_asset, comparison_asset in pairs:

    for horizon in horizons:

        long_return = (
            data[long_asset].shift(-horizon)
            /
            data[long_asset]
            - 1
        ) * 100

        comparison_return = (
            data[comparison_asset].shift(-horizon)
            /
            data[comparison_asset]
            - 1
        ) * 100

        relative_return = (
            long_return
            -
            comparison_return
        )


        for warning_state in [
            0,
            1
        ]:

            mask = (
                data["warning"]
                ==
                warning_state
            )

            sample = relative_return[
                mask
            ].dropna()


            rows.append({
                "pair":
                    f"{long_asset} vs {comparison_asset}",

                "horizon_months":
                    horizon,

                "warning":
                    warning_state,

                "observations":
                    len(sample),

                "mean_relative_return":
                    sample.mean(),

                "median_relative_return":
                    sample.median(),

                "outperformance_rate":
                    (
                        sample > 0
                    ).mean() * 100
            })


results = pd.DataFrame(rows)


print()
print("RECESSION RADAR — RELATIVE ASSET PERFORMANCE")
print("=" * 110)

print(
    results.to_string(
        index=False,
        formatters={
            "mean_relative_return":
                "{:.2f}".format,

            "median_relative_return":
                "{:.2f}".format,

            "outperformance_rate":
                "{:.1f}".format
        }
    )
)


results.to_csv(
    "data/relative_asset_results.csv",
    index=False
)