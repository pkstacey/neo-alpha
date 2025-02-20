from setuptools import setup, find_packages

setup(
    name="neo_midi_generator_alpha",
    version="0.1",
    description="Near Earth Objects MIDI Generator with NASA API integration",
    author="Patrick Stacey",
    packages=find_packages(),
    install_requires=[
        "PyQt5>=5.15.0",
        "mido>=1.2.9",
        "python-rtmidi>=1.4.7",  # Required backend for mido
        "requests>=2.25.1"
    ],
    entry_points={
        "console_scripts": [
            "neo_midi_generator_alpha=neo_midi_generator_alpha:main",
        ],
    },
)
