"""
Search Variables
"""

def _vp_load_instance(var=''):
    """
    load Variables with dir(globals)
    """
    _VP_NOT_USING_VAR = ['_html', '_nms', 'NamespaceMagics', '_Jupyter', 'In', 'Out', 'exit', 'quit', 'get_ipython']
    varList = []
    query = ''
    result = {}
    if var == '':
        varList = sorted(globals())
        # result = { 'type': 'NoneType', 'list': [{'name': v, 'type': type(eval(v)).__name__} for v in _vp_vars if (not v.startswith('_')) and (v not in _VP_NOT_USING_VAR)] }
        result = {'type': 'NoneType', 'list': []}
    else:
        varList = dir(eval(var))
        query = var + '.'
        # result = { 'type': type(eval(var)).__name__, 'list': [{'name': v, 'type': type(eval(var + '.' + v)).__name__} for v in _vp_vars if (not v.startswith('_')) and (v not in _VP_NOT_USING_VAR)] }
        result = {'type': type(eval(var)).__name__, 'list': []}

    tmpList = []
    for v in varList:
        try:
            if (not v.startswith('_')) and (v not in _VP_NOT_USING_VAR):
                tmpList.append({'name': v, 'type': type(eval(query + v)).__name__ })
        except Exception as e:
            continue
    result['list'] = tmpList

    return result

def _vp_get_type(var=None):
    """
    get type name
    """
    return str(type(var).__name__)