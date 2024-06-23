
CREATE TABLE voyages (
    id INT,
    event VARCHAR(50),
    dateStamp INT,
    timeStamp FLOAT,
    voyage_From VARCHAR(50),
    lat DECIMAL(9,6),
    lon DECIMAL(9,6),
    imo_num VARCHAR(20),
    voyage_Id VARCHAR(20),
    allocatedVoyageId VARCHAR(20)
);

INSERT INTO voyages VALUES
(1, 'SOSP', 43831, 0.708333, 'Port A', 34.0522, -118.2437, '9434761', '6', NULL),
(2, 'EOSP', 43831, 0.791667, 'Port A', 34.0522, -118.2437, '9434761', '6', NULL),
(3, 'SOSP', 43832, 0.333333, 'Port B', 36.7783, -119.4179, '9434761', '6', NULL),
(4, 'EOSP', 43832, 0.583333, 'Port B', 36.7783, -119.4179, '9434761', '6', NULL);

-- Advanced query to calculate durations and distances
WITH event_times AS (
    SELECT 
        id,
        event,
        dateStamp + timeStamp AS event_utc,
        voyage_From,
        lat,
        lon,
        imo_num,
        voyage_Id,
        LAG(event) OVER (PARTITION BY imo_num ORDER BY dateStamp + timeStamp) AS prev_event,
        LAG(dateStamp + timeStamp) OVER (PARTITION BY imo_num ORDER BY dateStamp + timeStamp) AS prev_event_utc,
        LAG(voyage_From) OVER (PARTITION BY imo_num ORDER BY dateStamp + timeStamp) AS prev_port,
        LAG(lat) OVER (PARTITION BY imo_num ORDER BY dateStamp + timeStamp) AS prev_lat,
        LAG(lon) OVER (PARTITION BY imo_num ORDER BY dateStamp + timeStamp) AS prev_lon
    FROM voyages
    WHERE allocatedVoyageId IS NULL
),
calculated_times AS (
    SELECT
        *,
        CASE 
            WHEN event = 'SOSP' THEN event_utc - prev_event_utc
            ELSE NULL
        END AS sailing_time,
        CASE 
            WHEN event = 'EOSP' THEN event_utc - prev_event_utc
            ELSE NULL
        END AS port_stay_duration,
        CASE 
            WHEN event = 'SOSP' THEN 
                111 * SQRT(POWER(lat - prev_lat, 2) + POWER(lon - prev_lon, 2))
            ELSE NULL
        END AS distance_travelled
    FROM event_times
)
SELECT 
    id,
    event,
    event_utc,
    voyage_From,
    lat,
    lon,
    imo_num,
    voyage_Id,
    prev_event,
    prev_event_utc,
    prev_port,
    sailing_time,
    port_stay_duration,
    distance_travelled
FROM calculated_times
ORDER BY event_utc;
