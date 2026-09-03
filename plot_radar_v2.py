import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# LOAD
# ============================================================

radar = pd.read_csv(
    "data/recession_radar_history_v1.csv"
)

economic = pd.read_csv(
    "data/recession_radar_dataset.csv"
)


radar["observation_date"] = pd.to_datetime(
    radar["observation_date"]
)

economic["observation_date"] = pd.to_datetime(
    economic["observation_date"]
)


# ============================================================
# FIGURE
# ============================================================

fig, ax = plt.subplots(
    figsize=(15, 7.5)
)


# ============================================================
# RECESSION SHADING FIRST
# ============================================================

economic = economic.sort_values(
    "observation_date"
)


in_recession = False
start = None


for _, row in economic.iterrows():

    if (
        row["recession"] == 1
        and not in_recession
    ):

        start = row[
            "observation_date"
        ]

        in_recession = True


    elif (
        row["recession"] == 0
        and in_recession
    ):

        end = row[
            "observation_date"
        ]

        ax.axvspan(
            start,
            end,
            alpha=0.12
        )

        in_recession = False


# ============================================================
# RADAR SERIES
# ============================================================

ax.plot(
    radar["observation_date"],
    radar["radar_score"],
    linewidth=1.8,
    label="Recession Radar"
)


# ============================================================
# WARNING THRESHOLD
# ============================================================

ax.axhline(
    35,
    linestyle="--",
    linewidth=1.3,
    label="Warning threshold"
)


# ============================================================
# CURRENT POINT
# ============================================================

latest = radar.iloc[-1]


ax.scatter(
    latest["observation_date"],
    latest["radar_score"],
    s=90,
    zorder=5
)


ax.annotate(
    (
        f'Current: {latest["radar_score"]:.1f}\n'
f'Normal range'
    ),
    (
        latest["observation_date"],
        latest["radar_score"]
    ),
    xytext=(18, 12),
    textcoords="offset points",
    fontsize=10
)


# ============================================================
# TITLES
# ============================================================

fig.suptitle(
    "Recession Radar",
    fontsize=19,
    fontweight="bold",
    x=0.06,
    y=0.97,
    ha="left"
)


fig.text(
    0.06,
    0.925,
    (
        "Point-in-time-aware US recession-start risk signal "
        "| 12-month horizon"
    ),
    fontsize=10,
    ha="left"
)

# ============================================================
# AXES
# ============================================================

ax.set_ylabel(
    "Radar Score"
)

ax.set_xlabel("")

ax.set_ylim(
    0,
    105
)


ax.set_xlim(
    radar[
        "observation_date"
    ].min(),
    radar[
        "observation_date"
    ].max()
    + pd.DateOffset(months=30)
)


# ============================================================
# FOOTNOTE
# ============================================================

fig.text(
    0.01,
    0.015,
    (
        "Score is not a calibrated recession probability. "
        "Shaded areas indicate NBER recession periods. "
        "Historical series uses purged walk-forward predictions."
    ),
    fontsize=9
)


# ============================================================
# STYLE
# ============================================================

ax.grid(
    alpha=0.18
)

ax.spines[
    "top"
].set_visible(False)

ax.spines[
    "right"
].set_visible(False)


ax.legend(
    frameon=False,
    loc="upper left"
)


plt.tight_layout(
    rect=[
        0.04,
        0.06,
        0.98,
        0.89
    ]
)


plt.savefig(
    "outputs/recession_radar_v2.png",
    dpi=250,
    bbox_inches="tight"
)


plt.show()


print(
    "\nSaved chart to:"
)

print(
    "outputs/recession_radar_v2.png"
)