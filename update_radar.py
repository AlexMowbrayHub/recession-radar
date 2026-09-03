import subprocess
import sys


scripts = [
    "build_live_core4.py",
    "live_radar_score.py",
    "build_radar_history_v1.py",
    "current_score_percentile.py",
    "live_feature_contributions.py",
    "build_current_snapshot.py",
    "current_asset_context.py",
]


print(
    "\nRECESSION RADAR — UPDATE PIPELINE"
)

print("=" * 80)


for script in scripts:

    print(
        f"\nRunning {script}..."
    )

    print("-" * 80)


    result = subprocess.run(
        [
            sys.executable,
            script
        ]
    )


    if result.returncode != 0:

        print(
            f"\nUPDATE FAILED AT: {script}"
        )

        sys.exit(
            result.returncode
        )


print()

print("=" * 80)

print(
    "RECESSION RADAR UPDATE COMPLETE"
)

print("=" * 80)

print(
    "\nCurrent outputs:"
)

print(
    "data/live_radar_output.csv"
)

print(
    "data/current_radar_snapshot.csv"
)

print(
    "data/recession_radar_history_v1.csv"
)