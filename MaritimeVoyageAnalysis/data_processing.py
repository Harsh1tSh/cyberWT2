import pandas as pd
from geopy.distance import geodesic

def process_data(data):
    data['timestamp'] = pd.to_datetime(data['datestamp'], unit='D') + pd.to_timedelta(data['timestamp'], unit='D')


    data['duration'] = data.groupby(['imo_num', 'voyage_id'])['timestamp'].diff().dt.total_seconds()


    data['next_lat'] = data['lat'].shift(-1)
    data['next_lon'] = data['lon'].shift(-1)


    def calculate_distance(row):
        if pd.notna(row['next_lat']) and pd.notna(row['next_lon']):
            coords_1 = (row['lat'], row['lon'])
            coords_2 = (row['next_lat'], row['next_lon'])
            return geodesic(coords_1, coords_2).miles * 0.868976  # Convert miles to nautical miles
        return None

    # Calculate distances
    data['distance_nm'] = data.apply(calculate_distance, axis=1)

    return data

if __name__ == "__main__":
    #test
    import numpy as np
    df = pd.DataFrame({
        'datestamp': [43831, 43831, 43832, 43832],
        'timestamp': np.random.rand(4),
        'lat': [34.0522, 34.0522, 36.7783, 36.7783],
        'lon': [-118.2437, -118.2437, -119.4179, -119.4179],
        'imo_num': ['9434761', '9434761', '9434761', '9434761'],
        'voyage_id': ['6', '6', '6', '6']
    })
    processed_data = process_data(df)
    print(processed_data)
    processed_data.to_csv('processed_data.csv', index=False)
