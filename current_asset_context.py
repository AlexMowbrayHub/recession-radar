import pandas as pd
from pathlib import Path


RADAR_FILE = Path(
    "data/live_radar_output.csv"
)

ASSET_FILE = Path(
    "data/asset_context.csv"
)

OUTPUT_FILE = Path(
    "data/current_asset_context.csv"
)


radar = pd.read_csv(RADAR_FILE)
assets = pd.read_csv(ASSET_FILE)


latest = radar.iloc[-1]


score_column = None

for candidate in [
    "radar_score",
    "score",
    "Radar Score"
]:

    if candidate in radar.columns:
        score_column = candidate
        break


if score_column is None:

    raise RuntimeError(
        "Could not find Radar score column in live_radar_output.csv."
    )


score = float(
    latest[score_column]
)


warning = score >= 35.0


context = {
    "radar_score": score,
    "warning": warning,
    "gold_context": (
        "historically defensive"
        if warning
        else "inactive"
    ),
    "oil_context": (
        "historically vulnerable"
        if warning
        else "inactive"
    ),
    "equity_context": (
        "large-cap relative bias"
        if warning
        else "inactive"
    ),
    "evidence_strength": "limited"
}


result = pd.DataFrame(
    [context]
)


result.to_csv(
    OUTPUT_FILE,
    index=False
)


print()
print("RECESSION RADAR — CURRENT ASSET CONTEXT")
print("=" * 70)

print(f"Radar score: {score:.2f}")
print(
    f"Warning: {'ON' if warning else 'OFF'}"
)

print()

print(
    "Gold:",
    context["gold_context"]
)

print(
    "Oil:",
    context["oil_context"]
)

print(
    "Equities:",
    context["equity_context"]
)

print(
    "Evidence:",
    context["evidence_strength"]
)

print()
print("Saved:")
print(OUTPUT_FILE)