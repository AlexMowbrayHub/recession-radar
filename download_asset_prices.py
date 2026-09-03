import yfinance as yf
import pandas as pd


# ============================================================
# ASSETS
# ============================================================

tickers = {
    "SPY": "SPY",   # S&P 500
    "IWM": "IWM",   # Russell 2000
    "GLD": "GLD",   # Gold
    "USO": "USO",   # Oil
    "UUP": "UUP",   # US Dollar
    "TLT": "TLT",   # Long-term US Treasuries
}


# ============================================================
# DOWNLOAD
# ============================================================

frames = []

for name, ticker in tickers.items():

    print(f"Downloading {name}...")

    data = yf.download(
        ticker,
        start="2005-01-01",
        interval="1mo",
        auto_adjust=True,
        progress=False
    )

    if data.empty:
        print(f"WARNING: No data returned for {name}")
        continue

    # yfinance can return MultiIndex columns.
    # Flatten them so the script works reliably.
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data = data.reset_index()

    data = data[
        [
            "Date",
            "Close"
        ]
    ].copy()

    data.columns = [
        "observation_date",
        name
    ]

    data["observation_date"] = pd.to_datetime(
        data["observation_date"]
    )

    frames.append(data)


# ============================================================
# CHECK
# ============================================================

if not frames:
    raise RuntimeError(
        "No asset data was downloaded."
    )


# ============================================================
# COMBINE
# ============================================================

combined = frames[0]

for frame in frames[1:]:

    combined = combined.merge(
        frame,
        on="observation_date",
        how="outer"
    )


combined = combined.sort_values(
    "observation_date"
).reset_index(drop=True)


# ============================================================
# SAVE
# ============================================================

output_path = "data/asset_monthly_prices.csv"

combined.to_csv(
    output_path,
    index=False
)


# ============================================================
# SUMMARY
# ============================================================

print()
print("=" * 80)
print("ASSET PRICE DOWNLOAD COMPLETE")
print("=" * 80)

print(
    f"Observations: {len(combined)}"
)

print(
    "Period:",
    combined["observation_date"].min().date(),
    "to",
    combined["observation_date"].max().date()
)

print()

for asset in tickers:

    if asset in combined.columns:

        count = combined[asset].notna().sum()

        print(
            f"{asset}: {count} monthly observations"
        )

print()
print("Saved to:")
print(output_path)