import json
import logging
import os
import sys

from enrichwrap import get_data, get_steps, get_all_mappings, set_default_targets, decide_with_json, \
    convert_to_sas


def enrich(step_string, incoming_data=None):
    logname = os.path.dirname(__file__) + os.path.sep + 'pythonenrich.log'
    logging.basicConfig(filename=logname,
                        format='[%(asctime)s] %(levelname)s:%(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S',
                        level=logging.INFO)

    enrich_targets = set_default_targets()
    step_dictionary = get_steps(step_string)
    if isinstance(incoming_data, str):
        incoming_data = get_data(incoming_data)

    mappings = get_all_mappings()
    #print('number of enrich_targets:', end=' ')
    #print(len(enrich_targets))
    #print('number in step_dictionary:', end=' ')
    #print(len(step_dictionary))
    #print('number in mappings: ', end=' ')
    #print(len(mappings))

    resulting_data = decide_with_json(enrich_targets, step_dictionary, mappings, incoming_data)
    sas_values = convert_to_sas(resulting_data, mappings)

    #print(json.dumps(resulting_data, indent=4))
    #print(json.dumps(sas_values, indent=4))
    return sas_values


if __name__ == '__main__':
    # setup_default_enrich_targets

    # Get default user data, as a starting point
    user_data = None

    # Get default step string of None as a starting point
    stepString = None
    if len(sys.argv) > 1:
        stepString = sys.argv[1]

    if len(sys.argv) > 2:
        user_data = sys.argv[2]

    enrich(stepString, user_data)

