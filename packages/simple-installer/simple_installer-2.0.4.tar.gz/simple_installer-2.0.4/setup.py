from setuptools import setup, find_packages


VERSION = '2.0.4'
DESCRIPTION = 'Extandable installer for Github release zip files.'
LONG_DESCRIPTION = 'A package that allows to build simple installer to download Github realease source zip or assets'

# Setting up
setup(
    name="simple_installer",
    version=VERSION,
    author="Dmitrii Shevchenko",
    author_email="<dmitrii.shevchenko96@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['PySide2', 'requests', 'PyGithub', 'elevate'],
    keywords=['python', 'installer', 'github'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
