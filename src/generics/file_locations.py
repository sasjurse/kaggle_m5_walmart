from pathlib import Path


def _search_for_root(path):
    tmp = path / 'src'
    if not tmp.exists():
        return _search_for_root(tmp.parent)
    else:
        return path


def raw_data_folder():
    root = _search_for_root(Path.cwd())
    return root / 'raw_data'


def plots_folder():
    root = _search_for_root(Path.cwd())
    return root / 'plots'


def sql_folder():
    root = _search_for_root(Path.cwd())
    return root / 'src' / 'sql'
