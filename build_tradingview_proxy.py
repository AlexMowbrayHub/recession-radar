import os
import time
import requests
import pandas as pd
import numpy as np

from sklearn.metrics import (
    roc_auc_score,
    average_precision_score
)


# ============================================================
# SETTINGS
# ============================================================

API_KEY = os.getenv("FRED_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "FRED_API_KEY is not set in this PowerShell session."
    )


BASE_URL = (
    "https://api.stlouisfed.org/fred/series/observations"
)


START_DATE = "1982-01-01"


# ============================================================
# FROZEN MODEL CONSTANTS
# ============================================================

UNEMPLOYMENT_MEAN = 6.0328070175
UNEMPLOYMENT_SCALE = 1.7714284596
UNEMPLOYMENT_COEF = -0.3750787000

YIELD_MEAN = 0.8460836333
YIELD_SCALE = 0.9305186587
YIELD_COEF = -1.6932924103

CLAIMS_MEAN = 379581.4035087719
CLAIMS_SCALE = 264814.6457624858
CLAIMS_COEF = -0.0249181030

INDUSTRIAL_MEAN = 2.0152720750
INDUSTRIAL_SCALE = 4.3947284085
INDUSTRIAL_COEF = -0.2908922102

INTERCEPT = -2.9270269913

WARNING_THRESHOLD = 35.0


# ============================================================
# FRED DOWNLOAD
# ============================================================

session = requests.Session()


def fetch_series(
    series_id,
    start_date=START_DATE
):

    params = {
        "series_id":
            series_id,

        "api_key":
            API_KEY,

        "file_type":
            "json",

        "observation_start":
            start_date
    }


    for attempt in range(5):

        response = session.get(
            BASE_URL,
            params=params,
            timeout=30
        )


        if response.status_code == 200:

            payload = response.json()

            rows = []


            for item in payload.get(
                "observations",
                []
            ):

                if item["value"] == ".":
                    continue


                rows.append({
                    "date":
                        pd.Timestamp(
                            item["date"]
                        ),

                    "value":
                        float(
                            item["value"]
                        )
                })


            result = pd.DataFrame(rows)

            result = result.sort_values(
                "date"
            ).reset_index(drop=True)

            print(
                f"{series_id}: "
                f"{len(result)} observations"
            )

            return result


        if response.status_code == 429:

            wait = (
                5 * (attempt + 1)
            )

            print(
                f"Rate limited on "
                f"{series_id}. "
                f"Waiting {wait}s..."
            )

            time.sleep(wait)

            continue


        raise RuntimeError(
            f"FRED request failed for "
            f"{series_id}: "
            f"{response.status_code} "
            f"{response.text[:250]}"
        )


    raise RuntimeError(
        f"Could not retrieve {series_id}"
    )


print(
    "\nDOWNLOADING TRADINGVIEW PROXY DATA"
)

print("=" * 85)


unrate = fetch_series(
    "UNRATE"
)

yield_curve = fetch_series(
    "T10Y2Y"
)

claims = fetch_series(
    "ICSA"
)

indpro = fetch_series(
    "INDPRO"
)


# ============================================================
# TRADINGVIEW-STYLE FEATURES
# ============================================================

# Pine approximation:
# request.security("FRED:T10Y2Y", "D", ta.sma(close, 21))

yield_curve[
    "yield_proxy"
] = (
    yield_curve["value"]
    .rolling(
        21,
        min_periods=21
    )
    .mean()
)


# Pine approximation:
# request.security("FRED:ICSA", "W", ta.sma(close, 4))

claims[
    "claims_proxy"
] = (
    claims["value"]
    .rolling(
        4,
        min_periods=4
    )
    .mean()
)


# Pine approximation:
# request.security(
#     "FRED:INDPRO",
#     "M",
#     (close / close[12] - 1) * 100
# )

indpro[
    "industrial_growth_proxy"
] = (
    (
        indpro["value"]
        /
        indpro["value"].shift(12)
    )
    - 1
) * 100


# ============================================================
# MONTHLY PREDICTION DATES
# ============================================================

today = pd.Timestamp.today().normalize()

latest_completed_month = (
    today.replace(day=1)
    - pd.Timedelta(days=1)
)


prediction_dates = pd.date_range(
    start="1983-12-31",
    end=latest_completed_month,
    freq="ME"
)


rows = []


# ============================================================
# HELPER
# ============================================================

def latest_available(
    frame,
    date,
    column
):

    sample = frame[
        frame["date"] <= date
    ]


    if sample.empty:
        return np.nan


    return float(
        sample.iloc[-1][column]
    )


# ============================================================
# BUILD MONTHLY PROXY
# ============================================================

for prediction_date in prediction_dates:

    previous_month_end = (
        prediction_date
        - pd.offsets.MonthEnd(1)
    )


    unemployment_value = (
        latest_available(
            unrate,
            previous_month_end,
            "value"
        )
    )


    yield_value = (
        latest_available(
            yield_curve,
            previous_month_end,
            "yield_proxy"
        )
    )


    claims_value = (
        latest_available(
            claims,
            previous_month_end,
            "claims_proxy"
        )
    )


    industrial_value = (
        latest_available(
            indpro,
            previous_month_end,
            "industrial_growth_proxy"
        )
    )


    rows.append({
        "observation_date":
            prediction_date,

        "unemployment_proxy":
            unemployment_value,

        "yield_curve_proxy":
            yield_value,

        "claims_proxy":
            claims_value,

        "industrial_growth_proxy":
            industrial_value
    })


