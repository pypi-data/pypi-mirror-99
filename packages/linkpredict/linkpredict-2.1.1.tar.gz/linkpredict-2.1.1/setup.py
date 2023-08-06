from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="linkpredict",
    version="2.1.1",
    author="Jona Saffer, Artur Scholz, Shayan Majumder",
    description="A generic and dynamic link budget tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/librecube/lib/python-linkpredict",
    license="MIT",
    python_requires='>=3.4',
    packages=find_packages(),
    install_requires=['numpy', 'scipy', 'skyfield'],
)
