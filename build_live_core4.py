import os
import sys
import time
import requests
import pandas as pd


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


# ============================================================
# DATE
# ============================================================

def get_prediction_date():

    # Optional:
    # python build_live_core4.py 2025-06-30

    if len(sys.argv) > 1:

        date = pd.Timestamp(
            sys.argv[1]
        )

        return date


    # Otherwise use latest COMPLETED calendar month-end

    today = pd.Timestamp.today().normalize()

    first_day_current_month = (
        today.replace(day=1)
    )

    latest_completed_month = (
        first_day_current_month
        - pd.Timedelta(days=1)
    )

    return latest_completed_month


prediction_date = get_prediction_date()


# ============================================================
# PREVIOUS CALENDAR MONTH
# ============================================================

previous_month_end = (
    prediction_date
    - pd.offsets.MonthEnd(1)
)

previous_month_start = (
    previous_month_end
    .replace(day=1)
)


year_ago_month_end = (
    previous_month_end
    - pd.DateOffset(years=1)
)

year_ago_month_start = (
    year_ago_month_end
    .replace(day=1)
)


# ============================================================
# FRED REQUEST FUNCTION
# ============================================================

session = requests.Session()


def fetch_series(
    series_id,
    observation_start,
    observation_end,
    realtime_date
):

    params = {
        "series_id":
            series_id,

        "api_key":
            API_KEY,

        "file_type":
            "json",

        "observation_start":
            observation_start.strftime(
                "%Y-%m-%d"
            ),

        "observation_end":
            observation_end.strftime(
                "%Y-%m-%d"
            ),

        "realtime_start":
            realtime_date.strftime(
                "%Y-%m-%d"
            ),

        "realtime_end":
            realtime_date.strftime(
                "%Y-%m-%d"
            )
    }


    for attempt in range(5):

        response = session.get(
            BASE_URL,
            params=params,
            timeout=30
        )


        if response.status_code == 200:

            payload = response.json()

            observations = (
                payload.get(
                    "observations",
                    []
                )
            )


            rows = []

            for observation in observations:

                value = observation[
                    "value"
                ]

                if value == ".":
                    continue


                rows.append({
                    "date":
                        pd.Timestamp(
                            observation["date"]
                        ),

                    "value":
                        float(value)
                })


            return pd.DataFrame(rows)


        if response.status_code == 429:

            wait = 5 * (
                attempt + 1
            )

            print(
                f"Rate limited. Waiting {wait} seconds..."
            )

            time.sleep(wait)

            continue


        raise RuntimeError(
            f"FRED request failed: "
            f"{response.status_code} "
            f"{response.text[:300]}"
        )


    raise RuntimeError(
        f"Could not retrieve {series_id}"
    )


# ============================================================
# UNEMPLOYMENT
# ============================================================

unemployment_data = fetch_series(
    "UNRATE",
    previous_month_start,
    previous_month_end,
    prediction_date
)


if unemployment_data.empty:

    raise RuntimeError(
        "No unemployment observation available."
    )


unemployment_pit = (
    unemployment_data
    .sort_values("date")
    .iloc[-1]["value"]
)


unemployment_source_date = (
    unemployment_data
    .sort_values("date")
    .iloc[-1]["date"]
)


# ============================================================
# INDUSTRIAL PRODUCTION — SAME VINTAGE YoY
# ============================================================

indpro_latest = fetch_series(
    "INDPRO",
    previous_month_start,
    previous_month_end,
    prediction_date
)


indpro_year_ago = fetch_series(
    "INDPRO",
    year_ago_month_start,
    year_ago_month_end,
    prediction_date
)


if (
    indpro_latest.empty
    or indpro_year_ago.empty
):

    raise RuntimeError(
        "Could not construct industrial production growth."
    )


indpro_latest_row = (
    indpro_latest
    .sort_values("date")
    .iloc[-1]
)


indpro_year_ago_row = (
    indpro_year_ago
    .sort_values("date")
    .iloc[-1]
)


indpro_latest_value = (
    indpro_latest_row["value"]
)

indpro_year_ago_value = (
    indpro_year_ago_row["value"]
)


industrial_growth_pit = (
    (
        indpro_latest_value
        /
        indpro_year_ago_value
    )
    - 1
) * 100


# ============================================================
# INITIAL CLAIMS
# Previous calendar month's weekly observations
# ============================================================

claims_data = fetch_series(
    "ICSA",
    previous_month_start,
    previous_month_end,
    prediction_date
)


if claims_data.empty:

    raise RuntimeError(
        "No claims observations available."
    )


claims_pit = (
    claims_data["value"].mean()
)


claims_weeks_used = (
    len(claims_data)
)


# ============================================================
# 10Y–2Y YIELD CURVE
# Previous calendar month's daily observations
# ============================================================

yield_data = fetch_series(
    "T10Y2Y",
    previous_month_start,
    previous_month_end,
    prediction_date
)


if yield_data.empty:

    raise RuntimeError(
        "No yield-curve observations available."
    )


yield_curve_pit = (
    yield_data["value"].mean()
)


yield_days_used = (
    len(yield_data)
)


# ============================================================
# OUTPUT
# ============================================================

output = pd.DataFrame([
    {
        "observation_date":
            prediction_date,

        "source_month":
            previous_month_end,

        "unemployment_source_date":
            unemployment_source_date,

        "unemployment_pit":
            unemployment_pit,

        "yield_curve_pit":
            yield_curve_pit,

        "yield_days_used":
            yield_days_used,

        "claims_pit":
            claims_pit,

        "claims_weeks_used":
            claims_weeks_used,

        "indpro_latest_source_date":
            indpro_latest_row["date"],

        "indpro_latest_value":
            indpro_latest_value,

        "indpro_year_ago_source_date":
            indpro_year_ago_row["date"],

        "indpro_year_ago_value":
            indpro_year_ago_value,

        "industrial_growth_pit":
            industrial_growth_pit
    }
])


if len(sys.argv) > 1:

    output_file = (
        "data/live_core4_validation.csv"
    )

else:

    output_file = (
        "data/live_core4_latest.csv"
    )


output.to_csv(
    output_file,
    index=False
)


print(
    "\nRECESSION RADAR — LIVE CORE-4 FEATURES"
)

print("=" * 90)

print(
    "Prediction date:",
    prediction_date.date()
)

print(
    "Source month:",
    previous_month_end.date()
)


print()

print(
    "Unemployment:",
    round(
        unemployment_pit,
        4
    )
)

print(
    "Yield curve:",
    round(
        yield_curve_pit,
        4
    )
)

print(
    "Initial claims:",
    round(
        claims_pit,
        2
    ),
    f"({claims_weeks_used} weeks)"
)

print(
    "Industrial growth:",
    round(
        industrial_growth_pit,
        4
    )
)


print(
    "\nSaved to:"
)

print(
    output_file
)