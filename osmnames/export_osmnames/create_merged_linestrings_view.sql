DROP MATERIALIZED VIEW IF EXISTS mv_merged_linestrings;
CREATE MATERIALIZED VIEW mv_merged_linestrings AS
SELECT
  name,
  alternative_names,
  'way'::TEXT as osm_type,
  osm_id::VARCHAR AS osm_id,
  class,
  type,
  round(ST_X(ST_PointOnSurface(geometry))::numeric, 7) AS lon,
  round(ST_Y(ST_PointOnSurface(geometry))::numeric, 7) AS lat,
  place_rank,
  get_importance(place_rank, wikipedia, parentInfo.country_code) AS importance,
  CASE WHEN class = 'highway' THEN name ELSE NULL::TEXT END AS street,
  parentInfo.city AS city,
  parentInfo.county AS county,
  parentInfo.state AS state,
  get_country_name(parentInfo.country_code) AS country,
  parentInfo.country_code AS country_code,
  parentInfo.displayName AS display_name,
  round(ST_XMIN(geometry)::numeric, 7) AS west,
  round(ST_YMIN(geometry)::numeric, 7) AS south,
  round(ST_XMAX(geometry)::numeric, 7) AS east,
  round(ST_YMAX(geometry)::numeric, 7) AS north,
  NULLIF(wikidata, '') AS wikidata,
  NULLIF(wikipedia, '') AS wikipedia,
  get_housenumbers(osm_id) AS housenumbers
FROM
  osm_merged_linestring,
  determine_class(type) AS class,
  get_parent_info(parent_id, name) as parentInfo;
