import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis, ttest_rel, ttest_ind
from pathlib import Path

file_path = Path("C:/Users/camjh/downloads/INFO 2/archive/players_stats_by_season_full_details.csv")
df = pd.read_csv(file_path)

df.columns = df.columns.str.strip()
for col in ["League", "Stage", "Player", "Season"]:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()

print("Dataset loaded.")
print("Source file:", file_path)
print("Total rows:", len(df))

nba = df[(df["League"] == "NBA") & (df["Stage"] == "Regular_Season")].copy()
print("NBA Regular Season rows:", len(nba))

season_counts = nba.groupby("Player")["Season"].nunique()
total_seasons = season_counts.max()
top_players = sorted(season_counts[season_counts == total_seasons].index.tolist())
player_name = top_players[0]

print("\nPlayer with most seasons:", player_name)
print("Total seasons played:", total_seasons)
if len(top_players) > 1:
    print("Players tied for most seasons:", ", ".join(top_players))

player_df = nba[nba["Player"] == player_name].copy()

# Extract starting year
player_df["SeasonStart"] = player_df["Season"].str.split("-").str[0].astype(int)

# Remove zero attempts
player_df = player_df[player_df["3PA"] > 0]

# Compute accuracy
player_df["ThreePointAccuracy"] = player_df["3PM"] / player_df["3PA"]

player_df = player_df.sort_values("SeasonStart")

print("\n3-Point Accuracy by Season:")
print(player_df[["SeasonStart", "ThreePointAccuracy"]])

x = player_df["SeasonStart"].values
y = player_df["ThreePointAccuracy"].values

# Compute slope (m) and intercept (b)
x_mean = np.mean(x)
y_mean = np.mean(y)

m = np.sum((x - x_mean) * (y - y_mean)) / np.sum((x - x_mean) ** 2)
b = y_mean - m * x_mean

print("\nLinear Regression Equation:")
print(f"Accuracy = {m:.6f} * Year + {b:.6f}")

# Compute predicted values
y_fit = m * x + b

integrated_avg = np.trapezoid(y_fit, x) / (x.max() - x.min())
actual_avg = np.mean(y)

print("\nModel Average (Integration):", integrated_avg)
print("Actual Average:", actual_avg)
print("Difference:", abs(integrated_avg - actual_avg))

player_interp = player_df.set_index("SeasonStart")

full_range = range(player_interp.index.min(), player_interp.index.max() + 1)
player_interp = player_interp.reindex(full_range)

player_interp["ThreePointAccuracy"] = player_interp["ThreePointAccuracy"].interpolate()

print("\nInterpolated Values:")
if 2002 in player_interp.index:
    print("2002-2003:", player_interp.loc[2002]["ThreePointAccuracy"])
if 2015 in player_interp.index:
    print("2015-2016:", player_interp.loc[2015]["ThreePointAccuracy"])

print("\n--- FGM Statistics ---")
print("Mean:", nba["FGM"].mean())
print("Variance:", nba["FGM"].var())
print("Skew:", skew(nba["FGM"].dropna()))
print("Kurtosis:", kurtosis(nba["FGM"].dropna()))

print("\n--- FGA Statistics ---")
print("Mean:", nba["FGA"].mean())
print("Variance:", nba["FGA"].var())
print("Skew:", skew(nba["FGA"].dropna()))
print("Kurtosis:", kurtosis(nba["FGA"].dropna()))

# Paired (Relational) t-test
t_rel, p_rel = ttest_rel(nba["FGM"], nba["FGA"])

print("\nPaired T-Test (FGM vs FGA)")
print("T-statistic:", t_rel)
print("P-value:", p_rel)

# Independent t-test
t_ind, p_ind = ttest_ind(nba["FGM"], nba["FGA"])

print("\nIndependent T-Test (FGM vs FGA)")
print("T-statistic:", t_ind)
print("P-value:", p_ind)


print("\n You did it!")