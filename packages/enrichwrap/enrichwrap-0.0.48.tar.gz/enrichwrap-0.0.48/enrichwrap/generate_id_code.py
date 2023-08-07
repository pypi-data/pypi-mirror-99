import os

from enrichwrap import enrich, add_mapping


def get_return_line(extra, sas_data):
    val = ['   return ']
    if extra is not None:
        val.append(extra)
    for key in sas_data.keys():
        if len(val) > 0:
            val.append(',')
        val.append(key)
    return ''.join(val)


def get_output_line(extra, sas_data):
    val = ["   'Output:"]
    if extra is not None:
        val.append(extra)
    for key in sas_data.keys():
        if len(val) > 0:
            val.append(',')
        val.append(key)
    val.append("'")
    return ''.join(val)


def get_starter_body(tool, http_addr, http_port, sample_data_in=None, targets_in=None, mappings_in=None, mappings_out=None):

    sample_data = None
    if sample_data_in is not None:
        sample_data = sample_data_in

    content = ["   choices = enrichwrap.get_mapping_choices()", ""]

    if sample_data is not None:
        content.append("   sample_data = '" + sample_data_in + "'")
    else:
        content.append("   sample_data = None")
    content.append("")

    if targets_in is not None:
        content.append("   targets = enrichwrap.add_or_update_target('" + tool + "',")
        content.append("             " + str(targets_in[tool]) + ")")
    else:
        content.append("   targets = None")
    content.append("")

    if mappings_in is not None and mappings_out is not None:
        content.append("   to_map = " + str(mappings_in))
        content.append("   from_map = " + str(mappings_out))
        content.append("   mappings = enrichwrap.add_mapping(to_map, from_map, '" + tool + "', False)")
    else:
        content.append("   mappings = None")
    content.append("")

    content.append("   val = enrichwrap.enrich('" + tool + "', sample_data, None, '" + http_addr + "', '" + http_port + "', targets, mappings)")
    content.append("   sas_data = val['sas_data']")
    content.append("   tool_data = val['tool_data']")
    content.append("   dict = str(sas_data)")
    content.append("   outputString = tool_data['" + tool + "']['result']")
    return '\n'.join(content)


def get_variables(sas_data):
    content = []
    bools = []
    ints = []
    strings = []
    # Find the booleans
    for key in sas_data.keys():
        val = sas_data[key]
        if isinstance(val, bool):
            bools.append("   " + key + " = (sas_data['" + key + "'] is True)")

    # Find the integers
    for key in sas_data.keys():
        val = sas_data[key]
        if isinstance(val, bool) == False and isinstance(val, int):
            ints.append("   " + key + " = sas_data['" + key + "']")

    # Find the strings
    for key in sas_data.keys():
        val = sas_data[key]
        if isinstance(val, str):
            strings.append("   " + key + " = sas_data['" + key + "']")

    if len(bools) > 0:
        content.append('   # Go to the Variables tab, and ensure the following are mapping to Boolean')
        content.append('   # Booleans')
        content.append('\n'.join(bools))
        content.append('')

    if len(ints) > 0:
        content.append('   # Go to the Variables tab, and ensure the following are mapping to Integer')
        content.append('   # Integers')
        content.append('\n'.join(ints))
        content.append('')

    if len(strings) > 0:
        content.append('   # Go to the Variables tab, and ensure the following are mapping to Strings')
        content.append('   # Strings')
        content.append('\n'.join(strings))
        content.append('')

    return '\n'.join(content)


def gen_structure(tool, mappings, sample_data=None, targets=None, mappings_in=None, mappings_out=None):
    starting_dir = os.path.dirname(__file__)
    IDFiles = starting_dir + os.path.sep + '..' + os.path.sep + 'ID_modules' + os.path.sep
    print('Content for structure will go here [%s]' % IDFiles)
    #list_samples = glob.glob(IDFiles + '*.*')

    bench_file = None
    filename = IDFiles + 'bench_' + tool + '.txt'
    if os.path.isfile(filename):
        bench_file = open(filename, 'r')
        bench = bench_file.read()
        bench_file.close()

    if mappings is not None:
        outgoing_data = enrich(tool, None, mappings)
    else:
        created_mappings = add_mapping(mappings_in, mappings_out, tool, False)
        outgoing_data = enrich(tool, sample_data, None, None, None, targets, created_mappings)

    sas_data = outgoing_data['sas_data']
    extra = 'choices,outputString,dict'

    id_content = ["import enrichwrap",
                  '',
                  "''' List all output parameters as comma-separated values in the \"Output:\" docString. Do not specify \"None\" if there is no output parameter. '''",
                  "def execute ():",
                  get_output_line(extra, sas_data),
                  get_starter_body(tool, '10.44.16.24', '8200', sample_data, targets, mappings_in, mappings_out),
                  '',
                  get_variables(sas_data),
                  get_return_line(extra, sas_data),
                  '']

    if bench is None:
        bench = open(filename, 'w')
        strcontent = '\n'.join(id_content)
        bench.write(strcontent)
        bench.close()
    elif bench != id_content:
        compare_file = open(IDFiles + 'compare_' + tool + '.txt', 'w')
        strcontent = '\n'.join(id_content)
        compare_file.write(strcontent)
        compare_file.close()

    return bench, '\n'.join(id_content)


