#  Copyright (c) 2020, Manfred Moitzi
#  License: MIT License
import pytest
import os
import ezdxf

BASEDIR = os.path.dirname(__file__)
DATADIR = 'data'
COLDFIRE = os.path.join(
    ezdxf.EZDXF_TEST_FILES,
    "CADKitSamples/kit-dev-coldfire-xilinx_5213.dxf")


@pytest.mark.skipif(not os.path.exists(COLDFIRE),
                    reason='test data not present')
def test_kit_dev_coldfire():
    doc = ezdxf.readfile(COLDFIRE)
    auditor = doc.audit()
    assert len(auditor) == 0


@pytest.fixture(params=['Leica_Disto_S910.dxf'])
def filename(request):
    filename = os.path.join(BASEDIR, DATADIR, request.param)
    if not os.path.exists(filename):
        pytest.skip(f'File {filename} not found.')
    return filename


def test_leica_disto_r12(filename):
    doc = ezdxf.readfile(filename)
    auditor = doc.audit()
    assert len(auditor) == 0
