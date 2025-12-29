# Wine Review Analysis

This project analyzes wine review data using Python and creates five different visualizations to explore patterns in wine ratings, countries, provinces, varieties, and prices.

## Data Source

The dataset used is **Wine Reviews** from Kaggle:
- **Dataset**: [Wine Reviews](https://www.kaggle.com/datasets/zynicide/wine-reviews) (or search for "winemag-data-130k-v2.csv")
- **File**: `winemag-data-130k-v2.csv`
- **Description**: Contains over 130,000 wine reviews with information about country, province, variety, points (ratings), price, and more

### Downloading the Data

1. Visit the [Kaggle dataset page](https://www.kaggle.com/datasets/zynicide/wine-reviews)
2. Download `winemag-data-130k-v2.csv`
3. Place the CSV file in the `Day08` directory (same folder as `wine_analysis.ipynb`)

## Files

- `wine_analysis.ipynb` - Jupyter notebook containing the data analysis and visualizations
- `winemag-data-130k-v2.csv` - Wine review dataset (must be downloaded from Kaggle)

## Requirements

- **Python 3.8+**
- **Jupyter Notebook** or **JupyterLab** (or any environment that supports `.ipynb` files like VS Code, Cursor)
- **Required Python packages**:
  - `pandas` - for data manipulation
  - `numpy` - for numerical operations
  - `matplotlib` - for creating visualizations

### Installing Requirements

Install the required packages using pip:

```bash
pip install pandas numpy matplotlib jupyter
```

Or if you're using a requirements file:

```bash
pip install -r requirements.txt
```

## How to Run

### Option 1: Using Jupyter Notebook

1. Make sure you have the CSV file in the same directory as the notebook
2. Open a terminal in the `Day08` directory
3. Start Jupyter Notebook:
   ```bash
   jupyter notebook
   ```
4. Open `wine_analysis.ipynb` from the Jupyter interface
5. Run cells sequentially using `Shift+Enter` or the "Run" button

### Option 2: Using VS Code / Cursor

1. Make sure you have the CSV file in the same directory as the notebook
2. Open `wine_analysis.ipynb` in VS Code or Cursor
3. Select a Python kernel/interpreter
4. Run cells individually or run all cells

### Option 3: Using JupyterLab

1. Make sure you have the CSV file in the same directory as the notebook
2. Open a terminal in the `Day08` directory
3. Start JupyterLab:
   ```bash
   jupyter lab
   ```
4. Open `wine_analysis.ipynb` and run the cells

## Visualizations

The notebook creates five different visualizations:

### Plot 1: Review Counts by Country (Stacked by Rating Bands)
- **Type**: Stacked horizontal bar chart
- **Shows**: Top 20 countries by review count, with reviews stacked by rating bands (80-84, 85-89, 90-94, 95-100 points)
- **Insight**: Identifies which countries have the most wine reviews and how ratings are distributed

### Plot 2: Distribution of Wine Ratings
- **Type**: Bar chart
- **Shows**: Frequency distribution of wine rating points across all reviews
- **Insight**: Reveals the overall distribution pattern of wine ratings

### Plot 3: Points Distribution by Province
- **Type**: Violin plot
- **Shows**: Distribution of rating points for the top 15 provinces (by number of reviews)
- **Insight**: Compares rating distributions across different wine-producing provinces

### Plot 4: Average Points by Wine Variety
- **Type**: Horizontal bar chart with error bars
- **Shows**: Average rating points for the top 20 wine varieties, with standard deviation error bars
- **Insight**: Identifies which wine varieties tend to receive higher ratings

### Plot 5: Province Price Distribution by Country
- **Type**: Box plot with jittered scatter overlay
- **Shows**: Distribution of average province prices within the top 10 countries (log scale)
- **Insight**: Compares price distributions across countries and shows price variability within each country

## Data Cleaning

The notebook performs the following data cleaning steps:

- Removes the "Unnamed: 0" column if present
- Fills missing values in categorical columns (`country`, `province`, `variety`) with "Unknown"
- Converts `points` and `price` columns to numeric format
- Filters out invalid data points as needed for each visualization

## Notes

- The notebook uses `%matplotlib inline` to display plots directly in the notebook
- All plots are saved inline and will appear below their respective code cells when executed
- Some visualizations filter data (e.g., top N countries/provinces) to improve readability
- The price visualization uses a logarithmic scale to better show price differences

## Troubleshooting

**Issue**: "FileNotFoundError" when loading the CSV
- **Solution**: Make sure `winemag-data-130k-v2.csv` is in the same directory as the notebook

**Issue**: Plots not displaying
- **Solution**: Make sure you've run the first cell with `%matplotlib inline` before running plotting cells

**Issue**: Missing packages
- **Solution**: Install required packages using `pip install pandas numpy matplotlib jupyter`

