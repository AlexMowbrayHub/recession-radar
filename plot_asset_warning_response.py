import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


INPUT_FILE = Path(
    "data/asset_warning_event_summary.csv"
)

OUTPUT_FILE = Path(
    "outputs/asset_warning_response.png"
)


data = pd.read_csv(INPUT_FILE)


horizon = 6

plot_data = data[
    data["horizon_months"] == horizon
].copy()


preferred_order = [
    "GLD",
    "SPY",
    "TLT",
    "IWM",
    "UUP",
    "USO"
]


plot_data["asset"] = pd.Categorical(
    plot_data["asset"],
    categories=preferred_order,
    ordered=True
)

plot_data = plot_data.sort_values(
    "asset"
)


fig, ax = plt.subplots(
    figsize=(11, 6)
)


bars = ax.bar(
    plot_data["asset"],
    plot_data["mean_return"]
)


ax.axhline(
    0,
    linewidth=1
)


ax.set_title(
    "Recession Radar — Asset Performance After Warning Activation"
)

ax.set_ylabel(
    "Mean 6-Month Forward Return (%)"
)

ax.set_xlabel(
    "Asset"
)


for bar, value in zip(
    bars,
    plot_data["mean_return"]
):

    position = (
        value + 0.4
        if value >= 0
        else value - 1.2
    )

    ax.text(
        bar.get_x()
        + bar.get_width() / 2,
        position,
        f"{value:.1f}%",
        ha="center",
        fontsize=10
    )


ax.text(
    0.01,
    0.02,
    "Historical research only — small number of independent warning events",
    transform=ax.transAxes,
    fontsize=9
)


plt.tight_layout()


OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)


plt.savefig(
    OUTPUT_FILE,
    dpi=200,
    bbox_inches="tight"
)


plt.close()


print()
print("Saved:")
print(OUTPUT_FILE)