#!/usr/bin/python


import os
import pytest
import shutil
import tempfile

from ansible.modules.gears import sprocket

@pytest.fixture()
def handle_test_outputs(request):

    # emit a directory to write test files to
    testdir = tempfile.mkdtemp()
    yield testdir

    # cleanup the directory once the test completes
    def cleanup():
        shutil.rmtree(testdir)        
    request.addfinalizer(cleanup)


def test_sprocket_set_gear(handle_test_outputs):

    # declare the gear file with the test dir as the path
    fn = os.path.join(handle_test_outputs, 'testgear.txt')
    
    # run the setter
    sprocket.set_gear('test', fn)

    # check that it was written
    assert os.path.isfile(fn)

    # check that it had the right content
    with open(fn, 'r') as f:
        fdata = f.read()
    assert fdata == 'test\n'

    os.remove(fn)


def test_sprocket_unset_gear(handle_test_outputs):
    # unset_gear(gearname, gearfile)

    fn = os.path.join(handle_test_outputs, 'testgear.txt')
    with open(fn, 'w') as f:
        f.write('test\n')

    sprocket.unset_gear(fn)

    assert not os.path.isfile(fn)    