proxy = pd.DataFrame(rows)


proxy = proxy.dropna(
    subset=[
        "unemployment_proxy",
        "yield_curve_proxy",
        "claims_proxy",
        "industrial_growth_proxy"
    ]
).reset_index(drop=True)


# ============================================================
# STANDARDIZE
# ============================================================

proxy[
    "z_unemployment"
] = (
    (
        proxy["unemployment_proxy"]
        - UNEMPLOYMENT_MEAN
    )
    /
    UNEMPLOYMENT_SCALE
)


proxy[
    "z_yield"
] = (
    (
        proxy["yield_curve_proxy"]
        - YIELD_MEAN
    )
    /
    YIELD_SCALE
)


proxy[
    "z_claims"
] = (
    (
        proxy["claims_proxy"]
        - CLAIMS_MEAN
    )
    /
    CLAIMS_SCALE
)


proxy[
    "z_industrial"
] = (
    (
        proxy["industrial_growth_proxy"]
        - INDUSTRIAL_MEAN
    )
    /
    INDUSTRIAL_SCALE
)


# ============================================================
# FROZEN LOGISTIC MODEL
# ============================================================

proxy[
    "log_odds"
] = (
    INTERCEPT
    +
    proxy["z_unemployment"]
    * UNEMPLOYMENT_COEF
    +
    proxy["z_yield"]
    * YIELD_COEF
    +
    proxy["z_claims"]
    * CLAIMS_COEF
    +
    proxy["z_industrial"]
    * INDUSTRIAL_COEF
)


proxy[
    "proxy_probability"
] = (
    1
    /
    (
        1
        +
        np.exp(
            -proxy["log_odds"]
        )
    )
)


proxy[
    "proxy_radar_score"
] = (
    proxy["proxy_probability"]
    * 100
)


proxy[
    "proxy_warning"
] = (
    proxy["proxy_radar_score"]
    >= WARNING_THRESHOLD
).astype(int)


# ============================================================
# SAVE
# ============================================================

proxy.to_csv(
    "data/tradingview_proxy_history.csv",
    index=False
)


# ============================================================
# LATEST PROXY READING
# ============================================================

latest = proxy.iloc[-1]


print(
    "\nLATEST TRADINGVIEW PROXY"
)

print("=" * 85)


print(
    "Observation date:",
    latest[
        "observation_date"
    ].date()
)


print(
    "Unemployment:",
    round(
        latest[
            "unemployment_proxy"
        ],
        4
    )
)


print(
    "Yield proxy:",
    round(
        latest[
            "yield_curve_proxy"
        ],
        4
    )
)


print(
    "Claims proxy:",
    round(
        latest[
            "claims_proxy"
        ],
        2
    )
)


print(
    "Industrial growth proxy:",
    round(
        latest[
            "industrial_growth_proxy"
        ],
        4
    )
)


print(
    "Proxy Radar score:",
    round(
        latest[
            "proxy_radar_score"
        ],
        2
    )
)


print(
    "Proxy warning:",
    "ON"
    if latest[
        "proxy_warning"
    ] == 1
    else "OFF"
)


# ============================================================
# COMPARE WITH OFFICIAL HISTORICAL RADAR
# ============================================================

official = pd.read_csv(
    "data/recession_radar_history_v1.csv"
)


official[
    "observation_date"
] = pd.to_datetime(
    official[
        "observation_date"
    ]
)


comparison = official.merge(
    proxy[
        [
            "observation_date",
            "proxy_radar_score",
            "proxy_warning"
        ]
    ],
    on="observation_date",
    how="inner"
)


comparison = comparison.dropna(
    subset=[
        "radar_score",
        "proxy_radar_score"
    ]
)


correlation = (
    comparison[
        "radar_score"
    ].corr(
        comparison[
            "proxy_radar_score"
        ]
    )
)


mae = (
    (
        comparison[
            "radar_score"
        ]
        -
        comparison[
            "proxy_radar_score"
        ]
    )
    .abs()
    .mean()
)


warning_agreement = (
    (
        comparison[
            "warning"
        ]
        ==
        comparison[
            "proxy_warning"
        ]
    )
    .mean()
    * 100
)


print(
    "\nPROXY VS OFFICIAL RADAR"
)

print("=" * 85)


print(
    "Common observations:",
    len(comparison)
)


print(
    "Score correlation:",
    f"{correlation:.4f}"
)


print(
    "Mean absolute score difference:",
    f"{mae:.2f}"
)


print(
    "Warning-state agreement:",
    f"{warning_agreement:.1f}%"
)


# ============================================================
# OPTIONAL PERFORMANCE
# ============================================================

if (
    "actual"
    in comparison.columns
    and
    comparison[
        "actual"
    ].notna().sum() > 0
):

    labelled = comparison.dropna(
        subset=["actual"]
    ).copy()


    if (
        labelled[
            "actual"
        ].nunique()
        >= 2
    ):

        proxy_roc = roc_auc_score(
            labelled[
                "actual"
            ],
            labelled[
                "proxy_radar_score"
            ]
        )


        proxy_pr = (
            average_precision_score(
                labelled[
                    "actual"
                ],
                labelled[
                    "proxy_radar_score"
                ]
            )
        )


        print()

        print(
            "Proxy ROC-AUC:",
            f"{proxy_roc:.4f}"
        )


        print(
            "Proxy PR-AUC:",
            f"{proxy_pr:.4f}"
        )


print(
    "\nSaved to:"
)

print(
    "data/tradingview_proxy_history.csv"
)