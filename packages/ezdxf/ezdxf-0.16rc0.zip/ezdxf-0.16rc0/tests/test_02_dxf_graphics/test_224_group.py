# Copyright (c) 2015-2019, Manfred Moitzi
# License: MIT License
import pytest
import ezdxf


@pytest.fixture(scope='module')
def groups():
    doc = ezdxf.new('R2000')
    return doc.groups


def test_group_table_is_empty(groups):
    assert 0 == len(groups)


def test_create_new_group(groups):
    g = groups.new('MyGroup', description="The group description.")
    assert 'GROUP' == g.dxftype()
    assert 'MyGroup' in groups
    assert 0 == g.dxf.unnamed, "Named group has wrong unnamed attribute."
    assert 1 == g.dxf.selectable, "Group should be selectable by default."
    assert "The group description." == g.dxf.description
    assert 1 == len(groups)
    groups.clear()
    assert 0 == len(groups)


def test_create_unnamed_group(groups):
    g = groups.new()
    assert 'GROUP' == g.dxftype()
    assert '*A1' in groups
    assert 1 == g.dxf.unnamed, "Unnamed group has wrong unnamed attribute."
    assert 1 == g.dxf.selectable, "Group should be selectable by default."
    assert "" == g.dxf.description, "Group description should be '' by default."
    assert 1 == len(groups)
    groups.clear()
    assert 0 == len(groups)


def test_delete_group_by_entity(groups):
    assert len(groups) == 0
    g = groups.new('MyGroup')
    assert len(groups) == 1
    groups.delete(g)
    assert len(groups) == 0


def test_delete_group_by_name(groups):
    assert 'MyGroup' not in groups
    groups.new('MyGroup')
    groups.delete('MyGroup')
    assert 0 == len(groups)


def test_add_entities():
    dwg = ezdxf.new('R2000')
    group = dwg.groups.new()
    # the group itself is not an entity space, DXF entities has to be placed in model space, paper space
    # or in a block
    msp = dwg.modelspace()
    with group.edit_data() as e:  # e is a standard Python list of DXF entities
        line = msp.add_line((0, 0), (3, 0))
        e.append(line)
        e.append(msp.add_circle((0, 0), radius=2))

    assert 2 == len(group)
    assert line in group

    ungrouped_line = msp.add_line((0, 1), (3, 1))
    assert ungrouped_line not in group

    group.clear()
    assert 0 == len(group)
