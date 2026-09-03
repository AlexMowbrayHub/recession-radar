import pandas as pd


# ============================================================
# LOAD HISTORICAL WALK-FORWARD PREDICTIONS
# ============================================================

history = pd.read_csv(
    "data/point_in_time_core4_predictions.csv"
)

history["observation_date"] = pd.to_datetime(
    history["observation_date"]
)

history = history[
    [
        "observation_date",
        "predicted_probability",
        "actual"
    ]
].copy()


history["radar_score"] = (
    history["predicted_probability"] * 100
)

history["source"] = "historical walk-forward"


# ============================================================
# LOAD LIVE SCORE
# ============================================================

live = pd.read_csv(
    "data/live_radar_output.csv"
)

live["observation_date"] = pd.to_datetime(
    live["observation_date"]
)


live_row = pd.DataFrame([
    {
        "observation_date":
            live["observation_date"].iloc[0],

        "predicted_probability":
            live["radar_score"].iloc[0] / 100,

        "actual":
            None,

        "radar_score":
            live["radar_score"].iloc[0],

        "source":
            "live frozen model"
    }
])


# ============================================================
# COMBINE
# ============================================================

combined = pd.concat(
    [
        history,
        live_row
    ],
    ignore_index=True
)


combined = combined.sort_values(
    "observation_date"
).reset_index(drop=True)


# ============================================================
# WARNING STATE
# ============================================================

combined["warning"] = (
    combined["radar_score"] >= 35
).astype(int)


combined.to_csv(
    "data/recession_radar_history_v1.csv",
    index=False
)


print(
    "\nRECESSION RADAR v1 — HISTORY CREATED"
)

print("=" * 85)

print(
    "Observations:",
    len(combined)
)

print(
    "Start:",
    combined["observation_date"].min().date()
)

print(
    "Latest:",
    combined["observation_date"].max().date()
)

print(
    "Latest score:",
    round(
        combined["radar_score"].iloc[-1],
        2
    )
)

print(
    "Latest warning:",
    "ON"
    if combined["warning"].iloc[-1] == 1
    else "OFF"
)

print(
    "\nSaved to:"
)

print(
    "data/recession_radar_history_v1.csv"
)