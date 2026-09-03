import pandas as pd
import numpy as np


np.random.seed(42)


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


radar["month"] = (
    radar[
        "observation_date"
    ]
    .dt.to_period("M")
)


prices["month"] = (
    prices[
        "observation_date"
    ]
    .dt.to_period("M")
)


data = radar.merge(
    prices.drop(
        columns="observation_date"
    ),
    on="month",
    how="inner"
)


data = data.sort_values(
    "month"
).reset_index(drop=True)


data["activation"] = (
    (data["warning"] == 1)
    &
    (
        data[
            "warning"
        ]
        .shift(1)
        .fillna(0)
        == 0
    )
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


iterations = 5000


rows = []


for asset in assets:

    for horizon in horizons:

        temp = data.dropna(
            subset=[asset]
        ).copy()

        temp[
            "forward_return"
        ] = (
            temp[
                asset
            ]
            .shift(-horizon)
            /
            temp[
                asset
            ]
            - 1
        ) * 100


        temp = temp.dropna(
            subset=[
                "forward_return"
            ]
        )


        event_returns = temp.loc[
            temp["activation"],
            "forward_return"
        ]


        n_events = len(
            event_returns
        )


        if n_events < 2:
            continue


        observed_mean = (
            event_returns.mean()
        )


        random_means = []


        values = temp[
            "forward_return"
        ].to_numpy()


        for _ in range(
            iterations
        ):

            sample = np.random.choice(
                values,
                size=n_events,
                replace=False
            )

            random_means.append(
                sample.mean()
            )


        random_means = np.array(
            random_means
        )


        percentile = (
            (
                random_means
                <=
                observed_mean
            ).mean()
            * 100
        )


        rows.append({
            "asset":
                asset,

            "horizon_months":
                horizon,

            "events":
                n_events,

            "observed_mean":
                observed_mean,

            "random_mean":
                random_means.mean(),

            "random_5pct":
                np.percentile(
                    random_means,
                    5
                ),

            "random_95pct":
                np.percentile(
                    random_means,
                    95
                ),

            "observed_percentile":
                percentile
        })


results = pd.DataFrame(rows)


print()
print("RECESSION RADAR — RANDOM EVENT BENCHMARK")
print("=" * 110)


print(
    results.to_string(
        index=False,
        formatters={
            "observed_mean":
                "{:.2f}".format,

            "random_mean":
                "{:.2f}".format,

            "random_5pct":
                "{:.2f}".format,

            "random_95pct":
                "{:.2f}".format,

            "observed_percentile":
                "{:.1f}".format
        }
    )
)


results.to_csv(
    "data/random_event_benchmark.csv",
    index=False
)