# coding: utf-8
# Converted from group_10_final_notebook.ipynb

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from statsmodels.stats.proportion import proportions_ztest

# Load cleaned dataset with series_id
file_path = r"C:\MAIN\UNI\UNI 4TH\Efarm_stat\Git-Up\HLE_Combined_With_SeriesID.csv"
df = pd.read_csv(file_path)

# Convert date to datetime
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Define manual BO5 dates (for 2025 only)
manual_bo5_dates = [
    "2025-02-13", "2025-02-16", "2025-02-19",
    "2025-02-23", "2025-03-15", "2025-03-16"
]

# Initialize summary list
summary = []

# Process for both years
for year in [2024, 2025]:
    data = df[df["year"] == year].copy()

    total_games = len(data)
    total_wins = data["result"].sum()
    overall_win_rate = total_wins / total_games * 100 if total_games > 0 else 0

    # Sides
    blue = data[data["side"] == "Blue"]
    red = data[data["side"] == "Red"]
    blue_wins = blue["result"].sum()
    red_wins = red["result"].sum()
    blue_win_rate = blue_wins / len(blue) * 100 if len(blue) > 0 else 0
    red_win_rate = red_wins / len(red) * 100 if len(red) > 0 else 0

    # BO5 classification
    data["bo5_series"] = data.apply(
        lambda row: row["playoffs"] or
        (row["year"] == 2025 and row["date"].strftime("%Y-%m-%d") in manual_bo5_dates),
        axis=1
    )

    # Series
    bo3 = data[data["bo5_series"] == False].groupby("series_id")["result"].sum()
    bo5 = data[data["bo5_series"] == True].groupby("series_id")["result"].sum()

    bo3_series = len(bo3)
    bo5_series = len(bo5)
    bo3_wins = (bo3 >= 2).sum()
    bo5_wins = (bo5 >= 3).sum()
    bo3_win_rate = bo3_wins / bo3_series * 100 if bo3_series > 0 else 0
    bo5_win_rate = bo5_wins / bo5_series * 100 if bo5_series > 0 else 0

    summary.append({
        "Year": year,
        "Total Games": total_games,
        "Total Wins": int(total_wins),
        "Overall Win Rate (%)": round(overall_win_rate, 2),
        "Blue Side Wins": int(blue_wins),
        "Blue Side Win Rate (%)": round(blue_win_rate, 2),
        "Red Side Wins": int(red_wins),
        "Red Side Win Rate (%)": round(red_win_rate, 2),
        "BO3 Series": bo3_series,
        "BO3 Series Wins": bo3_wins,
        "BO3 Series Win Rate (%)": round(bo3_win_rate, 2),
        "BO5 Series": bo5_series,
        "BO5 Series Wins": bo5_wins,
        "BO5 Series Win Rate (%)": round(bo5_win_rate, 2)
    })

# Convert to DataFrame
summary_df = pd.DataFrame(summary)
summary_df.to_csv(r"C:\MAIN\UNI\UNI 4TH\Efarm_stat\HLE_Descriptive_Stats.csv", index=False)
print("✅ Descriptive statistics saved.")

# =======================
# Plot 1: Blue vs Red win rates
# =======================
plt.figure(figsize=(8, 5))
plt.bar(["Blue 2024", "Red 2024", "Blue 2025", "Red 2025"],
        [summary_df.loc[0, "Blue Side Win Rate (%)"],
         summary_df.loc[0, "Red Side Win Rate (%)"],
         summary_df.loc[1, "Blue Side Win Rate (%)"],
         summary_df.loc[1, "Red Side Win Rate (%)"]],
        color=["skyblue", "lightcoral", "skyblue", "lightcoral"])
plt.title("Blue vs Red Side Win Rates by Year")
plt.ylabel("Win Rate (%)")
plt.tight_layout()
plt.savefig(r"C:\MAIN\UNI\UNI 4TH\Efarm_stat\Side_Win_Rates.png")
plt.show()
plt.close()

# =======================
# Plot 2: BO3 vs BO5 win rates
# =======================
plt.figure(figsize=(8, 5))
plt.bar(["BO3 2024", "BO5 2024", "BO3 2025", "BO5 2025"],
        [summary_df.loc[0, "BO3 Series Win Rate (%)"],
         summary_df.loc[0, "BO5 Series Win Rate (%)"],
         summary_df.loc[1, "BO3 Series Win Rate (%)"],
         summary_df.loc[1, "BO5 Series Win Rate (%)"]],
        color=["darkviolet", "gold", "darkviolet", "gold"])
