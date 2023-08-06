from setuptools import setup, find_packages

VERSION = '0.0.8' 
DESCRIPTION = 'gnani_rest_api'
LONG_DESCRIPTION = 'This is a rest api for transcription of audio to text'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="gnani-ats-rest-ap", 
        version=VERSION,
        author="Sandeep S",
        author_email="<sandeep.s@gnani.ai>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], 
        
        keywords=['python', 'automatic text to speech'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
