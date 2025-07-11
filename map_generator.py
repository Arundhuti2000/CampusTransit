import folium
import os
import pandas as pd
from data_processor import load_gtfs_data

def generate_mbta_map(stops_df, routes_df, trips_df, shapes_df, output_file='mbta_static_map.html'):
    if stops_df is None or routes_df is None or trips_df is None or shapes_df is None:
        print("Error: One or more required DataFrames are missing or None. Cannot generate map.")
        return
    print("\nCreating the interactive map...")
    m = folium.Map(location=[42.3601, -71.0589], zoom_start=12)
    print("Adding bus stops to the map...")
    # Iterating through a DataFrame is possible, but for large datasets,
    # We'll limit the number of stops to plot initially to avoid overwhelming the map and your browser if you have tens of thousands of stops.
    # Let's plot the first 1000 stops or so for a start.
    num_stops_to_plot = min(1000, len(stops_df)) # Plot max 1000 or all if less
    for index, row in stops_df.head(num_stops_to_plot).iterrows():
        folium.Marker(
            location=[row['stop_lat'], row['stop_lon']],
            popup=row['stop_name'],
            tooltip=row['stop_name']
        ).add_to(m)
    print(f"Added {num_stops_to_plot} bus stops.")

    print("Adding bus routes (shapes) to the map...")
    route_1_info = routes_df[routes_df['route_short_name'] == '1']

    if not route_1_info.empty:
        route_1_id = route_1_info.iloc[0]['route_id']
        print(f"Found Route '1' with route_id: {route_1_id}")

        route_1_trips = trips_df[trips_df['route_id'] == route_1_id]
        unique_shape_ids = route_1_trips['shape_id'].unique()
        print(f"Found {len(unique_shape_ids)} unique shapes for Route '1'. Plotting up to 5.")

        shapes_plotted_count = 0
        for shape_id in unique_shape_ids:
            if shapes_plotted_count >= 5:
                break

            current_shape_data = shapes_df[shapes_df['shape_id'] == shape_id].sort_values(by='shape_pt_sequence')
            if not current_shape_data.empty:
                points = current_shape_data[['shape_pt_lat', 'shape_pt_lon']].values.tolist()
                folium.PolyLine(
                    locations=points,
                    color='red',
                    weight=3,
                    opacity=0.05, # Making it slightly transparent so we can see other lines if they overlap
                    tooltip=f"Route 1 Shape (ID: {shape_id})"
                ).add_to(m)
                shapes_plotted_count += 1
        print(f"Plotted {shapes_plotted_count} shapes for Route '1'.")
    else:
        print("Route '1' not found in routes.txt. Cannot plot its shapes.")
        m.save(output_file)
    print(f"\nInteractive map saved to {output_file}")
    print("Open this HTML file in your web browser to view the map.")
if __name__ == "__main__":
    print("Running map_generator.py directly to create map...")
    # Call the load_gtfs_data function to get the DataFrames
    stops_df, routes_df, trips_df, shapes_df = load_gtfs_data()

    # Then, pass these DataFrames to the map generation function
    generate_mbta_map(stops_df, routes_df, trips_df, shapes_df)
