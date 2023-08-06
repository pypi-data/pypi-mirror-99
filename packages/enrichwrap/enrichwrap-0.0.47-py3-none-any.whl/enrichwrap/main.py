import sys

from enrichwrap import get_data, get_steps, get_all_mappings, set_default_targets, convert_to_sas, decide_with_json, \
    get_default_data, setup_logging, add_outstr, get_outstr


def enrich(step_string,
           incoming_data=None, logdir=None, http_url=None, http_port=None, enrich_targets=None, in_mappings=None):

    setup_logging(logdir)

    add_outstr('Starting enrichment')
    step_dictionary = get_steps(step_string)
    if isinstance(incoming_data, str):
        incoming_data = get_data(incoming_data)
    else:
        incoming_data = get_default_data()

    if enrich_targets is None or enrich_targets == 'None':
        enrich_targets = set_default_targets(http_url, http_port)

    if in_mappings is None:
        mappings = get_all_mappings()
    else:
        mappings = in_mappings

    tool_data = decide_with_json(enrich_targets, step_dictionary, mappings, incoming_data)
    sas_data = convert_to_sas(tool_data, mappings)

    #print(json.dumps(resulting_data, indent=4))
    #print(json.dumps(sas_values, indent=4))
    return {"tool_data": tool_data, "sas_data": sas_data}


if __name__ == '__main__':
    # setup_default_enrich_targets

    # Get default user data, as a starting point
    user_data = None
    logdir = None
    http_url = None
    http_port = None
    enrichtargets = None
    in_mappings = None

    # Get default step string of None as a starting point
    stepString = None
    if len(sys.argv) > 1:
        stepString = sys.argv[1]

    if len(sys.argv) > 2 and sys.argv[2] != 'None':
        user_data = sys.argv[2]

    if len(sys.argv) > 3 and sys.argv[3] != 'None':
        logdir = sys.argv[3]

    if len(sys.argv) > 4:
        http_url = sys.argv[4]

    if len(sys.argv) > 5:
        http_port = sys.argv[5]

    if len(sys.argv) > 6:
        enrichtargets = sys.argv[6]

    if len(sys.argv) > 7:
        in_mappings = sys.argv[8]

    # enrich('socure', None, None, '10.44.16.24', '8200', None)
    enrich(stepString, user_data, logdir, http_url, http_port, enrichtargets, in_mappings)
    #print(get_outstr())
