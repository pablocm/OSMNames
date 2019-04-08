from helpers.functions import geometry_from_wkt
from osmnames.prepare_data.prepare_data import set_country_codes


def test_osm_polygon_country_code_get_set_base_on_country_grid(session, tables):
    session.add(
            tables.country_osm_grid(
                country_code='CH',
                geometry=geometry_from_wkt("POLYGON((0 0,4 0,4 4,0 4,0 0))")
            )
        )

    session.add(
            tables.osm_polygon(
                id=1,
                name="Some Polygon with missing country_code",
                geometry=geometry_from_wkt("POLYGON((1 1, 2 1, 2 2, 1 2,1 1))")
            )
        )

    session.commit()

    set_country_codes()

    assert session.query(tables.osm_polygon).get(1).country_code == 'ch'


def test_osm_polygon_country_code_get_set_bases_on_imported_country_code(session, tables):
    session.add(
            tables.osm_polygon(
                id=1,
                imported_country_code='CH',
            )
        )

    session.commit()

    set_country_codes()

    assert session.query(tables.osm_polygon).get(1).country_code == 'ch'


def test_osm_polygon_country_code_get_set_with_most_intersecting_country(session, tables):
    session.add(
            tables.country_osm_grid(
                country_code='CH',
                geometry=geometry_from_wkt("POLYGON((0 0,4 0,4 1,0 1,0 0))")
            )
        )

    session.add(
            tables.country_osm_grid(
                country_code='DE',
                geometry=geometry_from_wkt("POLYGON((0 0,4 0,4 4,0 4,0 0))")
            )
        )

    session.add(
            tables.osm_polygon(
                id=1,
                name="Some country with missing country_code",
                place_rank=4,
                geometry=geometry_from_wkt("POLYGON((0 0,4 0,4 4,0 4,0 0))")
            )
        )

    session.commit()

    set_country_codes()

    assert session.query(tables.osm_polygon).get(1).country_code == 'de'
