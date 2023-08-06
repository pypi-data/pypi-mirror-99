from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Repeater to use in messages'
LONG_DESCRIPTION = 'Repeater that can repeat a word so many times'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="sparksrepeater", 
        version=VERSION,
        author="Sourya Sparks",
        author_email="vzoid8@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        
        
        keywords=['python', 'repeater'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
