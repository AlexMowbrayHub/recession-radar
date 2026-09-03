# Recession Radar — Methodology

## 1. Objective

Recession Radar is designed to identify periods in which the risk of a US recession beginning within the following 12 months is elevated.

The model output is referred to as a Radar score.

It is not interpreted as a calibrated probability of recession.

---

## 2. Target

The target equals 1 when an NBER recession begins within the following 12 months and 0 otherwise.

The system predicts recession starts rather than whether the economy is currently in recession.

This distinction matters because observations during an existing recession can technically receive a target value of 0 if another recession does not begin within the following 12 months.

---

## 3. Core Indicators

The frozen Core-4 specification uses:

1. US unemployment rate
2. 10-year minus 2-year Treasury yield spread
3. Initial unemployment claims
4. Industrial production year-over-year growth

The model is implemented using StandardScaler and logistic regression.

---

## 4. Point-in-Time Data

A major objective of the project was reducing hindsight bias from revised macroeconomic data.

Where practical, ALFRED vintage observations were used to approximate what an analyst could have observed at each historical prediction date.

### Unemployment

Historical vintage unemployment observations are used with publication timing taken into account.

### Industrial Production

Year-over-year industrial production growth is calculated using values from the same historical vintage rather than combining observations from different revision dates.

### Initial Claims

ALFRED vintage data is used where archival coverage is available.

For earlier periods without complete archival vintage coverage, a conservative lagged historical fallback is used.

### Yield Curve

Historical point-in-time observations are used where vintage coverage is available.

Earlier observations use a conservative lagged historical fallback.

The resulting dataset is therefore described as **point-in-time-aware**, not perfectly vintage-complete.

---

## 5. Validation

Performance is evaluated using expanding walk-forward testing rather than a random train/test split.

For each historical test date:

1. Only earlier observations are used for model training.
2. A temporal separation is applied to reduce overlap between the 12-month forward target and the test period.
3. The model is retrained.
4. A prediction is generated for the next historical observation.

This better approximates a real forecasting process than randomly mixing historical observations.

---

## 6. Headline Performance

Point-in-time-aware Core-4 walk-forward results:

- ROC-AUC: 0.8482
- PR-AUC: 0.2562

Year-block bootstrap 95% intervals:

- ROC-AUC: 0.7542–0.9356
- PR-AUC: 0.0965–0.5012

The wide intervals reflect the small number of historical US recession events.

---

## 7. Warning Threshold

A warning threshold of 0.35 was selected using the development period ending in December 2004.

The threshold was then locked before evaluation on the post-2005 period.

Post-2005 results:

- ROC-AUC: 0.8151
- PR-AUC: 0.2243
- Precision: 0.3208
- Recall: 0.7083
- F1: 0.4416

---

## 8. Recession Event Results

Within the post-2005 evaluation period:

### 2008 recession

Earliest model warning occurred 12 months before recession start.

### 2020 recession

Earliest model warning occurred 11 months before recession start.

Only two recession-start events occur in this evaluation period, so these results have substantial statistical uncertainty.

---

## 9. 2022–2024 Failure Regime

The largest historical model failure was a prolonged warning regime between July 2022 and October 2024.

Feature-contribution analysis showed that the deeply inverted yield curve was the dominant driver.

The model also historically learned a negative unemployment coefficient, meaning unusually low unemployment can contribute positively to a late-cycle recession-risk score.

The episode demonstrates that prolonged yield-curve inversion does not necessarily imply that a recession will begin within 12 months.

---

## 10. Alternative Specifications Tested

Several alternatives were evaluated.

### Momentum features

Unemployment and claims momentum features reduced overall model performance.

Decision: rejected.

### Sahm-style unemployment feature

The additional labour-market deterioration feature did not improve matched-sample discrimination.

Decision: rejected.

### Credit spreads

Adding a corporate credit spread materially reduced ROC-AUC and PR-AUC.

Decision: rejected.

### Labour deterioration specification

Replacing raw labour-market levels reduced the 2022–2024 score but deteriorated post-2005 performance and increased false alarms.

Decision: rejected.

### Structural yield-curve models

Models incorporating inversion state, inversion depth and confirmation interactions reduced model discrimination substantially.

Decision: rejected.

### Gradient boosting

A shallow gradient-boosting model produced materially weaker ROC-AUC and PR-AUC than logistic regression.

Decision: rejected.

### Alternative target horizons

6-month and 9-month targets reduced the 2022–2024 score but also materially weakened overall predictive performance.

The 12-month horizon was retained.

### Warning decay

Very long warnings performed poorly after 2005, but this relationship was not present in the pre-2005 development data.

Adding warning decay would therefore risk fitting specifically to the already-inspected 2022–2024 episode.

Decision: rejected.

---

## 11. Model Freeze

After robustness testing, Core-4 was frozen rather than continually modified to improve historical backtests.

Further model development should use a new model-selection protocol rather than repeatedly optimizing against already-inspected historical episodes.

---

## 12. Live Deployment

The deployment system:

1. Retrieves current FRED/ALFRED data.
2. Uses the previous completed calendar month.
3. Reconstructs the four model inputs using the same definitions used historically.
4. Loads the frozen Core-4 model.
5. Generates the live Radar score.
6. Calculates historical context and feature contributions.

Historical pipeline replication was validated against June 2025.

All four reconstructed features matched the stored historical point-in-time values exactly.

Maximum absolute difference: 0.0.

---

## 13. Current Reading

As of the August 2026 observation:

- Radar score: 17.0
- Warning threshold: 35
- Warning state: OFF
- Historical percentile: 62.7th

The reading is above the historical median but below the predictive warning threshold.

---

## 14. Limitations

Important limitations include:

- Very few historical US recession events
- Regime-dependent model performance
- Particularly weak discrimination in the limited 2020s sample
- Incomplete historical vintage availability for some indicators
- Retrospective NBER recession dating
- A major false-positive episode during 2022–2024
- Model scores are not calibrated recession probabilities
- Historical performance does not guarantee future forecasting performance