import glob
import os
from pathlib import Path

from enrichwrap import MasLog


def print_contents ():
    _masLog = MasLog()
    starting_dir = os.path.dirname(__file__)
    _masLog.info('__file__ contents: ')
    list_main = glob.glob(starting_dir + '*.*')
    for i in list_main:
        _masLog.info('\t' + i[len(starting_dir):])
    _masLog.info()

    _masLog.info('__file__' + os.path.sep + 'samples contents: ')
    samples = starting_dir + os.path.sep + 'samples' + os.path.sep
    list_samples = glob.glob(samples + '*.*')
    for i in list_samples:
        _masLog.info('\t' + i[len(samples):])
    _masLog.info()

    _masLog.info('__file__' + os.path.sep + 'xml contents: ')
    xmls = starting_dir + os.path.sep + 'xml' + os.path.sep
    list_xml = glob.glob(xmls + '*.*')
    for i in list_xml:
        _masLog.info('\t' + i[len(xmls):])


def get_xml_files():
    starting_dir = os.path.dirname(__file__)
    xmls = starting_dir + os.path.sep + 'xml' + os.path.sep
    list_xml = glob.glob(xmls + '*.*')
    list_clean = []
    for i in list_xml:
        list_clean.append(i[len(xmls):])
    return list_clean


def get_sample_files():
    starting_dir = os.path.dirname(__file__)
    samples = starting_dir + os.path.sep +  'samples' + os.path.sep
    list_samples = glob.glob(samples + '*.*')
    list_clean = []
    for i in list_samples:
        list_clean.append(i[len(samples):])
    return list_clean


def get_contents(dirname, filename):
    starting_dir = os.path.dirname(__file__)
    file_loc = starting_dir + os.path.sep + dirname + os.path.sep + filename
    if os.path.isfile(file_loc):
        return file_loc
    return None


if __name__ == "__main__":
    print_contents()
