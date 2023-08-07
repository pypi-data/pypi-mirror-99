import setuptools

with open("README.MD", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='trainmote-module_felix-nievelstein_de',    
    version='0.5.24',
    description='Application to create a web server to control a model train environment',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/FelixNievelstein/Trainmote-Server",
    author='Felix Nievelstein',
    author_email='app@felix-nievelstein.de',
    package_dir={'': 'src'},
    packages=[
        'pkg_trainmote',
        'pkg_trainmote.models',
        'pkg_trainmote.validators',
        'pkg_trainmote.actions'
    ],
    package_data={
        "pkg_trainmote": ["scripts/*.sh", "schemes/*.json"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux"
    ],
    install_requires=[
        'adafruit-circuitpython-ads1x15',
        'PyBluez',
        'RPI.GPIO',
        'adafruit-blinka',
        'flask',
        'jsonschema',
        'Flask-HTTPAuth',
        'python-statemachine'
    ],
    entry_points={
        'console_scripts': [
            'trainmote = pkg_trainmote.trainmote:main',
        ]
    },
    python_requires='>=3, <4',
    data_files=[('content/', [])]
)
