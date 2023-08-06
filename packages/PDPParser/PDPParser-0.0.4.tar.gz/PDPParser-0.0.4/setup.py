from setuptools import setup, find_packages

VERSION = '0.0.4'
DESCRIPTION = 'Simple package to help parse PDP on Footsites!'

# Setting up
setup(
    name="PDPParser",
    version=VERSION,
    author="Mrbeastmode",
    description=DESCRIPTION,
    long_description="Check https://github.com/MrbeastmodeXD/PDP-Parser for documentation! : D",
    packages=find_packages(),
    keywords=['python', 'pdp', 'footlocker'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)