# Copyright (c) 2020, Manfred Moitzi
# License: MIT License
from typing import cast, Union

import pytest
import ezdxf
import math

from ezdxf.entities import Ellipse, Point, Arc
from ezdxf.math import Vec3


@pytest.fixture(scope='module')
def doc():
    d = ezdxf.new()
    blk = d.blocks.new('Test1')
    blk.add_line((0, 0), (1, 0))
    blk.add_line((0, 0), (0, 1))
    msp = d.modelspace()
    msp.add_blockref('Test1', (10, 10))
    msp.add_blockref('Test1', (20, 10), dxfattribs={'xscale': 2})  # yscale and zscale
    return d


@pytest.fixture(scope='module')
def msp(doc):
    return doc.modelspace()


@pytest.fixture(scope='module')
def entitydb(doc):
    return doc.entitydb


def test_01_virtual_entities(msp):
    blockrefs = msp.query('INSERT')
    blockref = blockrefs[0]

    virtual_entities = list(blockref.virtual_entities())
    assert len(virtual_entities) == 2

    e = virtual_entities[0]
    # Virtual entities should not be stored in the entity database.
    assert e.dxf.handle is None, 'handle should be None'
    # Virtual entities should not reside in a layout.
    assert e.dxf.owner is None, 'owner should be None'
    # Virtual entities should be assigned to the same document as the block reference.
    assert e.doc is blockref.doc

    assert e.dxftype() == 'LINE'
    assert e.dxf.start == blockref.dxf.insert
    assert e.dxf.end == blockref.dxf.insert + (1, 0)

    e = virtual_entities[1]
    assert e.dxftype() == 'LINE'
    assert e.dxf.start == blockref.dxf.insert
    assert e.dxf.end == blockref.dxf.insert + (0, 1)

    blockref = blockrefs[1]
    virtual_entities = list(blockref.virtual_entities())
    assert len(virtual_entities) == 2

    e = virtual_entities[0]
    assert e.dxftype() == 'LINE'
    assert e.dxf.start == blockref.dxf.insert
    assert e.dxf.end == blockref.dxf.insert + (2, 0), 'should apply xscale 2'

    e = virtual_entities[1]
    assert e.dxftype() == 'LINE'
    assert e.dxf.start == blockref.dxf.insert
    assert e.dxf.end == blockref.dxf.insert + (0, 1), 'should apply yscale 1'


def test_02_explode_blockrefs(doc, msp, entitydb):
    blockrefs = msp.query('INSERT')
    blockref = blockrefs.first
    blockref_owner = blockref.dxf.owner
    blockref_insert = blockref.dxf.insert

    assert len(msp) == 2  # 2 INSERT
    exploded_entities = blockref.explode()
    assert blockref.is_alive is False, 'Exploded block reference should be destroyed.'
    assert len(exploded_entities) == 2
    assert len(msp) == 3  # 2 INSERT - 1 exploded INSERT + 2 LINE

    e = exploded_entities[0]
    # Exploded entities should be stored in the entity database.
    assert e.dxf.handle is not None, 'entity should have a handle'
    assert e.dxf.handle in entitydb
    # Exploded entities should reside in a layout.
    assert e.dxf.owner is not None, 'entity should have an owner'
    assert e.dxf.owner is blockref_owner
    # Exploded entities should be assigned to the same document as the block reference.
    assert e.doc is doc

    assert e.dxftype() == 'LINE'
    assert e.dxf.start == blockref_insert
    assert e.dxf.end == blockref_insert + (1, 0)

    e = exploded_entities[1]
    assert e.dxftype() == 'LINE'
    assert e.dxf.start == blockref_insert
    assert e.dxf.end == blockref_insert + (0, 1)


