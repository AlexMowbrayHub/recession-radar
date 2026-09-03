# Recession Radar

Recession Radar is a Python-based early-warning system designed to identify periods of elevated risk that a US recession will begin within the following 12 months.

The project combines macroeconomic data from FRED and ALFRED with an interpretable logistic-regression model and a point-in-time-aware historical evaluation framework.

## Current Reading

**Radar Score: 17.0 / 100**

**Signal: Normal range**

**Warning: OFF**

Latest observation: August 2026.

The warning threshold is 35.

The Radar score is a model score and should not be interpreted as a calibrated probability of recession.

---

## Core Indicators

Recession Radar uses four macroeconomic indicators:

- US unemployment rate
- 10-year minus 2-year Treasury yield spread
- Initial unemployment claims
- Industrial production year-over-year growth

These variables capture labour-market conditions, the yield curve and real economic activity.

---

## Methodology

The target equals 1 when an NBER recession begins within the following 12 months and 0 otherwise.

The benchmark model uses:

- StandardScaler
- Logistic Regression
- Expanding walk-forward evaluation
- A temporal purge between training and test observations
- Point-in-time-aware macroeconomic data where available

The historical model is evaluated using information designed to approximate what would have been available at each prediction date.

---

## Historical Performance

Point-in-time-aware walk-forward performance:

**ROC-AUC: 0.8482**

**PR-AUC: 0.2562**

Year-block bootstrap 95% intervals:

- ROC-AUC: 0.7542–0.9356
- PR-AUC: 0.0965–0.5012

The warning threshold of **0.35** was selected using pre-2005 development data.

Post-2005 evaluation:

- ROC-AUC: 0.8151
- PR-AUC: 0.2243
- Precision: 0.3208
- Recall: 0.7083
- F1: 0.4416

---

## Historical Recession Signals

In the post-2005 evaluation period, the model generated warning signals ahead of both recession starts:

- 2008 recession: earliest warning 12 months before recession start
- 2020 recession: earliest warning 11 months before recession start

This represents only two recession events and should not be interpreted as evidence of universal recession-detection ability.

---

## Known Failure Regime

Recession Radar produced a prolonged false-warning regime between 2022 and 2024.

Analysis indicated that the signal was driven primarily by the unusually deep yield-curve inversion.

Alternative specifications were tested, including labour-market confirmation variables, momentum features, credit spreads and a nonlinear gradient-boosting model.

These alternatives were rejected when they failed to improve overall out-of-sample performance or introduced additional overfitting risk.

The original Core-4 specification was therefore retained.

---

## Live System

The deployment pipeline:

1. Retrieves current macroeconomic data.
2. Constructs the same four features used by the historical model.
3. Loads the frozen Core-4 model.
4. Generates the current Radar score.
5. Calculates the score's historical percentile.
6. Identifies the largest model drivers.
7. Updates the historical output files.

The complete live system can be run with:

```bash
python update_radar.py

## TradingView Asset Context

The TradingView version of Recession Radar includes an experimental cross-asset context layer.

When the recession-warning regime is active, the dashboard displays historical tendencies observed after Radar warning activations:

- Gold: defensive bias
- Oil: vulnerable
- Large-cap equities: relative strength versus small caps

These relationships are based on a small number of independent warning events and are therefore labelled **limited evidence**.

They are not direct buy or sell signals.