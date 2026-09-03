import pandas as pd
import joblib

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression


# ============================================================
# SETTINGS
# ============================================================

FEATURES = [
    "unemployment_pit",
    "yield_curve_pit",
    "claims_pit",
    "industrial_growth_pit"
]

TARGET = "recession_next_12m"


# ============================================================
# LOAD TRAINING DATA
# ============================================================

data = pd.read_csv(
    "data/recession_radar_point_in_time.csv"
)

data["observation_date"] = pd.to_datetime(
    data["observation_date"]
)

data = data.sort_values(
    "observation_date"
).reset_index(drop=True)


training = data.dropna(
    subset=FEATURES + [TARGET]
).copy()


# ============================================================
# TRAIN FINAL FROZEN MODEL
# ============================================================

model = Pipeline([
    (
        "scaler",
        StandardScaler()
    ),
    (
        "logistic",
        LogisticRegression(
            max_iter=1000
        )
    )
])


model.fit(
    training[FEATURES],
    training[TARGET]
)


# ============================================================
# SAVE MODEL
# ============================================================

joblib.dump(
    model,
    "models/core4_v1.joblib"
)


# ============================================================
# MODEL INFORMATION
# ============================================================

logistic = model.named_steps[
    "logistic"
]

coefficients = pd.DataFrame({
    "feature": FEATURES,
    "standardized_coefficient":
        logistic.coef_[0]
})


coefficients.to_csv(
    "data/core4_v1_coefficients.csv",
    index=False
)


print(
    "\nRECESSION RADAR CORE-4 v1"
)

print("=" * 75)

print(
    "Training observations:",
    len(training)
)

print(
    "Training period:",
    training[
        "observation_date"
    ].min().date(),
    "to",
    training[
        "observation_date"
    ].max().date()
)

print(
    "\nSTANDARDISED COEFFICIENTS"
)

print("=" * 75)

print(
    coefficients.to_string(
        index=False,
        formatters={
            "standardized_coefficient":
                "{:+.4f}".format
        }
    )
)

print(
    "\nModel saved to:"
)

print(
    "models/core4_v1.joblib"
)