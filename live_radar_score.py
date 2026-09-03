import joblib
import pandas as pd


FEATURES = [
    "unemployment_pit",
    "yield_curve_pit",
    "claims_pit",
    "industrial_growth_pit"
]


# ============================================================
# LOAD
# ============================================================

model = joblib.load(
    "models/core4_v1.joblib"
)


live = pd.read_csv(
    "data/live_core4_latest.csv"
)


live[
    "observation_date"
] = pd.to_datetime(
    live[
        "observation_date"
    ]
)


X = live[FEATURES]


# ============================================================
# SCORE
# ============================================================

raw_score = (
    model.predict_proba(
        X
    )[0, 1]
)


radar_score = (
    raw_score * 100
)


# ============================================================
# WARNING STATE
# ============================================================

threshold = 0.35


warning = (
    raw_score >= threshold
)


# ============================================================
# OUTPUT
# ============================================================

print(
    "\nRECESSION RADAR v1.0"
)

print("=" * 75)


print(
    "Observation date:",
    live[
        "observation_date"
    ].iloc[0].date()
)


print()

print(
    "CORE INPUTS"
)

print("-" * 75)


print(
    "Unemployment:",
    round(
        live[
            "unemployment_pit"
        ].iloc[0],
        3
    )
)


print(
    "10Y–2Y yield curve:",
    round(
        live[
            "yield_curve_pit"
        ].iloc[0],
        3
    )
)


print(
    "Initial claims:",
    round(
        live[
            "claims_pit"
        ].iloc[0]
    )
)


print(
    "Industrial production growth:",
    round(
        live[
            "industrial_growth_pit"
        ].iloc[0],
        3
    ),
    "%"
)


print()

print(
    "RADAR SCORE:",
    f"{radar_score:.2f}"
)


print(
    "LOCKED WARNING THRESHOLD:",
    "35.00"
)


print(
    "WARNING STATE:",
    "ON"
    if warning
    else "OFF"
)


print()

print(
    "The Radar score is a model score,"
)

print(
    "not a calibrated probability of recession."
)


# ============================================================
# SAVE
# ============================================================

result = live.copy()

result[
    "radar_score"
] = radar_score

result[
    "warning_threshold"
] = threshold * 100

result[
    "warning"
] = int(warning)


result.to_csv(
    "data/live_radar_output.csv",
    index=False
)


print()

print(
    "Saved to:"
)

print(
    "data/live_radar_output.csv"
)