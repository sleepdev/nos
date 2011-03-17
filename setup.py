from distutils.core import setup

setup(
    name="nosqlsql",
    py_modules=['nosqlsql'],
    data_files=[('/etc/nosqlsql',['dbconf.json'])],
)