def test_03_explode_polyline_bulge(doc, msp):
    blk = doc.blocks.new('Test03')
    blk.add_lwpolyline([(0, 0), (3, 0, 0.5), (6, 0), (9, 0)], format='xyb')
    block_ref = msp.add_blockref('Test03', insert=(0, 0), dxfattribs={
        'yscale': 0.5,
    })
    entities = list(block_ref.virtual_entities())
    assert len(entities) == 3

    e = entities[0]
    assert e.dxftype() == 'LINE'
    assert e.dxf.start == (0, 0)
    assert e.dxf.end == (3, 0)

    e = entities[1]
    e = cast(Ellipse, e)
    assert e.dxftype() == 'ELLIPSE'
    assert e.dxf.center.isclose((4.5, 0.5625, 0))
    assert e.dxf.major_axis.isclose((1.875, 0.0, 0))
    assert e.dxf.ratio == 0.5
    assert math.isclose(e.dxf.start_param, -2.498091544796509 % math.tau)
    assert math.isclose(e.dxf.end_param, -0.6435011087932843 % math.tau)
    assert e.start_point.isclose(Vec3(3, 0, 0))
    assert e.end_point.isclose(Vec3(6, 0, 0), abs_tol=1e-5)

    e = entities[2]
    assert e.dxftype() == 'LINE'
    assert e.dxf.start == (6, 0)
    assert e.dxf.end == (9, 0)


def test_04_explode_blockref_with_attrib(doc, msp, entitydb):
    blockref = msp.add_blockref('Test1', (20, 10))  # with attrib
    blockref.add_attrib(tag='TAG', text='Text', insert=(1.5, 2.6))
    assert len(blockref.attribs) == 1, 'Error in add_attrib()'
    attrib = blockref.attribs[0]

    exploded_entities = blockref.explode()
    assert blockref.is_alive is False, 'Exploded block reference should be destroyed.'
    assert attrib.is_alive is False, 'Exploded attribs should be destroyed.'
    assert len(exploded_entities) == 3, '2x LINE and 1x TEXT'
    text = exploded_entities[-1]
    assert text.dxftype() == 'TEXT'
    assert text.dxf.text == 'Text'
    assert text.dxf.insert == (1.5, 2.6), 'ATTRIB already located in WCS'


def test_05_examine_uniform_scaled_ellipse(doc, msp):
    blk = doc.blocks.new('EllipseBlk')
    blk.add_ellipse((0, 0), major_axis=(2, 0), ratio=0.5)
    blkref = msp.add_blockref('EllipseBlk', insert=(2, 2)).set_scale(2)
    ellipse = list(blkref.virtual_entities())[0]
    assert ellipse.dxftype() == 'ELLIPSE'
    assert ellipse.dxf.center == (2, 2)
    assert ellipse.dxf.major_axis == (4, 0)
    assert ellipse.dxf.ratio == 0.5


def test_06_skipped_entities_callback(doc, msp):
    blk = doc.blocks.new('test_block')
    hatch = blk.add_hatch()
    edge_path = hatch.paths.add_edge_path()
    edge_path.add_arc((0, 0))
    blk.add_line((0, 0), (1, 0))
    blkref = msp.add_blockref('test_block', insert=(0, 0)).place((0, 0), (1, 2, 3))
    skipped_entities = []

    def on_entity_skipped(entity, reason):
        skipped_entities.append((entity, reason))

    assert not blkref.has_uniform_scaling
    assert hatch.paths.has_critical_elements()
    entities = list(blkref.virtual_entities(skipped_entity_callback=on_entity_skipped))

    assert len(entities) == 2
    assert entities[0].dxftype() == 'HATCH'
    assert entities[1].dxftype() == 'LINE'
    assert len(skipped_entities) == 0


def _get_transformed_curve(scale_factors: Vec3, rotation: float, is_arc: bool) -> Union[Ellipse, Arc]:
    doc = ezdxf.new()
    blk = doc.blocks.new('block')
    if is_arc:
        blk.add_arc((0, 0), radius=1, start_angle=0, end_angle=math.degrees(math.pi / 2))
    else:
        blk.add_ellipse((0, 0), major_axis=(1, 0), ratio=1, start_param=0, end_param=math.pi / 2)

    assert blk[0].start_point.isclose(Vec3(1, 0, 0))
    assert blk[0].end_point.isclose(Vec3(0, 1, 0))

    blk.add_point((1, 0))
    blk.add_point((0, 1))
    block_ref = doc.modelspace().add_blockref('block', insert=(0, 0), dxfattribs={
        'xscale': scale_factors.x, 'yscale': scale_factors.y, 'zscale': scale_factors.z,
        'rotation': math.degrees(rotation)
    })
    entities = list(block_ref.virtual_entities())
    assert len(entities) == 3
    ellipse = cast(Union[Ellipse, Arc], entities[0])

    # points should have been transformed the same as the ellipse
    assert entities[1].dxftype() == 'POINT'
    start_point = cast(Point, entities[1])
    assert start_point.dxf.location.isclose(ellipse.start_point)
    assert entities[2].dxftype() == 'POINT'
    end_point = cast(Point, entities[2])
    assert end_point.dxf.location.isclose(ellipse.end_point)

    return ellipse


