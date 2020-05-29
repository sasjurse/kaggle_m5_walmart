from pathlib import Path


def raw_data_folder():
    tmp = Path('../raw_data')
    tmp = tmp.resolve()
    return tmp


def plots_folder():
    tmp = Path('../raw_data')
    tmp = tmp.resolve()
    return tmp