plt.title("BO3 vs BO5 Series Win Rates by Year")
plt.ylabel("Series Win Rate (%)")
plt.tight_layout()
plt.savefig(r"C:\MAIN\UNI\UNI 4TH\Efarm_stat\BO3_BO5_Win_Rates.png")
plt.show()
plt.close()
# =======================
# Plot 3: Blue vs Red gap comparison
# =======================
plt.figure(figsize=(8, 5))
blue_red_gap_2024 = summary_df.loc[0, "Blue Side Win Rate (%)"] - summary_df.loc[0, "Red Side Win Rate (%)"]
blue_red_gap_2025 = summary_df.loc[1, "Blue Side Win Rate (%)"] - summary_df.loc[1, "Red Side Win Rate (%)"]

plt.bar(["2024", "2025"], [blue_red_gap_2024, blue_red_gap_2025], 
        color=["steelblue", "darkorange"])
plt.title("Blue-Red Win Rate Gap by Year")
plt.ylabel("Gap (Blue - Red) %")
plt.axhline(y=0, color='black', linestyle='--', alpha=0.5)  # Reference line at 0
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(r"C:\MAIN\UNI\UNI 4TH\Efarm_stat\Blue_Red_Gap.png")
plt.show()
plt.close()

# =======================
# Plot 4: BO3 vs BO5 gap comparison
# =======================
plt.figure(figsize=(8, 5))
bo3_bo5_gap_2024 = summary_df.loc[0, "BO3 Series Win Rate (%)"] - summary_df.loc[0, "BO5 Series Win Rate (%)"]
bo3_bo5_gap_2025 = summary_df.loc[1, "BO3 Series Win Rate (%)"] - summary_df.loc[1, "BO5 Series Win Rate (%)"]

plt.bar(["2024", "2025"], [bo3_bo5_gap_2024, bo3_bo5_gap_2025], 
        color=["forestgreen", "crimson"])
plt.title("BO3-BO5 Win Rate Gap by Year")
plt.ylabel("Gap (BO3 - BO5) %")
plt.axhline(y=0, color='black', linestyle='--', alpha=0.5)  # Reference line at 0
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(r"C:\MAIN\UNI\UNI 4TH\Efarm_stat\BO3_BO5_Gap.png")
plt.show()
plt.close()

# =======================
# Plot 5: Overall win rate over time
# =======================
plt.figure(figsize=(8, 5))
plt.plot(summary_df["Year"], summary_df["Overall Win Rate (%)"], marker="o", linestyle="-", color="purple")
plt.title("Overall Win Rate Over Time")
plt.ylabel("Win Rate (%)")
plt.xlabel("Year")
plt.grid(True)
plt.tight_layout()
plt.savefig(r"C:\MAIN\UNI\UNI 4TH\Efarm_stat\Overall_Win_Rate.png")
plt.show()
plt.close()

File_descriptive_stats = r"C:\MAIN\UNI\UNI 4TH\Efarm_stat\HLE_Descriptive_Stats.csv" 
stats_df = pd.read_csv(File_descriptive_stats)

stats_df["Game Win"] = stats_df["Total Wins"] / stats_df["Total Games"]
stats_df["Series Win"] = (
    (stats_df["BO3 Series Win Rate (%)"] * stats_df["BO3 Series"] +
     stats_df["BO5 Series Win Rate (%)"] * stats_df["BO5 Series"]) /
    (stats_df["BO3 Series"] + stats_df["BO5 Series"])) / 100

variables = {
    "Series win (BO3 or BO5)": stats_df["Series Win"],
    "Game win": stats_df["Game Win"],
    "Blue Side Win Rate (%)": stats_df["Blue Side Win Rate (%)"],
    "Red Side Win Rate (%)": stats_df["Red Side Win Rate (%)"],
    "BO3 Series Win Rate (%)": stats_df["BO3 Series Win Rate (%)"],
    "BO5 Series Win Rate (%)": stats_df["BO5 Series Win Rate (%)"],
}

print("Descriptive Statistics Table:\n")
for name, series in variables.items():
    print(f"{name}:")
    print(f"  Mean: {series.mean():.2f}")
    print(f"  Std Dev: {series.std():.2f}")
    print(f"  Min: {series.min():.2f}")
    print(f"  Max: {series.max():.2f}\n")

