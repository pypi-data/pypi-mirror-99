"""
Search Variables
"""

def _vp_load_dir(var=''):
    """
    load Variables with dir(globals)
    """
    _VP_NOT_USING_VAR = ['_html', '_nms', 'NamespaceMagics', '_Jupyter', 'In', 'Out', 'exit', 'quit', 'get_ipython']
    _vp_vars = []
    result = {}
    if var == '':
        _vp_vars = sorted(globals())
        result = { 'type': 'None', 'list': [{'name': v, 'type': type(eval(v)).__name__} for v in _vp_vars if (not v.startswith('_')) and (v not in _VP_NOT_USING_VAR)] }
    else:
        _vp_vars = dir(eval(var))
        result = { 'type': type(eval(var)).__name__, 'list': [{'name': v, 'type': type(eval(var + '.' + v)).__name__} for v in _vp_vars if (not v.startswith('_')) and (v not in _VP_NOT_USING_VAR)] }
    return result

def _vp_get_type(var == ''):
    """
    get type name
    """
    if var == '':
        return 'None'
    return type(var).__name__