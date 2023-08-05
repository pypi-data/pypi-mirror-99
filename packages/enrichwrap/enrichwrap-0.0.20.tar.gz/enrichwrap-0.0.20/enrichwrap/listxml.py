import glob
import os


def print_contents ():
    starting_dir = os.path.dirname(__file__)
    print('__file__ contents: ', end=' ')
    print(glob.glob(starting_dir + '*.*'))

    print('__file__/samples contents: ', end=' ')
    print(glob.glob(starting_dir + os.path.sep +  'samples' + os.path.sep + '*.*'))

    print('__file__/xml contents: ', end = ' ')
    print(glob.glob(starting_dir + os.path.sep + 'xml' + os.path.sep +  '*.*'))


if __name__ == "__main__":
    print_contents()
