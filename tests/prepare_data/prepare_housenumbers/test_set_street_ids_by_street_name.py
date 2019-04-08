from helpers.functions import geometry_from_wkt
from osmnames.prepare_data.prepare_housenumbers import set_street_ids_by_street_name


def test_when_street_with_same_parent_id_and_name_exists(session, tables):
    session.add(tables.osm_housenumber(id=1, parent_id=1337, normalized_street="haldenweg"))
    session.add(tables.osm_linestring(id=2, osm_id=42, parent_id=1337, normalized_name="haldenweg"))

    session.commit()

    set_street_ids_by_street_name()

    assert session.query(tables.osm_housenumber).get(1).street_id == 42


def test_when_street_with_same_parent_id_but_different_name_exists(session, tables):
    session.add(tables.osm_housenumber(id=1, parent_id=1337, normalized_street="haldenweg"))
    session.add(tables.osm_linestring(id=2, osm_id=42, parent_id=1337, normalized_name="hornstrasse"))

    session.commit()

    set_street_ids_by_street_name()

    assert session.query(tables.osm_housenumber).get(1).street_id is None


def test_when_street_with_same_name_but_different_parent_id_exists(session, tables):
    session.add(tables.osm_housenumber(id=1, parent_id=1337, normalized_street="haldenweg"))
    session.add(tables.osm_linestring(id=2, osm_id=42, parent_id=9999, normalized_name="haldenweg"))

    session.commit()

    set_street_ids_by_street_name()

    assert session.query(tables.osm_housenumber).get(1).street_id is None


def test_when_merged_street_with_same_parent_id_and_name_exists(session, tables):
    session.add(tables.osm_housenumber(id=1, parent_id=1337, normalized_street="haldenweg"))
    session.add(tables.osm_linestring(id=2, osm_id=42, merged_into=77, parent_id=1337, normalized_name="haldenweg"))

    session.commit()

    set_street_ids_by_street_name()

    assert session.query(tables.osm_housenumber).get(1).street_id == 77


def test_when_street_with_same_parent_id_but_almost_same_name_exists(session, tables):
    session.add(
            tables.osm_housenumber(
                id=1,
                parent_id=1337,
                osm_id=88267051,
                normalized_street="bochslenrasse",
                geometry_center=geometry_from_wkt("""POINT(5.87177496592101 51.010839973769)""")
                )

            )

    session.add(
            tables.osm_linestring(
                id=2,
                osm_id=42,
                parent_id=1337,
                normalized_name="bochslenstrasse",
                geometry=geometry_from_wkt("""LINESTRING(5.87196997089833
                    51.0102699589409,5.87157996094367 51.0114099815915)""")
                )
            )

    session.commit()

    set_street_ids_by_street_name()

    assert session.query(tables.osm_housenumber).get(1).street_id == 42


def test_when_housenumber_street_contains_full_street_name(session, tables):
    session.add(
            tables.osm_housenumber(
                id=1,
                parent_id=1337,
                osm_id=88267051,
                normalized_street="citepreville19",
                geometry_center=geometry_from_wkt("""POINT(5.87177496592101
                51.010839973769)""")
                )

            )

    session.add(
            tables.osm_linestring(
                id=2,
                osm_id=42,
                parent_id=1337,
                normalized_name="citepreville",
                geometry=geometry_from_wkt("""LINESTRING(5.87196997089833
                    51.0102699589409,5.87157996094367 51.0114099815915)""")
                )
            )

    session.commit()

    set_street_ids_by_street_name()

    assert session.query(tables.osm_housenumber).get(1).street_id == 42
