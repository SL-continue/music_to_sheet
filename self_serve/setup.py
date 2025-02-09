from setuptools import setup, find_packages

setup(
    name="music_to_sheet",  # Package name
    version="0.1.0",          # Version number
    author="Junyi Liu",       # Your name
    description="A tool to convert music into MIDI sheets using AI.",
    long_description=open("README.md").read(),  # Reads from a README file
    long_description_content_type="text/markdown",
    url="https://github.com/SL-continue/music_to_sheet",  # Project repo (if applicable)
    packages=find_packages(),  # Automatically find all packages
    install_requires=[  # Dependencies
        "basic-pitch",
        "music21",
        "streamlit"
    ],
    classifiers=[  # Metadata
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8, < 3.11",  # Other version not sure
)