def report_z_test_result(stat, pval, alpha_levels=[0.01, 0.05, 0.10]):
    if pval < alpha_levels[0]:
        return f"❗❗ Statistically significant (p < {alpha_levels[0]:.2f})"
    elif pval < alpha_levels[1]:
        return f"❗ Statistically significant (p < {alpha_levels[1]:.2f})"
    elif pval < alpha_levels[2]:
        return f"⚠️ Marginally significant (p < {alpha_levels[2]:.2f})"
    else:
        return f"✅ Not statistically significant (p ≥ {alpha_levels[2]:.2f})"

def perform_z_test(success_a, nobs_a, success_b, nobs_b, label):
    count = [success_a, success_b]
    nobs = [nobs_a, nobs_b]
    stat, pval = proportions_ztest(count, nobs)
    print(f"{label}:")
    print(f"  Proportion A = {success_a}/{nobs_a} = {success_a/nobs_a:.2%}")
    print(f"  Proportion B = {success_b}/{nobs_b} = {success_b/nobs_b:.2%}")
    print(f"  z-stat = {stat:.3f}, p-value = {pval:.4f}")
    print(report_z_test_result(stat, pval))

# Overall win rate test (2024 vs 2025)
perform_z_test(stats_df.loc[0, "Total Wins"], stats_df.loc[0, "Total Games"],
               stats_df.loc[1, "Total Wins"], stats_df.loc[1, "Total Games"],
               "Overall Win Rate (2024 vs 2025)")

print()  # Line gap

# Blue side win rate test (2024 vs 2025)
perform_z_test(stats_df.loc[0, "Blue Side Wins"], stats_df.loc[0, "Total Games"] // 2,
               stats_df.loc[1, "Blue Side Wins"], stats_df.loc[1, "Total Games"] // 2,
               "Blue Side Win Rate (2024 vs 2025)")

print()  # Line gap

# Red side win rate test (2024 vs 2025)
perform_z_test(stats_df.loc[0, "Red Side Wins"], stats_df.loc[0, "Total Games"] // 2,
               stats_df.loc[1, "Red Side Wins"], stats_df.loc[1, "Total Games"] // 2,
               "Red Side Win Rate (2024 vs 2025)")

print()  # Line gap

# Test: Blue-Red gap change between 2024 and 2025
print("=== Blue-Red Gap Change Statistical Test ===")

# Use already calculated win rates (convert from % to proportions)
p_blue_2024 = stats_df.loc[0, "Blue Side Win Rate (%)"] / 100
p_red_2024 = stats_df.loc[0, "Red Side Win Rate (%)"] / 100
p_blue_2025 = stats_df.loc[1, "Blue Side Win Rate (%)"] / 100
p_red_2025 = stats_df.loc[1, "Red Side Win Rate (%)"] / 100

# Calculate differences
diff_2024 = p_blue_2024 - p_red_2024
diff_2025 = p_blue_2025 - p_red_2025

# Sample sizes (games per side)
n_2024 = stats_df.loc[0, "Total Games"] // 2
n_2025 = stats_df.loc[1, "Total Games"] // 2

# Standard error of difference of differences
se_2024 = ((p_blue_2024 * (1 - p_blue_2024) + p_red_2024 * (1 - p_red_2024)) / n_2024) ** 0.5
se_2025 = ((p_blue_2025 * (1 - p_blue_2025) + p_red_2025 * (1 - p_red_2025)) / n_2025) ** 0.5
se_diff_of_diffs = (se_2024**2 + se_2025**2) ** 0.5

# Z-test
z_stat = (diff_2025 - diff_2024) / se_diff_of_diffs
p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

# Results
print(f"2024: Blue-Red difference = {diff_2024:.3f} ({diff_2024*100:.1f}%)")
print(f"2025: Blue-Red difference = {diff_2025:.3f} ({diff_2025*100:.1f}%)")
print(f"Change in gap = {diff_2025 - diff_2024:.3f} ({(diff_2025 - diff_2024)*100:.1f}%)")
print(f"z-statistic = {z_stat:.3f}, p-value = {p_value:.4f}")

print(report_z_test_result(z_stat, p_value))

if diff_2025 > diff_2024:
    print("📈 Direction: Blue side advantage increased")
elif diff_2025 < diff_2024:
    print("📉 Direction: Blue side advantage decreased")
else:
    print("➡️ Direction: No change in blue-red difference")
print()

print()  # Line gap

# Test: BO3-BO5 gap change between 2024 and 2025
print("=== BO3-BO5 Gap Change Statistical Test ===")

