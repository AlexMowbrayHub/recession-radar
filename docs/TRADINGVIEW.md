# Recession Radar — TradingView

## Overview

The TradingView implementation of Recession Radar is a live macro-regime indicator based on the frozen Core-4 logistic-regression model.

It is designed to monitor whether US recession-start risk is elevated over a 12-month horizon.

## Current Model Inputs

The model uses:

- US unemployment rate
- 10Y–2Y Treasury yield spread
- Initial unemployment claims
- Industrial production year-over-year growth

## Warning Threshold

The locked warning threshold is:

**Radar Score >= 35**

Crossing above 35 activates the recession-warning regime.

## TradingView Implementation

TradingView reconstructs the frozen model using FRED data available through TradingView.

The live TradingView score closely reproduces the Python deployment score.

The historical TradingView series is not identical to the point-in-time ALFRED backtest because TradingView uses revised historical FRED observations and approximate rolling aggregation.

The Python/ALFRED implementation remains the official historical research benchmark.

## Asset Context

When the warning regime is active, the dashboard displays experimental historical asset context:

- Gold: defensive bias
- Oil: vulnerable
- Large-cap equities: relative strength versus small caps

The evidence is based on a small number of independent warning episodes and is therefore labelled **LIMITED**.

These are not direct trading instructions.

## Important

The Radar score is not a calibrated recession probability.

Recession Radar is an economic research project and should not be interpreted as investment advice.