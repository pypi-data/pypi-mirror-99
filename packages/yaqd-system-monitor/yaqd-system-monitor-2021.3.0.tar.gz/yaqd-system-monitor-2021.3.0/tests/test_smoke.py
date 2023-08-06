import time
import pathlib
import subprocess

import pytest

import yaqc


@pytest.fixture(scope="module")
def run_daemon():
    config = pathlib.Path(__file__).parent / "config.toml"
    with subprocess.Popen(["yaqd-system-monitor", "--config", config]) as proc:
        time.sleep(0.2)
        c = yaqc.Client(38070)
        yield c
        proc.terminate()


def test_nothing(run_daemon):
    c = run_daemon
    print(c.id())
    c.measure()
    start = time.time()
    while c.busy():
        if time.time() - start > 2:
            raise TimeoutError
        time.sleep(0.1)
    assert c.get_measured()