def _check_curve(ellipse: Ellipse, expected_start: Vec3, expected_end: Vec3, expected_extrusion: Vec3):
    assert ellipse.start_point.isclose(expected_start)
    assert ellipse.end_point.isclose(expected_end)
    assert ellipse.dxf.extrusion.is_parallel(expected_extrusion)


@pytest.mark.parametrize('zscale,is_arc', [(1, False), (0.5, False), (1, True), (0.5, True), (-1, False), (-1, True)])
def test_07_rotated_and_reflected_curves(zscale, is_arc):
    scale = Vec3(1, 1, zscale)

    ellipse = _get_transformed_curve(scale, 0.0, is_arc)
    _check_curve(ellipse, Vec3(1, 0, 0), Vec3(0, 1, 0), Vec3(0, 0, zscale))

    ellipse = _get_transformed_curve(scale, math.pi / 2, is_arc)
    _check_curve(ellipse, Vec3(0, 1, 0), Vec3(-1, 0, 0), Vec3(0, 0, zscale))

    ellipse = _get_transformed_curve(scale, math.pi, is_arc)
    _check_curve(ellipse, Vec3(-1, 0, 0), Vec3(0, -1, 0), Vec3(0, 0, zscale))

    ellipse = _get_transformed_curve(scale, 3 * math.pi / 2, is_arc)
    _check_curve(ellipse, Vec3(0, -1, 0), Vec3(1, 0, 0), Vec3(0, 0, zscale))

    scale = Vec3(1, -1, zscale)

    ellipse = _get_transformed_curve(scale, 0.0, is_arc)
    _check_curve(ellipse, Vec3(1, 0, 0), Vec3(0, -1, 0), Vec3(0, 0, zscale))

    ellipse = _get_transformed_curve(scale, math.pi / 2, is_arc)
    _check_curve(ellipse, Vec3(0, 1, 0), Vec3(1, 0, 0), Vec3(0, 0, zscale))

    ellipse = _get_transformed_curve(scale, math.pi, is_arc)
    _check_curve(ellipse, Vec3(-1, 0, 0), Vec3(0, 1, 0), Vec3(0, 0, zscale))

    ellipse = _get_transformed_curve(scale, 3 * math.pi / 2, is_arc)
    _check_curve(ellipse, Vec3(0, -1, 0), Vec3(-1, 0, 0), Vec3(0, 0, zscale))

    scale = Vec3(-1, 1, zscale)

    ellipse = _get_transformed_curve(scale, 0.0, is_arc)
    _check_curve(ellipse, Vec3(-1, 0, 0), Vec3(0, 1, 0), Vec3(0, 0, zscale))

    ellipse = _get_transformed_curve(scale, math.pi / 2, is_arc)
    _check_curve(ellipse, Vec3(0, -1, 0), Vec3(-1, 0, 0), Vec3(0, 0, zscale))

    ellipse = _get_transformed_curve(scale, math.pi, is_arc)
    _check_curve(ellipse, Vec3(1, 0, 0), Vec3(0, -1, 0), Vec3(0, 0, zscale))

    ellipse = _get_transformed_curve(scale, 3 * math.pi / 2, is_arc)
    _check_curve(ellipse, Vec3(0, 1, 0), Vec3(1, 0, 0), Vec3(0, 0, zscale))

    scale = Vec3(-1, -1, zscale)

    ellipse = _get_transformed_curve(scale, 0.0, is_arc)
    _check_curve(ellipse, Vec3(-1, 0, 0), Vec3(0, -1, 0), Vec3(0, 0, zscale))

    ellipse = _get_transformed_curve(scale, math.pi / 2, is_arc)
    _check_curve(ellipse, Vec3(0, -1, 0), Vec3(1, 0, 0), Vec3(0, 0, zscale))

    ellipse = _get_transformed_curve(scale, math.pi, is_arc)
    _check_curve(ellipse, Vec3(1, 0, 0), Vec3(0, 1, 0), Vec3(0, 0, zscale))

    ellipse = _get_transformed_curve(scale, 3 * math.pi / 2, is_arc)
    _check_curve(ellipse, Vec3(0, 1, 0), Vec3(-1, 0, 0), Vec3(0, 0, zscale))


