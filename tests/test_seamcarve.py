from seamcarvelib import seamcarve
import shutil
import filecmp
import os
import pytest


in_file = 'test_in.mp4'
duplicated_file = 'duplicate_file.mp4'
out_file = 'test_out.mp4'


@pytest.fixture(scope='module', autouse=True)
def carve_video():
    os.chdir('tests')
    shutil.copyfile(in_file, 'duplicate_file.mp4')
    seamcarve.carve_seams(in_file, out_file, distort_percentage=60)
    yield
    os.remove(duplicated_file)
    os.remove(out_file)


def test_carve_seams_no_alter_original_file():
    assert filecmp.cmp(in_file, duplicated_file)


def test_carve_seams_cleaned_up_properly():
    assert not os.path.isfile("distorted_" + out_file)


def test_carve_seams_output_file_exists():
    assert os.path.isfile(out_file)
