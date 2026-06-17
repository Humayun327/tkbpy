import importlib.metadata

def get_plugins():
    """Finds all installed packages starting with 'tkbpy-'"""
    plugins = []
    for dist in importlib.metadata.distributions():
        name = dist.metadata['Name']
        if name.startswith("tkbpy-") and name != "tkbpy":
            plugins.append(name)
    return plugins