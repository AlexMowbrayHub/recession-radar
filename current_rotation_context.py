import pandas as pd


snapshot = pd.read_csv(
    "data/current_radar_snapshot.csv"
)


row = snapshot.iloc[-1]


score = float(
    row["radar_score"]
)


warning = bool(
    row["warning"]
)


if score < 10:

    context = "SMALL-CAP FAVOURABLE HISTORY"

    description = (
        "Very low Radar scores have historically "
        "been associated with stronger small-cap "
        "relative performance."
    )

elif score < 25:

    context = "NEUTRAL ROTATION CONTEXT"

    description = (
        "The current Radar level does not imply "
        "a strong historical large-versus-small "
        "rotation bias."
    )

elif score < 35:

    context = "LARGE-CAP STRENGTH WATCH"

    description = (
        "Higher Radar levels have historically "
        "been associated with increasing large-cap "
        "relative strength."
    )

else:

    context = "HISTORICAL LARGE-CAP BIAS"

    description = (
        "Warning-level Radar readings have historically "
        "been associated with stronger large-cap "
        "performance relative to small caps."
    )


output = pd.DataFrame(
    [
        {
            "radar_score": score,
            "warning": warning,
            "rotation_context": context,
            "description": description,
            "evidence_status": "HISTORICAL_CONTEXT"
        }
    ]
)


print()
print(
    "RECESSION RADAR — CURRENT EQUITY ROTATION CONTEXT"
)

print("=" * 80)

print(
    f"Radar Score: {score:.2f}"
)

print(
    f"Context: {context}"
)

print(
    f"Evidence: HISTORICAL CONTEXT"
)

print()

print(description)


output.to_csv(
    "data/current_rotation_context.csv",
    index=False
)