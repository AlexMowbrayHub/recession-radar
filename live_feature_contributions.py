import joblib
import pandas as pd


FEATURES = [
    "unemployment_pit",
    "yield_curve_pit",
    "claims_pit",
    "industrial_growth_pit"
]


DISPLAY_NAMES = {
    "unemployment_pit":
        "Unemployment",

    "yield_curve_pit":
        "Yield curve",

    "claims_pit":
        "Initial claims",

    "industrial_growth_pit":
        "Industrial production growth"
}


# ============================================================
# LOAD
# ============================================================

model = joblib.load(
    "models/core4_v1.joblib"
)

live = pd.read_csv(
    "data/live_core4_latest.csv"
)


X = live[FEATURES]


# ============================================================
# EXTRACT MODEL PARTS
# ============================================================

scaler = model.named_steps[
    "scaler"
]

logistic = model.named_steps[
    "logistic"
]


standardized = scaler.transform(
    X
)[0]


coefficients = (
    logistic.coef_[0]
)


contributions = (
    standardized
    * coefficients
)


# ============================================================
# OUTPUT
# ============================================================

rows = []


for feature, standardized_value, coefficient, contribution in zip(
    FEATURES,
    standardized,
    coefficients,
    contributions
):

    rows.append({
        "feature":
            DISPLAY_NAMES[feature],

        "raw_value":
            float(X[feature].iloc[0]),

        "standardized_value":
            standardized_value,

        "coefficient":
            coefficient,

        "log_odds_contribution":
            contribution
    })


results = pd.DataFrame(rows)


results["direction"] = results[
    "log_odds_contribution"
].apply(
    lambda x:
        "Raises score"
        if x > 0
        else "Lowers score"
)


results = results.sort_values(
    "log_odds_contribution",
    ascending=False
)


print(
    "\nCURRENT RECESSION RADAR DRIVERS"
)

print("=" * 105)


print(
    results.to_string(
        index=False,
        formatters={
            "raw_value":
                "{:.3f}".format,

            "standardized_value":
                "{:+.3f}".format,

            "coefficient":
                "{:+.3f}".format,

            "log_odds_contribution":
                "{:+.3f}".format
        }
    )
)


results.to_csv(
    "data/live_feature_contributions.csv",
    index=False
)


print(
    "\nSaved to:"
)

print(
    "data/live_feature_contributions.csv"
)