@pytest.mark.parametrize('stretch,is_arc', [(0.5, False), (0.5, True)])
def test_08_rotated_and_reflected_and_stretched_curves(stretch, is_arc):
    scale = Vec3(1, stretch, 1)

    ellipse = _get_transformed_curve(scale, 0.0, is_arc)
    _check_curve(ellipse, Vec3(1, 0, 0), Vec3(0, stretch, 0), Vec3(0, 0, 1))

    ellipse = _get_transformed_curve(scale, math.pi / 2, is_arc)
    _check_curve(ellipse, Vec3(0, 1, 0), Vec3(-stretch, 0, 0), Vec3(0, 0, 1))

    ellipse = _get_transformed_curve(scale, math.pi, is_arc)
    _check_curve(ellipse, Vec3(-1, 0, 0), Vec3(0, -stretch, 0), Vec3(0, 0, 1))

    ellipse = _get_transformed_curve(scale, 3 * math.pi / 2, is_arc)
    _check_curve(ellipse, Vec3(0, -1, 0), Vec3(stretch, 0, 0), Vec3(0, 0, 1))

    scale = Vec3(1, -stretch, 1)

    ellipse = _get_transformed_curve(scale, 0.0, is_arc)
    _check_curve(ellipse, Vec3(1, 0, 0), Vec3(0, -stretch, 0), Vec3(0, 0, 1))

    ellipse = _get_transformed_curve(scale, math.pi / 2, is_arc)
    _check_curve(ellipse, Vec3(0, 1, 0), Vec3(stretch, 0, 0), Vec3(0, 0, 1))

    ellipse = _get_transformed_curve(scale, math.pi, is_arc)
    _check_curve(ellipse, Vec3(-1, 0, 0), Vec3(0, stretch, 0), Vec3(0, 0, 1))

    ellipse = _get_transformed_curve(scale, 3 * math.pi / 2, is_arc)
    _check_curve(ellipse, Vec3(0, -1, 0), Vec3(-stretch, 0, 0), Vec3(0, 0, 1))

    scale = Vec3(-1, stretch, 1)

    ellipse = _get_transformed_curve(scale, 0.0, is_arc)
    _check_curve(ellipse, Vec3(-1, 0, 0), Vec3(0, stretch, 0), Vec3(0, 0, 1))

    ellipse = _get_transformed_curve(scale, math.pi / 2, is_arc)
    _check_curve(ellipse, Vec3(0, -1, 0), Vec3(-stretch, 0, 0), Vec3(0, 0, 1))

    ellipse = _get_transformed_curve(scale, math.pi, is_arc)
    _check_curve(ellipse, Vec3(1, 0, 0), Vec3(0, -stretch, 0), Vec3(0, 0, 1))

    ellipse = _get_transformed_curve(scale, 3 * math.pi / 2, is_arc)
    _check_curve(ellipse, Vec3(0, 1, 0), Vec3(stretch, 0, 0), Vec3(0, 0, 1))

    scale = Vec3(-1, -stretch, 1)

    ellipse = _get_transformed_curve(scale, 0.0, is_arc)
    _check_curve(ellipse, Vec3(-1, 0, 0), Vec3(0, -stretch, 0), Vec3(0, 0, 1))

    ellipse = _get_transformed_curve(scale, math.pi / 2, is_arc)
    _check_curve(ellipse, Vec3(0, -1, 0), Vec3(stretch, 0, 0), Vec3(0, 0, 1))

    ellipse = _get_transformed_curve(scale, math.pi, is_arc)
    _check_curve(ellipse, Vec3(1, 0, 0), Vec3(0, stretch, 0), Vec3(0, 0, 1))

    ellipse = _get_transformed_curve(scale, 3 * math.pi / 2, is_arc)
    _check_curve(ellipse, Vec3(0, 1, 0), Vec3(-stretch, 0, 0), Vec3(0, 0, 1))


def test_explode_xref(doc, msp):
    doc.add_xref_def('test.dxf', 'xref_test')
    xref = msp.add_blockref('xref_test', (0, 0))
    assert xref.is_xref() is True
    
    result = xref.explode()
    assert len(result) == 0


if __name__ == '__main__':
    pytest.main([__file__])