# Use already calculated win rates (convert from % to proportions)
p_bo3_2024 = stats_df.loc[0, "BO3 Series Win Rate (%)"] / 100
p_bo5_2024 = stats_df.loc[0, "BO5 Series Win Rate (%)"] / 100
p_bo3_2025 = stats_df.loc[1, "BO3 Series Win Rate (%)"] / 100
p_bo5_2025 = stats_df.loc[1, "BO5 Series Win Rate (%)"] / 100

# Calculate differences
diff_bo_2024 = p_bo3_2024 - p_bo5_2024
diff_bo_2025 = p_bo3_2025 - p_bo5_2025

# Sample sizes (series counts)
n_bo3_2024 = stats_df.loc[0, "BO3 Series"]
n_bo5_2024 = stats_df.loc[0, "BO5 Series"]
n_bo3_2025 = stats_df.loc[1, "BO3 Series"]
n_bo5_2025 = stats_df.loc[1, "BO5 Series"]

# Standard error of difference of differences
se_bo_2024 = ((p_bo3_2024 * (1 - p_bo3_2024) / n_bo3_2024) + (p_bo5_2024 * (1 - p_bo5_2024) / n_bo5_2024)) ** 0.5
se_bo_2025 = ((p_bo3_2025 * (1 - p_bo3_2025) / n_bo3_2025) + (p_bo5_2025 * (1 - p_bo5_2025) / n_bo5_2025)) ** 0.5
se_diff_of_diffs_bo = (se_bo_2024**2 + se_bo_2025**2) ** 0.5

# Z-test
z_stat_bo = (diff_bo_2025 - diff_bo_2024) / se_diff_of_diffs_bo
p_value_bo = 2 * (1 - stats.norm.cdf(abs(z_stat_bo)))

# Results
print(f"2024: BO3-BO5 difference = {diff_bo_2024:.3f} ({diff_bo_2024*100:.1f}%)")
print(f"2025: BO3-BO5 difference = {diff_bo_2025:.3f} ({diff_bo_2025*100:.1f}%)")
print(f"Change in gap = {diff_bo_2025 - diff_bo_2024:.3f} ({(diff_bo_2025 - diff_bo_2024)*100:.1f}%)")
print(f"z-statistic = {z_stat_bo:.3f}, p-value = {p_value_bo:.4f}")

print(report_z_test_result(z_stat_bo, p_value_bo))

if diff_bo_2025 > diff_bo_2024:
    print("📈 Direction: BO3 advantage over BO5 increased")
elif diff_bo_2025 < diff_bo_2024:
    print("📉 Direction: BO3 advantage over BO5 decreased")
else:
    print("➡️ Direction: No change in BO3-BO5 difference")
print()

print()  # Line gap

# BO3 series win test
perform_z_test(stats_df.loc[0, "BO3 Series Wins"], stats_df.loc[0, "BO3 Series"],
               stats_df.loc[1, "BO3 Series Wins"], stats_df.loc[1, "BO3 Series"],
               "BO3 Series Win Rate (2024 vs 2025)")

print()  # Line gap

# BO5 series win test
perform_z_test(stats_df.loc[0, "BO5 Series Wins"], stats_df.loc[0, "BO5 Series"],
               stats_df.loc[1, "BO5 Series Wins"], stats_df.loc[1, "BO5 Series"],
               "BO5 Series Win Rate (2024 vs 2025)")


def plot_multiple_z_tests(z_stats_dict, title="Z-Test Comparison"):
    x = np.linspace(-4, 4, 1000)
    y = stats.norm.pdf(x, 0, 1)

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, label="Standard Normal Distribution", color="black")

    colors = ['red', 'blue', 'green', 'purple', 'orange', 'brown']
    for i, (label, z_val) in enumerate(z_stats_dict.items()):
        plt.axvline(z_val, color=colors[i % len(colors)], linestyle='--', label=f'{label} (z = {z_val:.2f})')

    plt.fill_between(x, y, where=(x < -1.96) | (x > 1.96), color='gray', alpha=0.1, label="95% Critical Region")
    plt.title(title)
    plt.xlabel("z")
    plt.ylabel("Probability Density")
    plt.legend(loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(r"C:\MAIN\UNI\UNI 4TH\Efarm_stat\Z-test.png")
    plt.show()
z_stats_all = {
    "Overall Win Rate": -0.847,
    "Blue Side Win Rate": -0.477,
    "Red Side Win Rate": -0.923,
    "Blue-Red Gap Change": z_stat,
    "BO3-BO5 Gap Change": z_stat_bo,
    "BO3 Series Win Rate": -1.318,
    "BO5 Series Win Rate": -1.692,
}

plot_multiple_z_tests(z_stats_all, title="Z-Statistics Comparison Across Tests")


