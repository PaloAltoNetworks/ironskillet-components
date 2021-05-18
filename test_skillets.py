import logging
import pytest

from skilletlib import SkilletLoader
from skilletlib.skillet.base import Skillet
from skilletlib.snippet.base import Snippet
from skilletlib.utils.testing_utils import setup_dir


logger = logging.getLogger(__name__)


def debug_skillet_can_load_in_dir(directory_to_test: str):
    skillet_loader = SkilletLoader()
    all_skillets = skillet_loader.load_all_skillets_from_dir(directory_to_test)

    assert len(all_skillets) > 0, 'Could not find any skillets to load!'

    assert len(skillet_loader.skillet_errors) == 0, 'Found Skillets with loader errors!'
    return all_skillets


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


def debug_skillet_includes(directory_to_test: str, skillet_name: str, amt_snippets: int, snippet_name: str, variable_name: str):
    """
    Tests to verify the Skillet object is successfully compiled from all included skillets.
    The 'include_other_skillets' skillet includes snippets and variables from two other skillets
    in the same directory

    :return: None
    """
    skillet_path = directory_to_test
    skillet_loader = SkilletLoader(path=skillet_path)
    skillet: Skillet = skillet_loader.get_skillet_with_name(skillet_name)
    
    # verify we can find and load the correct skillet
    assert skillet.name == skillet_name
    

    # verify the correct number of snippets.
    assert len(skillet.snippets) == amt_snippets
    
    included_snippet: Snippet = skillet.get_snippet_by_name(snippet_name)

    # verify we can get an included snippet from the skillet object
    #assert included_snippet is not None
    assert included_snippet.name == snippet_name

    # get the give variable name from the skillet
    included_variable: dict = skillet.get_variable_by_name(variable_name)

    # verify the included variable is present in the compiled skillet
    assert included_variable is not None

def debug_skillet_xpath_override(directory_to_test: str, skillet_name: str, snippet_name: str, xpath: str):
    """
    Tests to verify the Skillet object is successfully compiled from all included skillets.
    The 'include_other_skillets' skillet includes snippets and variables from two other skillets
    in the same directory

    :return: None
    """
    skillet_path = directory_to_test
    skillet_loader = SkilletLoader(path=skillet_path)
    skillet: Skillet = skillet_loader.get_skillet_with_name(skillet_name)
    
    # verify we can find and load the correct skillet
    assert skillet.name == skillet_name
    
    included_snippet: Snippet = skillet.get_snippet_by_name(snippet_name)

    # verify we can get an included snippet from the skillet object
    assert included_snippet is not None

    # verify the 'xpath' metadata attribute has been overridden correctly
    assert included_snippet.metadata.get('xpath', '') == xpath


# testing skillet directories for loading and variables
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



# Testing skillet includes for playlists
def test_panorama_shared_all_prototype():
    return debug_skillet_includes('./panos_v10.0', 'ironskillet_panorama_shared_all_prototype_10_0', 108, 'panorama_tag_10_0.ironskillet_tag_outbound', 'API_KEY_LIFETIME')


def test_panorama_shared_dgtemplate_prototype():
    return debug_skillet_includes('./panos_v10.0', 'ironskillet_panorama_shared_dgtemplate_all_prototype_10_0', 74, 'panorama_tag_10_0.ironskillet_tag_outbound', 'API_KEY_LIFETIME')


def test_panorama_notshared_dgtemplate_prototype():
    return debug_skillet_includes('./panos_v10.0', 'ironskillet_panorama_notshared_dgtemplate_all_prototype_10_0', 92, 'panorama_tag_10_0.ironskillet_tag_outbound', 'API_KEY_LIFETIME')


def test_panorama_notshared_prototype():
    return debug_skillet_includes('./panos_v10.0', 'ironskillet_panorama_notshared_all_prototype_10_0', 108, 'panorama_tag_10_0.ironskillet_tag_outbound', 'API_KEY_LIFETIME')


def test_panos_all_prototype():
    return debug_skillet_includes('./panos_v10.0', 'ironskillet_panos_all_prototype_10_0', 85, 'panos_ngfw_tag_10_0.ironskillet_tag_outbound', 'API_KEY_LIFETIME')



# Testing skillet xpath overrides
def test_panorama_notshared_xpath():
    return debug_skillet_xpath_override('./panos_v10.0', 'ironskillet_panorama_notshared_all_prototype_10_0', 'panorama_tag_10_0.ironskillet_tag_outbound', "/config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{{ DEVICE_GROUP }}']/tag")


def test_panorama_notshared_dgtemplate_xpath():
    return debug_skillet_xpath_override('./panos_v10.0', 'ironskillet_panorama_notshared_dgtemplate_all_prototype_10_0', 'panorama_tag_10_0.ironskillet_tag_outbound', "/config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{{ DEVICE_GROUP }}']/tag")
