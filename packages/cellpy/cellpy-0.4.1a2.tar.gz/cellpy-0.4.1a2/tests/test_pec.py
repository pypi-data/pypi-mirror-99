import tempfile
import shutil
import pytest
import logging
from cellpy import log
from . import fdv

log.setup_logging(default_level=logging.DEBUG)


@pytest.fixture
def cellpy_data_instance():
    from cellpy import cellreader

    return cellreader.CellpyData()


def test_set_instrument(cellpy_data_instance):
    instrument = "pec_csv"
    cellpy_data_instance.set_instrument(instrument=instrument)
    cellpy_data_instance.cycle_mode = "cathode"
    cellpy_data_instance.from_raw(fdv.pec_file_path)
    cellpy_data_instance.set_mass(50_000)
    cellpy_data_instance.make_step_table()
    cellpy_data_instance.make_summary()
    temp_dir = tempfile.mkdtemp()
    cellpy_data_instance.to_csv(datadir=temp_dir)
    shutil.rmtree(temp_dir)
