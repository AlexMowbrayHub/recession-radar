import pandas as pd


# ============================================================
# LOAD
# ============================================================

data = pd.read_csv(
    "data/recession_radar_history_v1.csv"
)

data["observation_date"] = pd.to_datetime(
    data["observation_date"]
)

data = data.sort_values(
    "observation_date"
).reset_index(drop=True)


# ============================================================
# CURRENT SCORE
# ============================================================

latest = data.iloc[-1]

current_score = float(
    latest["radar_score"]
)


# ============================================================
# HISTORICAL SAMPLE
# ============================================================

historical = data[
    data["source"]
    == "historical walk-forward"
].copy()


percentile = (
    (
        historical["radar_score"]
        <= current_score
    ).mean()
    * 100
)


# ============================================================
# DISTRIBUTION STATS
# ============================================================

median_score = (
    historical["radar_score"].median()
)

p25 = (
    historical["radar_score"]
    .quantile(0.25)
)

p75 = (
    historical["radar_score"]
    .quantile(0.75)
)

p90 = (
    historical["radar_score"]
    .quantile(0.90)
)


print(
    "\nCURRENT RECESSION RADAR CONTEXT"
)

print("=" * 80)

print(
    "Observation date:",
    latest[
        "observation_date"
    ].date()
)

print(
    "Current Radar score:",
    f"{current_score:.2f}"
)

print(
    "Historical percentile:",
    f"{percentile:.1f}"
)

print()

print(
    "Historical median:",
    f"{median_score:.2f}"
)

print(
    "25th percentile:",
    f"{p25:.2f}"
)

print(
    "75th percentile:",
    f"{p75:.2f}"
)

print(
    "90th percentile:",
    f"{p90:.2f}"
)


# ============================================================
# SAVE
# ============================================================

summary = pd.DataFrame([
    {
        "observation_date":
            latest[
                "observation_date"
            ],

        "radar_score":
            current_score,

        "historical_percentile":
            percentile,

        "historical_median":
            median_score,

        "historical_p25":
            p25,

        "historical_p75":
            p75,

        "historical_p90":
            p90
    }
])


summary.to_csv(
    "data/current_radar_context.csv",
    index=False
)


print()

print(
    "Saved to:"
)

print(
    "data/current_radar_context.csv"
)