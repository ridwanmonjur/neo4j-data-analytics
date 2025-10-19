import pandas as pd
from dotenv import load_dotenv

load_dotenv()
DATA_PATH = os.getenv("DATA_PATH", "./data")

def hdi_transform() -> None:

    hdi_df = pd.read_csv(DATA_PATH + "/HDI.csv")

    all_cols = hdi_df.columns.tolist()

    id_cols = ['iso3', 'country', 'hdicode', 'region', 'hdi_rank_2023']

    metrics = set()
    years = set()

    for col in all_cols:
        if col not in id_cols:
            # Split by last underscore to separate metric from year
            parts = col.rsplit('_', 1)
            if len(parts) == 2 and parts[1].isdigit():
                metrics.add(parts[0])
                years.add(int(parts[1]))

    print(f"Found {len(metrics)} metrics across {len(years)} years")
    print(f"Year range: {min(years)} to {max(years)}")

    # Using pd.wide_to_long (cleaner approach)
    # First, prepare the dataframe by setting the ID columns as index
    hdi_long = pd.wide_to_long(
        hdi_df,
        stubnames=list(metrics),
        i=['iso3', 'country', 'hdicode', 'region', 'hdi_rank_2023'],
        j='year',
        sep='_',
        suffix='\\d+'
    )

    # Reset index to make year a regular column
    hdi_long = hdi_long.reset_index()

    # Rename iso3 to ISO to match disaster data
    hdi_long = hdi_long.rename(columns={'iso3': 'ISO'})

if __name__ == "__main__":
    print("Running HDI transformation...")

