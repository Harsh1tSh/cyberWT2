CREATE EXTENSION IF NOT EXISTS cube;
CREATE EXTENSION IF NOT EXISTS earthdistance;

SELECT a.id, a.voyage_From as port, a.lat, a.lon, b.voyage_From as next_port, b.lat as next_lat, b.lon as next_lon,
       earth_distance(ll_to_earth(a.lat, a.lon), ll_to_earth(b.lat, b.lon)) as distance_meters
FROM voyages a
JOIN voyages b ON a.imo_num = b.imo_num AND a.voyage_Id = b.voyage_Id AND b.id = a.id + 1
WHERE a.allocatedVoyageId IS NULL AND b.allocatedVoyageId IS NULL;
