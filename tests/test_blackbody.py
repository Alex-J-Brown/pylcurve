import pytest
from pylcurve.blackbody import build_bb_interpolator

def test_build_bb_interpolator():
    assert True
    build_bb_interpolator()

@pytest.fixture
def bb_interpolator():
    return build_bb_interpolator()


def test_bb_ucam(bb_interpolator):
    assert bb_interpolator['WD']['Koester']['ucam']['gs'](10000, 8.0) == 10250.26772
    assert bb_interpolator['WD']['Claret']['ucam']['gs'](10000, 8.0) == 10332.55543
    assert bb_interpolator['MS']['PHOENIX-HiRes']['ucam']['gs'](3000, 4.5) == 2996.59618
    assert bb_interpolator['MS']['BT-SETTL']['ucam']['gs'](3000, 4.5) == 2891.20661
    assert bb_interpolator['MS']['BT-SETTL-CIFIST']['ucam']['gs'](3000, 4.5) == 2909.02127
    

def test_bb_hcam(bb_interpolator):
    assert bb_interpolator['WD']['Koester']['hcam']['gs'](10000, 8.0) == 10250.33952
    assert bb_interpolator['WD']['Claret']['hcam']['gs'](10000, 8.0) == 10332.55543
    assert bb_interpolator['MS']['PHOENIX-HiRes']['hcam']['gs'](3000, 4.5) == 2991.27596
    assert bb_interpolator['MS']['BT-SETTL']['hcam']['gs'](3000, 4.5) == 2887.07213
    assert bb_interpolator['MS']['BT-SETTL-CIFIST']['hcam']['gs'](3000, 4.5) == 2905.83433


def test_bb_sdss(bb_interpolator):
    assert bb_interpolator['WD']['Koester']['sdss']['g'](10000, 8.0) == 10233.95935
    assert bb_interpolator['MS']['PHOENIX-HiRes']['sdss']['g'](3000, 4.5) == 2975.86742
    assert bb_interpolator['MS']['BT-SETTL']['sdss']['g'](3000, 4.5) == 2882.16113
    assert bb_interpolator['MS']['BT-SETTL-CIFIST']['sdss']['g'](3000, 4.5) == 2910.68012


def test_bb_ucam_sloan(bb_interpolator):
    assert bb_interpolator['WD']['Koester']['ucam_sloan']['g'](10000, 8.0) == 10257.88300
    assert bb_interpolator['MS']['PHOENIX-HiRes']['ucam_sloan']['g'](3000, 4.5) == 2997.89380
    assert bb_interpolator['MS']['BT-SETTL']['ucam_sloan']['g'](3000, 4.5) == 2884.14573
    assert bb_interpolator['MS']['BT-SETTL-CIFIST']['ucam_sloan']['g'](3000, 4.5) == 2896.72521


def test_bb_ztf(bb_interpolator):
    assert bb_interpolator['WD']['Koester']['ztf']['g'](10000, 8.0) == 10291.82873
    assert bb_interpolator['MS']['PHOENIX-HiRes']['ztf']['g'](3000, 4.5) == 2903.64916
    assert bb_interpolator['MS']['BT-SETTL']['ztf']['g'](3000, 4.5) == 2878.92185
    assert bb_interpolator['MS']['BT-SETTL-CIFIST']['ztf']['g'](3000, 4.5) == 2897.49861


def test_bb_tess(bb_interpolator):
    assert bb_interpolator['WD']['Koester']['tess']['tess'](10000, 8.0) == 9767.81973
    assert bb_interpolator['WD']['Claret']['tess']['tess'](10000, 8.0) == 9758.77952
    assert bb_interpolator['MS']['PHOENIX-HiRes']['tess']['tess'](3000, 4.5) == 3005.45890
    assert bb_interpolator['MS']['BT-SETTL']['tess']['tess'](3000, 4.5) == 3000.03287
    assert bb_interpolator['MS']['BT-SETTL-CIFIST']['tess']['tess'](3000, 4.5) == 3010.74730