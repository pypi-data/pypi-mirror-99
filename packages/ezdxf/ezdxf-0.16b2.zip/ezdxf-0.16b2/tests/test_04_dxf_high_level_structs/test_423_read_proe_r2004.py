# Copyright (c) 2014-2020, Manfred Moitzi
# License: MIT-License
import pytest

import ezdxf
import os

FILE = os.path.join(ezdxf.EZDXF_TEST_FILES, 'ProE_AC1018.dxf')


@pytest.mark.skipif(
    not os.path.exists(FILE),
    reason=f"Skip reading ProE AC1018: test file '{FILE}' not available.")
def test_open_proe_ac1018():
    doc = ezdxf.readfile(FILE)
    modelspace = doc.modelspace()

    # are there entities in model space
    assert 17 == len(modelspace)

    # can you get entities
    lines = modelspace.query('LINE')
    assert 12 == len(lines)

    # is owner tag correct
    first_line = lines[0]
    assert modelspace.layout_key == first_line.dxf.owner

    # is paper space == 0
    assert 0 == first_line.dxf.paperspace
