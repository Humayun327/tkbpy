from setuptools import setup, find_packages

setup(
    name="tkbpy",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # If your framework needs other libraries (like Flask or Click), 
        # list them here later.
    ],
    entry_points={
        "console_scripts": [
            "tkbpy=tkbpy.cli:handle_args_from_terminal",
        ],
    },
)