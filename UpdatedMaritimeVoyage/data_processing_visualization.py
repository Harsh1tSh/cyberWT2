import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import math


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in kilometers
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance * 0.539957  # Convert km to nautical miles


data = {
    'id': [1, 2, 3, 4],
    'event': ['SOSP', 'EOSP', 'SOSP', 'EOSP'],
    'dateStamp': [43831, 43831, 43832, 43832],
    'timeStamp': [0.708333, 0.791667, 0.333333, 0.583333],
    'voyage_From': ['Port A', 'Port A', 'Port B', 'Port B'],
    'lat': [34.0522, 34.0522, 36.7783, 36.7783],
    'lon': [-118.2437, -118.2437, -119.4179, -119.4179],
    'imo_num': ['9434761', '9434761', '9434761', '9434761'],
    'voyage_Id': ['6', '6', '6', '6'],
    'allocatedVoyageId': [None, None, None, None]
}

df = pd.DataFrame(data)


df['event_utc'] = df.apply(lambda row: datetime(1900, 1, 1) + timedelta(days=row['dateStamp'] - 2) + timedelta(days=row['timeStamp']), axis=1)


df['prev_event'] = df['event'].shift(1)
df['prev_event_utc'] = df['event_utc'].shift(1)
df['prev_lat'] = df['lat'].shift(1)
df['prev_lon'] = df['lon'].shift(1)
df['prev_port'] = df['voyage_From'].shift(1)


df['sailing_time'] = df.apply(lambda row: (row['event_utc'] - row['prev_event_utc']).total_seconds() / 3600 if row['event'] == 'SOSP' else None, axis=1)
df['port_stay_duration'] = df.apply(lambda row: (row['event_utc'] - row['prev_event_utc']).total_seconds() / 3600 if row['event'] == 'EOSP' else None, axis=1)
df['distance_travelled'] = df.apply(lambda row: haversine(row['prev_lat'], row['prev_lon'], row['lat'], row['lon']) if row['event'] == 'SOSP' else None, axis=1)


plt.figure(figsize=(12, 6))
plt.plot(df['event_utc'], df['sailing_time'], label='Sailing Time (hours)')
plt.plot(df['event_utc'], df['port_stay_duration'], label='Port Stay Duration (hours)', linestyle='--')
plt.scatter(df['event_utc'], df['distance_travelled'], label='Distance Travelled (nautical miles)', color='r')
plt.xlabel('Event UTC')
plt.ylabel('Duration / Distance')
plt.title('Voyage Timeline and Metrics')
plt.legend()
plt.grid(True)
plt.show()
