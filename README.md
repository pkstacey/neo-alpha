Near Earth Objects MIDI Generator

A fun Python application that integrates NASA's API data with MIDI generation. This app fetches data from NASA, then uses that information to drive a MIDI note generator, complete with a promotional graphic and live log display.

Features

NASA API Integration: Fetch data from NASA APIs (e.g., Near-Earth Object feed, Mars Rover Photos, Astronomy Picture of the Day).
MIDI Generation: Convert NASA data into MIDI notes using a user-selected key, note range, velocity, and tempo.
Live Log Display: See real-time logs of MIDI note events.
Graphical Promo: Displays a promotional image (make sure neo_promo_graphic.png is in the working directory).
User-Friendly UI: Built with PyQt5.
Threaded MIDI Generation: Runs in a separate thread for a responsive GUI.
Easy Setup: Dependencies are managed via a setup.py script.
Prerequisites

Before using the application, ensure you have:

Python 3 installed.
A NASA API account.
You can sign up for a free API key at https://api.nasa.gov.
Installation

There are two ways to install the required dependencies:

Option 1: Using pip install -r requirements.txt
pip install -r requirements.txt
Option 2: Using setup.py
Package the project and install with:

pip install .
This will install the application along with all necessary dependencies (PyQt5, mido, python-rtmidi, and requests).

Configuration

NASA API Key:
When you first run the application, you will need to enter your NASA API key. If you don’t have one yet, visit https://api.nasa.gov to create an account and get your key.

Other Settings:
Configure the MIDI output port, date range, MIDI note/velocity range, key, and tempo through the UI. You can save your settings for future sessions.
Usage

Run the application from command line with:

python neo_midi_generator_alpha.py

Controls:
Save Settings: Save your current configuration.
Clear Display: Clear the MIDI log output.
Start MIDI Generation: Begin generating MIDI notes based on NASA data.
Stop MIDI Generation: Stop the MIDI generation process.
Project Structure

neo_midi_generator.py: Main application script containing the PyQt5 UI and MIDI generation logic.
neo_promo_graphic.png: Promotional image displayed in the application. Ensure this file is in the same directory as the main script.
setup.py: Packaging script to help with dependency installation.
requirements.txt: List of Python dependencies required by the project.
config.json: Configuration file used to save settings (created automatically after you save your settings).
Contributing

Contributions, issues, and feature requests are welcome! 

Use Github or paypal for donations.

License:

See LICENSE for more information.

Copyright (C) 2025 Dr Patrick Stacey
Email: pkstacey@gmail.com
