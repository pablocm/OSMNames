DROP MATERIALIZED VIEW IF EXISTS mv_housenumbers;
CREATE MATERIALIZED VIEW mv_housenumbers AS
SELECT
  osm_id,
  street_id::VARCHAR AS street_id,
  street,
  housenumber,
  round(ST_X(ST_Centroid(geometry))::numeric, 7) AS lon,
  round(ST_Y(ST_Centroid(geometry))::numeric, 7) AS lat
FROM osm_housenumber
WHERE street_id IS NOT NULL;
