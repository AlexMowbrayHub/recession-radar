import pandas as pd


live = pd.read_csv(
    "data/live_radar_output.csv"
)

context = pd.read_csv(
    "data/current_radar_context.csv"
)

drivers = pd.read_csv(
    "data/live_feature_contributions.csv"
)


# ============================================================
# STRONGEST DRIVER
# ============================================================

drivers = drivers.sort_values(
    "log_odds_contribution",
    ascending=False
)


strongest = (
    drivers.iloc[0]
)


# ============================================================
# COMBINE
# ============================================================

# ============================================================
# DESCRIPTIVE STATE
# ============================================================

score = float(
    live["radar_score"].iloc[0]
)


if score >= 35:

    signal_state = "WARNING"

elif score >= 28.74:

    signal_state = "Elevated"

elif score >= 9.65:

    signal_state = "Normal range"

else:

    signal_state = "Below historical median"


snapshot = pd.DataFrame([
    {
        "observation_date":
            live[
                "observation_date"
            ].iloc[0],

        "radar_score":
            live[
                "radar_score"
            ].iloc[0],

        "warning_threshold":
            live[
                "warning_threshold"
            ].iloc[0],

        "warning":
            live[
                "warning"
            ].iloc[0],

        "historical_percentile":
            context[
                "historical_percentile"
            ].iloc[0],
 
"signal_state":
    signal_state,

        "unemployment":
            live[
                "unemployment_pit"
            ].iloc[0],

        "yield_curve":
            live[
                "yield_curve_pit"
            ].iloc[0],

        "initial_claims":
            live[
                "claims_pit"
            ].iloc[0],

        "industrial_growth":
            live[
                "industrial_growth_pit"
            ].iloc[0],

        "strongest_driver":
            strongest[
                "feature"
            ],

        "strongest_driver_contribution":
            strongest[
                "log_odds_contribution"
            ]
    }
])


snapshot.to_csv(
    "data/current_radar_snapshot.csv",
    index=False
)


print(
    "\nCURRENT RADAR SNAPSHOT"
)

print("=" * 90)

print(
    snapshot.to_string(
        index=False
    )
)


print(
    "\nSaved to:"
)

print(
    "data/current_radar_snapshot.csv"
)