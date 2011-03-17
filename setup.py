from distutils.core import setup

setup(
    name="nos",
    py_modules=['nos'],
    data_files=[('/etc/nos',['dbconf.json'])],
)
