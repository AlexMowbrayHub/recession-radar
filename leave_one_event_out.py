import pandas as pd


data = pd.read_csv(
    "data/asset_warning_event_returns.csv"
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


rows = []


for asset in assets:

    for horizon in horizons:

        sample = data[
            (data["asset"] == asset)
            &
            (data["horizon_months"] == horizon)
        ].copy()

        events = sample[
            "event_month"
        ].unique()


        for excluded_event in events:

            remaining = sample[
                sample[
                    "event_month"
                ]
                !=
                excluded_event
            ]


            if remaining.empty:
                continue


            rows.append({
                "asset":
                    asset,

                "horizon_months":
                    horizon,

                "excluded_event":
                    excluded_event,

                "remaining_events":
                    len(remaining),

                "mean_return":
                    remaining[
                        "forward_return"
                    ].mean(),

                "median_return":
                    remaining[
                        "forward_return"
                    ].median(),

                "positive_rate":
                    (
                        remaining[
                            "forward_return"
                        ]
                        > 0
                    ).mean()
                    * 100
            })


results = pd.DataFrame(rows)


print()
print("RECESSION RADAR — LEAVE-ONE-EVENT-OUT TEST")
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
    "data/leave_one_event_out_results.csv",
    index=False
)