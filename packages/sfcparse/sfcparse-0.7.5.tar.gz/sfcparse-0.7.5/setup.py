from setuptools import setup

VERSION = '0.7.5'
DESCRIPTION = 'Simple File Configuration Parse. Python alternative to creating custom save/config files!'

# Import README
with open('.\\README.md', 'r') as f:
    LONG_DESCRIPTION = f.read()

# Setup
setup(
    name="sfcparse",
    version=VERSION,
    url="https://github.com/aaronater10/sfcparse",
    author="aaronater10",
    author_email="admin@dunnts.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    py_modules=['sfcparse'],
    package_dir={'': 'src'},
    install_requires=[],
    keywords=['python', 'ini file', 'config', 'text file', 'cfg', 'conf', 'save file', 'config file', 'sfcparse', 'aaronater10', 'db', 'database', 'simple', 'configuration', 'alternative', 'data', 'import'],
    license = 'MIT',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)