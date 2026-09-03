# Recession Radar — Model Card

## Version
Research model: Core-4 v1.0 candidate

## Objective
Estimate the relative risk that a US recession will begin within the next 12 months.

The model output is a Radar score and should not be interpreted as a calibrated probability of recession.

## Model
Logistic regression with StandardScaler.

## Core Indicators
1. Unemployment rate
2. 10Y–2Y Treasury yield spread
3. Initial unemployment claims
4. Industrial production year-over-year growth

## Target
1 if an NBER recession begins within the following 12 months.
0 otherwise.

## Validation
Expanding walk-forward evaluation.

Training observations are separated from each test observation to reduce forward-label overlap.

## Data Realism
The model uses point-in-time-aware macroeconomic inputs.

ALFRED vintages are used where practical.

Some historical claims and yield-curve observations predate available archival vintage coverage and therefore use conservative lagged historical fallbacks.

The evaluation should therefore be described as point-in-time-aware rather than perfectly vintage-complete.

## Headline Performance
ROC-AUC: 0.8482
PR-AUC: 0.2562

Year-block bootstrap 95% intervals:

ROC-AUC: 0.7542–0.9356
PR-AUC: 0.0965–0.5012

## Warning Threshold
0.35

Selected using pre-2005 development data.

## Post-2005 Evaluation
ROC-AUC: 0.8151
PR-AUC: 0.2243
Precision: 0.3208
Recall: 0.7083
F1: 0.4416

## Event Performance
2008 recession:
Warning detected 12 months before recession start.

2020 recession:
Warning detected 11 months before recession start.

The post-2005 sample contains only two recession-start events, so event-level detection statistics have substantial uncertainty.

## Major Failure Regime
The model generated a prolonged false-warning regime from July 2022 through October 2024.

The failure was primarily associated with the historically deep yield-curve inversion, combined with the model's treatment of unusually low unemployment as a late-cycle signal.

## Experiments Rejected
- Momentum features
- Sahm-style unemployment feature
- Credit spreads
- Labour-confirmation interactions
- Labour-deterioration replacement model
- Structural yield-curve state model
- Shallow gradient boosting
- 6-month target
- 9-month target
- Warning-duration decay

These alternatives either reduced overall discrimination, increased false alarms, or introduced substantial risk of retrospective overfitting.

## Known Limitations
- Very small number of recession events.
- Performance varies substantially across historical regimes.
- Particularly weak discrimination in the limited 2020s sample.
- Historical vintage coverage is incomplete for some indicators.
- NBER recession labels are retrospective.
- Radar score is not a calibrated recession probability.
- Historical performance does not imply future forecasting accuracy.

## Research Decision
Core-4 is frozen as the benchmark.

Further changes should be evaluated under a new validation protocol rather than optimized against already-inspected historical failure episodes.