import logging
import skilletlib

from skilletlib import SkilletLoader
from tests import test_skillet_include

logger = logging.getLogger(__name__)


def debug_skillet_can_load_in_dir(directory_to_test: str):
    skillet_loader = SkilletLoader()
    all_skillets = skillet_loader.load_all_skillets_from_dir(directory_to_test)

    assert len(all_skillets) > 0, 'Could not find any skillets to load!'

    assert len(skillet_loader.skillet_errors) == 0, 'Found Skillets with loader errors!'


def debug_all_skillets_in_dir(directory_to_test: str):
    skillet_loader = SkilletLoader()
    all_skillets = skillet_loader.load_all_skillets_from_dir(directory_to_test)

    assert len(all_skillets) > 0

    for skillet in all_skillets:
        errors = skillet_loader.debug_skillet_structure(skillet.skillet_dict)
        assert len(errors) == 0, f'Found debug errors for skillet: {skillet.name}'

        declared_variables = skillet.get_declared_variables()
        for var_name in declared_variables:
            found = False
            for var_def in skillet.variables:
                if var_def['name'] == var_name:
                    found = True
                    break

            assert found is True, f'Found variable with name: {var_name} that was not defined in {skillet.name}!'


def test_panos_v9_skillets_can_load():
    return debug_skillet_can_load_in_dir('./panos_v9.1')


def test_panos_v10_skillets_can_load():
    return debug_skillet_can_load_in_dir('./panos_v10.0')


def test_validation_skillets_can_load():
    return debug_skillet_can_load_in_dir('./validations')


def test_panos_v90_skillet_variables():
    return debug_all_skillets_in_dir('./panos_v9.1')


def test_panos_v10_skillet_variables():
    return debug_all_skillets_in_dir('./panos_v10.0')


def test_validation_skillet_variables():
    return debug_all_skillets_in_dir('./validations')
