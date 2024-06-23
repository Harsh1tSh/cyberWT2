# Maritime Voyage Analysis

## Project Overview
This project analyzes maritime voyage data to understand patterns and efficiencies in maritime navigations. It involves extracting data from a PostgreSQL database, processing it with Python, and visualizing key metrics.

## Installation
- Install Python 3.8+
- Install PostgreSQL
- Required Python packages: `pandas`, `matplotlib`, `seaborn`, `geopy`, `psycopg2`

## Usage
Run the scripts in the following order:
1. `data_extraction.py`: Extracts data from the database.
2. `data_processing.py`: Processes the data and calculates distances and durations.
3. `data_visualization.py`: Generates visual representations of the processed data.




## Requires more modification and better approaches to handle multiple situations

## Extended Documentation

### Overview
This section provides detailed explanations of the methodologies, assumptions, and calculations used in the `Port & Sail Calculation` project, focusing on how distances are calculated, data is processed, and visualizations are generated.

### Data Extraction (`data_extraction.py`)
The `fetch_data()` function connects to a PostgreSQL database, retrieves data from the `voyages` table using a basic SQL query, and handles any exceptions that occur during this process. It ensures that the connection is closed properly whether the query succeeds or fails.

### Data Processing (`data_processing.py`)
1. **Timestamp Conversion**: Converts the `datestamp` and `timestamp` from the database into a Python datetime format to facilitate time calculations.
2. **Duration Calculation**: Calculates the duration between consecutive events for the same voyage using the pandas `diff()` function applied on the timestamp column grouped by `imo_num` and `voyage_id`.
3. **Distance Calculation**:
    - Utilizes the `geopy.distance.geodesic` function, which calculates the geodesic distance between two points (latitude and longitude) on the Earth's surface.
    - Converts the distance from miles to nautical miles (factor of 0.868976) to align with maritime measurement standards.
    - Applies the calculation row-wise for each pair of consecutive coordinates, ensuring accurate spatial analysis.

### Visualization (`data_visualization.py`)
1. **Bar Plot**: Displays the duration between events by voyage ID, providing a visual summary of the time aspect of voyages.
2. **Line Plot**: Shows the distance traveled between ports by voyage ID, visualizing the spatial movement in a clear, intuitive format.
    - Uses `matplotlib` and `seaborn` for plotting, which are robust libraries for data visualization in Python.
    - Ensures that only complete data entries are used by dropping any rows with missing `duration` or `distance_nm` values.

### SQL Setup (`setup.sql`)
Sets up the initial database schema and populates the `voyages` table with sample data. This script is crucial for establishing a testing environment that mimics real-world scenarios of maritime voyages.

### Assumptions
- All geographic coordinates provided are accurate and represent the actual locations of the ports.
- The `allocatedVoyageId` field is used to filter out records that are not part of active voyages, assuming that null values indicate active records.

### Usage and Execution
Each script is designed to be run independently, with `data_extraction.py` fetching the data, `data_processing.py` processing the data, and `data_visualization.py` visualizing the results. Users are encouraged to run these scripts sequentially to perform a full analysis cycle from data extraction to visualization.


  
