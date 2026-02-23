# Assignment-4-scipy
# NBA Player 3PT Accuracy Trend + Shooting Stats (Python)

This script loads a season-by-season basketball dataset, filters to **NBA Regular Season** records, identifies the player(s) with the **most seasons played**, analyzes that player’s **3-point accuracy trend over time** using a simple linear regression, performs **interpolation** for missing seasons, and computes summary statistics and **t-tests** comparing **FGM vs FGA**.

---

## Features

- **Data loading & cleaning**
  - Reads a CSV file using `pandas`
  - Strips whitespace from column names and key string fields (`League`, `Stage`, `Player`, `Season`)
- **NBA Regular Season filter**
  - Filters dataset to: `League == "NBA"` and `Stage == "Regular_Season"`
- **Longest-tenured player detection**
  - Finds player(s) with the maximum number of unique seasons
  - Uses the first player in the sorted tie list for analysis
- **3-Point accuracy by season**
  - Extracts season starting year (e.g., `"2002-2003"` → `2002`)
  - Removes seasons with `3PA == 0` to avoid division-by-zero
  - Computes `ThreePointAccuracy = 3PM / 3PA`
- **Manual linear regression**
  - Computes slope and intercept using the least-squares formula
  - Prints regression equation: `Accuracy = m * Year + b`
- **Model vs actual average**
  - Uses trapezoidal integration on predicted values to estimate the model average
  - Compares against the actual mean accuracy
- **Interpolation across missing years**
  - Reindexes the player’s seasons to a full year range and interpolates missing `ThreePointAccuracy`
  - Prints interpolated values for specific years (2002 and 2015) if they exist in range
- **League-wide shooting stats**
  - Mean, variance, skewness, kurtosis for:
    - `FGM` (Field Goals Made)
    - `FGA` (Field Goals Attempted)
- **Statistical tests**
  - Paired t-test (`ttest_rel`) between `FGM` and `FGA`
  - Independent t-test (`ttest_ind`) between `FGM` and `FGA`



```bash
pip install pandas numpy scipy
```

Dataset / Input
The script expects this CSV file path (currently hard-coded):
```python
file_path = Path("C:/Users/camjh/downloads/INFO 2/archive/players_stats_by_season_full_details.csv")
```
Expected columns (minimum)
The script assumes these columns exist:

- League
- Stage
- Player
- Season (format like YYYY-YYYY)
- 3PM, 3PA
- FGM, FGA
If any of these are missing or named differently, the script will raise a KeyError.

### How to Run
Update the file_path variable to point to your CSV file.
Run:
```
python assignment 4 scipy.py
```

You should see console output including:

-Row counts for total dataset and NBA Regular Season subset
- Player with most seasons (and ties if applicable)
- 3PT accuracy per season for that player
- Linear regression equation + average comparisons
- Interpolated accuracy values (if within the player’s year range)
- Summary statistics for FGM/FGA
- Paired and independent t-test results
- Output (Console)
The script prints:

- Dataset load summary
- NBA Regular Season row count
- Player(s) with most seasons
- Per-season 3PT accuracy table
-Regression equation coefficients
- Model average vs actual average
- Interpolation examples (2002, 2015 when applicable)
- Descriptive statistics: mean/variance/skew/kurtosis
- T-test results: t-statistic and p-value
### Final message: You did it!
