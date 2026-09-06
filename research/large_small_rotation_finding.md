# Recession Radar — Large vs Small Cap Rotation Finding

## Status

Frozen exploratory research finding.

This relationship is used as historical market context only.
It is not a trading signal or investment recommendation.

## Definition

Relative equity performance is defined as:

S&P 500 forward return minus Russell 2000 forward return.

Positive values indicate large-cap outperformance.
Negative values indicate small-cap outperformance.

## Core Finding

Higher Recession Radar scores have historically been associated
with stronger subsequent large-cap performance relative to small caps.

Very low Radar scores have historically been associated with
stronger small-cap relative performance.

## Radar Band Results

### 3 months

LOW:
- Mean large-minus-small: -0.73 percentage points
- Large-cap win rate: 45.6%

WARNING:
- Mean large-minus-small: +2.30 percentage points
- Large-cap win rate: 67.7%

WARNING minus LOW:
+3.04 percentage points

### 6 months

LOW:
- Mean large-minus-small: -1.37 percentage points
- Large-cap win rate: 42.1%

WARNING:
- Mean large-minus-small: +4.48 percentage points
- Large-cap win rate: 76.3%

WARNING minus LOW:
+5.85 percentage points

### 12 months

LOW:
- Mean large-minus-small: -2.37 percentage points
- Large-cap win rate: 37.7%

WARNING:
- Mean large-minus-small: +4.56 percentage points
- Large-cap win rate: 74.2%

WARNING minus LOW:
+6.93 percentage points

## Continuous Score Relationship

Full-sample 12-month relationship:

- Pearson correlation: +0.266
- Spearman correlation: +0.330

Higher Radar scores therefore correspond historically with
greater subsequent large-cap relative performance.

## Non-Overlapping Robustness Test

Twelve independent sampling offsets were tested using
non-overlapping 12-month forward return windows.

Results:

- Average Pearson correlation: +0.282
- Average Spearman correlation: +0.328
- Positive Pearson correlations: 12 / 12
- Positive Spearman correlations: 12 / 12

This materially reduces concern that the relationship is merely
an artefact of overlapping forward-return windows.

## Era Robustness

2000 onward:
- Pearson: +0.243
- Spearman: +0.217
- WARNING minus LOW: +5.43 percentage points

2006 onward:
- Pearson: +0.230
- Spearman: +0.299
- WARNING minus LOW: +5.19 percentage points

2010 onward:
- Pearson: +0.175
- Spearman: +0.278
- WARNING minus LOW: +3.77 percentage points

The relationship weakens somewhat in magnitude in the newest
sample but remains positive.

## Outside Recessions

When actual NBER recession months are excluded:

- Observations: 407
- Pearson correlation: +0.299
- Spearman correlation: +0.361
- LOW mean: -2.05 percentage points
- WARNING mean: +5.45 percentage points
- WARNING minus LOW: +7.50 percentage points

Therefore, the relationship is not simply a mechanical consequence
of observations occurring during recessions.

## Statistical Testing

Permutation tests comparing WARNING and LOW regimes produced
no random samples as extreme as the observed differences in
10,000 simulations at the 3-, 6-, and 12-month horizons.

This should be described as approximately:

empirical p < 0.0001

rather than p = 0.

Monthly observations remain serially dependent, which is why
non-overlapping robustness tests are also reported.

## Important Limitations

This research was conducted after development of Recession Radar
and therefore constitutes exploratory, not untouched out-of-sample,
evidence.

The result does not establish causality.

Historical relationships may not persist in future markets.

Recession Radar should therefore present this information as
historical market context rather than a trading recommendation.

## Approved Interpretation

Higher historical Recession Radar readings have been associated
with relative strength in large-cap equities versus small caps.

Lower Radar readings have historically been more favourable to
small-cap relative performance.