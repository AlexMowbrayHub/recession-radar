from pathlib import Path
import pandas as pd
import joblib


# ============================================================
# REQUIRED FILES
# ============================================================

required_files = [
    "models/core4_v1.joblib",
    "data/live_core4_latest.csv",
    "data/live_radar_output.csv",
    "data/current_radar_snapshot.csv",
    "data/recession_radar_history_v1.csv",
    "MODEL_CARD.md",
    "data/current_asset_context.csv",
    "README.md"
]


print(
    "\nRECESSION RADAR — PRODUCTION CHECK"
)

print("=" * 85)


all_present = True


for filename in required_files:

    exists = Path(
        filename
    ).exists()

    print(
        f"{filename:<45}",
        "PASS"
        if exists
        else "MISSING"
    )


    if not exists:
        all_present = False


if not all_present:

    raise RuntimeError(
        "Required production files are missing."
    )


# ============================================================
# MODEL LOAD
# ============================================================

model = joblib.load(
    "models/core4_v1.joblib"
)


print(
    "\nModel load:"
    " PASS"
)


# ============================================================
# LIVE OUTPUT
# ============================================================

live = pd.read_csv(
    "data/live_radar_output.csv"
)


score = float(
    live["radar_score"].iloc[0]
)


if not (
    0 <= score <= 100
):

    raise RuntimeError(
        "Radar score outside expected range."
    )


print(
    "Radar score range:"
    " PASS"
)


print(
    "Current Radar score:",
    f"{score:.2f}"
)


# ============================================================
# SNAPSHOT
# ============================================================

snapshot = pd.read_csv(
    "data/current_radar_snapshot.csv"
)


required_columns = [
    "observation_date",
    "radar_score",
    "warning_threshold",
    "warning",
    "signal_state",
    "historical_percentile"
]


missing_columns = [
    column
    for column in required_columns
    if column not in snapshot.columns
]


if missing_columns:

    raise RuntimeError(
        "Snapshot missing columns: "
        + str(missing_columns)
    )


print(
    "Snapshot schema:"
    " PASS"
)


# ============================================================
# COMPLETE
# ============================================================

print()

print("=" * 85)

print(
    "RECESSION RADAR v1.0 PRODUCTION CHECK PASSED"
)

print("=" * 85)