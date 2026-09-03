import joblib
import pandas as pd


FEATURES = [
    "unemployment_pit",
    "yield_curve_pit",
    "claims_pit",
    "industrial_growth_pit"
]


model = joblib.load(
    "models/core4_v1.joblib"
)


scaler = model.named_steps[
    "scaler"
]

logistic = model.named_steps[
    "logistic"
]


rows = []


for i, feature in enumerate(FEATURES):

    rows.append({
        "feature":
            feature,

        "mean":
            scaler.mean_[i],

        "scale":
            scaler.scale_[i],

        "coefficient":
            logistic.coef_[0][i]
    })


constants = pd.DataFrame(rows)


print(
    "\nRECESSION RADAR — PINE CONSTANTS"
)

print("=" * 90)


print(
    constants.to_string(
        index=False,
        formatters={
            "mean":
                "{:.10f}".format,

            "scale":
                "{:.10f}".format,

            "coefficient":
                "{:+.10f}".format
        }
    )
)


print()

print(
    "INTERCEPT:"
)

print(
    f"{logistic.intercept_[0]:+.10f}"
)


constants.to_csv(
    "data/pine_model_constants.csv",
    index=False
)