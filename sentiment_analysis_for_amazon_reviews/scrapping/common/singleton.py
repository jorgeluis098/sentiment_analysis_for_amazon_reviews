
def singleton(cls):
    """
    This is a funtion to decorate any class to make it singleton.
    Returns:
        object: Instance of class.
    """    
    instances = dict()
    def wrap(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrap