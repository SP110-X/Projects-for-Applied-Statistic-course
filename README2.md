# Hanwha Life Esports (HLE) — League of Legends Performance Analysis (2024 vs 2025)

A statistical analysis comparing Hanwha Life Esports' competitive performance between the 2024 and 2025 League of Legends esports seasons, using descriptive statistics and two-proportion z-tests.

## Overview

This project analyzes match-level data for Hanwha Life Esports (HLE) across the 2024 and 2025 seasons to determine whether the team's win rates changed meaningfully year over year, broken down by side (Blue/Red) and series format (Best-of-3 vs Best-of-5).

## Methodology

1. **Data Combination** — Merges the 2024 and 2025 raw esports datasets, filtering for HLE's games and assigning a `series_id` to group games into series.
2. **Descriptive Statistics** — Computes overall win rate, win rate by side (Blue/Red), and win rate by series format (BO3/BO5) for each year.
3. **Visualization** — Generates bar charts and line plots comparing win rates across years and categories.
4. **Hypothesis Testing** — Runs two-proportion z-tests to check whether differences between 2024 and 2025 are statistically significant.

## Key Findings

- **Overall win rate** rose from 66.9% (2024) to 72.6% (2025), but the change is **not statistically significant** (p = 0.40).
- **Blue side win rate**: 70.6% (2024) → 75.0% (2025) — not significant (p = 0.63).
- **Red side win rate**: 63.2% (2024) → 72.2% (2025) — not significant (p = 0.36).
- **Blue–Red side advantage** widened from a 7.4-point gap in 2024 to a 16.8-point gap in 2025, but this increase is not statistically significant (p = 0.47).
- **BO3 series win rate**: 69.6% (2024) → 85.0% (2025) — not significant (p = 0.19).
- **BO5 series win rate**: 62.5% (2024) → 100% (2025) — **marginally significant** (p = 0.09), though based on a very small sample (8 and 6 series respectively).
- Across nearly all comparisons, observed performance improvements in 2025 were **not statistically significant at the 5% level**, mainly due to limited sample sizes (especially for BO5 series).

## Files

| File | Description |
|---|---|
| `group_10_final_notebook.ipynb` | Main analysis notebook |
| `2024_LoL_esports.csv` | Raw 2024 season match data |
| `2025_LoL_esports.csv` | Raw 2025 season match data |
| `HLE_Combined_With_SeriesID.csv` | Cleaned/combined dataset with series IDs |
| `HLE_Descriptive_Stats.csv` | Year-by-year summary statistics |

## Requirements

```
pandas
numpy
matplotlib
scipy
statsmodels
```

Install with:
```bash
pip install pandas numpy matplotlib scipy statsmodels
```

## How to Run

Open `group_10_final_notebook.ipynb` in Jupyter Notebook / JupyterLab and run all cells in order.

**Note:** the notebook currently uses absolute file paths (e.g. `C:\MAIN\UNI\...`) for loading data and saving plots. To run it on another machine, update these paths to point to wherever you've placed the CSV files (ideally relative paths, e.g. `data/2024_LoL_esports.csv`).

## Context

This project was developed as part of a university course in Applied Statistics ("Εφαρμοσμένη Στατιστική").
