import os

def get_project_root()->str:
    abspath = os.path.abspath(__file__)
    dirname = os.path.dirname(abspath)
    dirname2 = os.path.dirname(dirname)
    return dirname2

def get_abs_path(relative_path:str)->str:
    return os.path.abspath(os.path.join(get_project_root(), relative_path))
