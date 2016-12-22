def not_none(obj):
    return obj is not None

def get(obj, selector):
    from pyjq import first
    return first(selector, obj)
