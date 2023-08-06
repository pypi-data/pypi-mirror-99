import setuptools

import pyhelpers

with open("README.rst", 'r', encoding='utf-8') as readme:
    long_description = readme.read()

setuptools.setup(

    name=pyhelpers.__package_name__,

    version=pyhelpers.__version__,

    description=pyhelpers.__description__,
    long_description=long_description,
    long_description_content_type="text/x-rst",

    url='https://github.com/mikeqfu/pyhelpers',

    author=pyhelpers.__author__,
    author_email=pyhelpers.__email__,

    license='GPLv2',

    classifiers=[
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',

        'Topic :: Education',
        'Topic :: Scientific/Engineering',
        'Topic :: Utilities',

        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',

        'Programming Language :: Python :: 3',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
    ],

    keywords=['python', 'helper functions', 'utilities'],

    project_urls={
        'Documentation': 'https://pyhelpers.readthedocs.io/en/latest/',
        'Source': 'https://github.com/mikeqfu/pyhelpers',
        'Tracker': 'https://github.com/mikeqfu/pyhelpers/issues',
    },

    packages=setuptools.find_packages(exclude=["*.tests", "tests.*", "tests"]),

    install_requires=[
        'fake-useragent',
        'fuzzywuzzy',
        # 'gdal',
        # 'matplotlib',
        # 'nltk',
        'numpy',
        'openpyxl',
        'pandas',
        # 'pdfkit',
        'psycopg2',
        'python-rapidjson',
        # 'python-Levenshtein',
        'pyproj',
        'pyxlsb',
        'requests',
        'scipy',
        'shapely',
        'sqlalchemy~=1.3.23',
        'sqlalchemy-utils',
        'tqdm',
        'xlrd',
        'XlsxWriter',
    ],

    package_data={"": ["requirements.txt", "LICENSE"]},
    include_package_data=True,

)
