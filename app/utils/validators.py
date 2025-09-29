def parse_int(value, default=None, min_val=None, max_val=None):
    try:
        iv = int(value)
        if min_val is not None and iv < min_val: return default
        if max_val is not None and iv > max_val: return default
        return iv
    except:
        return default

def parse_float(value, default=None, min_val=None, max_val=None):
    try:
        fv = float(value)
        if min_val is not None and fv < min_val: return default
        if max_val is not None and fv > max_val: return default
        return fv
    except:
        return default
