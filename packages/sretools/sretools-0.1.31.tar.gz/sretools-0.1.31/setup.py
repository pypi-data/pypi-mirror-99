import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="sretools",
    version="0.1.31",
    description="SRE console/terminal toolbox",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/laowangv5/sretools",
    author="Yonghang Wang",
    author_email="wyhang@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],
    packages=["sretools"],
    include_package_data=True,
    install_requires=["pexpect","texttable","wcwidth","pyyaml","jaydebeapi","psutil"],
    keywords=['sretool','sre','ssh','yssh','pssh','ltexpect','expect','incident','postmortem','json2html','json','html','yaml','jdbc','dbx','dbquery'],
    entry_points={
        "console_scripts": [
            "sretools-ssh=sretools.yssh:main",
            "sretools-expect=sretools.ltexpect:main",
            #"sretools-incident=sretools.incident:main",
            "sretools-nonascii=sretools.nonascii:main",
            "sretools-table-format=sretools.tblfmt:main",
            "sretools-csv-format=sretools.csvfmt:main",
            "sretools-json2html=sretools.json2html:main",
            "sretools-json2yaml=sretools.json2yaml:main",
            "sretools-yaml2json=sretools.yaml2json:main",
            "sretools-yaml2html=sretools.yaml2html:main",
            #"sretools-jdbc-call=sretools.jdbc_call:main",
            "sretools-dbx=sretools.dbx:main",
        ]
    },
)
