import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# LOAD
# ============================================================

data = pd.read_csv(
    "data/live_feature_contributions.csv"
)


data = data.sort_values(
    "log_odds_contribution"
)


# ============================================================
# PLOT
# ============================================================

fig, ax = plt.subplots(
    figsize=(9, 5)
)


ax.barh(
    data["feature"],
    data["log_odds_contribution"]
)


ax.axvline(
    0,
    linewidth=1
)


# ============================================================
# LABELS
# ============================================================

for i, value in enumerate(
    data["log_odds_contribution"]
):

    ax.text(
        value + 0.015,
        i,
        f"{value:+.2f}",
        va="center"
    )


ax.set_title(
    "What's Driving the Current Radar Score?"
)

ax.set_xlabel(
    "Contribution to model log-odds"
)


fig.text(
    0.01,
    0.015,
    (
        "Positive values raise the Radar score; "
        "negative values lower it. "
        "Contributions are not percentage-point effects."
    ),
    fontsize=9
)


ax.spines[
    "top"
].set_visible(False)

ax.spines[
    "right"
].set_visible(False)


ax.grid(
    axis="x",
    alpha=0.15
)


plt.tight_layout(
    rect=[
        0,
        0.06,
        1,
        1
    ]
)


plt.savefig(
    "outputs/live_radar_drivers.png",
    dpi=250,
    bbox_inches="tight"
)


plt.show()


print(
    "\nSaved driver chart to:"
)

print(
    "outputs/live_radar_drivers.png"
)