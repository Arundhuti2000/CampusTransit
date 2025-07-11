import pandas as pd
import os

#load data from GTFS files into pandas dataframes
def load_gtfs_data(extract_dir='MBTA_GFTS'):
    print("Loading data into Pandas DataFrames...")
    stops_df = routes_df = trips_df = shapes_df = None
    try:
        stops_df = pd.read_csv(os.path.join(extract_dir, 'stops.txt'))
        routes_df = pd.read_csv(os.path.join(extract_dir, 'routes.txt'))
        trips_df = pd.read_csv(os.path.join(extract_dir, 'trips.txt'))
        shapes_df = pd.read_csv(os.path.join(extract_dir, 'shapes.txt'))
        print("All required static data loaded successfully!")
    except FileNotFoundError as e:
        print(f"Error loading a GTFS file: {e}. Make sure the file exists in the extracted directory.")
    except pd.errors.EmptyDataError as e:
        print(f"Error: {e}. One of the GTFS files is empty.")
    except Exception as e:
        print(f"An unexpected error occurred while loading data: {e}")

    return stops_df, routes_df, trips_df, shapes_df




if __name__ == "__main__":
    print("Running data_processor.py directly to test data loading...")
    stops, routes, trips, shapes = load_gtfs_data()
    if stops is not None:
        print("\nStops DataFrame head:")
        print(stops.head())