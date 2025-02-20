"""
Copyright (C) 2025 Dr Patrick Stacey
Email: pkstacey@gmail.com
 
This project is licensed under the NEO Non-Commercial License. See LICENSE for details.
"""

import json
import random
import time
import requests
import mido
import threading
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QTextEdit,
    QFormLayout,
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

# Constants
DEFAULTS_FILE = "defaults.json"
CONFIG_FILE = "config.json"

NASA_APIS = {
    "Near-Earth Object (NEO)": "https://api.nasa.gov/neo/rest/v1/feed",
    "Mars Rover Photos": "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos",
    "Astronomy Picture of the Day (APOD)": "https://api.nasa.gov/planetary/apod",
}

key_notes_dict = {
    "C": [60, 62, 64, 65, 67, 69, 71, 72],
    "D": [62, 64, 66, 67, 69, 71, 73, 74],
    "E": [64, 66, 68, 69, 71, 73, 75, 76],
    "F": [65, 67, 69, 70, 72, 74, 76, 77],
    "G": [67, 69, 71, 72, 74, 76, 78, 79],
    "A": [69, 71, 73, 74, 76, 78, 80, 81],
    "B": [71, 73, 75, 76, 78, 80, 82, 83],
}


class AppWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Near Earth Objects - MIDI Generator")
        self.setGeometry(100, 100, 800, 600)
        self.midi_thread = None
        self.stop_midi_flag = False

        # Main layout: split horizontally into left (display) and right (settings)
        self.main_layout = QHBoxLayout()

        # Left Section: Vertical split for promo graphic and log output
        self.left_layout = QVBoxLayout()

        # Top: Promotional PNG Graphic
        self.promo_label = QLabel()
        self.promo_label.setFixedHeight(200)
        self.promo_label.setAlignment(Qt.AlignCenter)
        # Load and scale the image to the fixed height, preserving aspect ratio
        pixmap = QPixmap("neo_promo_graphic.png")
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaledToHeight(200, Qt.SmoothTransformation)
            self.promo_label.setPixmap(scaled_pixmap)
        else:
            self.promo_label.setText("Promo graphic not found.")
        self.left_layout.addWidget(self.promo_label)

        # Bottom: Log output (MIDI note log)
        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)
        self.left_layout.addWidget(self.output_display)

        self.main_layout.addLayout(self.left_layout)

        # Right Section: Settings
        self.settings_layout = QVBoxLayout()

        # Title
        self.title_label = QLabel("<h1>Near Earth Objects</h1>")
        self.settings_layout.addWidget(self.title_label)

        # NASA API Key
        self.api_key_label = QLabel("NASA API Key:")
        self.api_key_input = QLineEdit()
        self.settings_layout.addWidget(self.api_key_label)
        self.settings_layout.addWidget(self.api_key_input)

        # API Selection
        self.api_select_label = QLabel("Select NASA API:")
        self.api_dropdown = QComboBox()
        self.api_dropdown.addItems(NASA_APIS.keys())
        self.settings_layout.addWidget(self.api_select_label)
        self.settings_layout.addWidget(self.api_dropdown)

        # MIDI Output Port
        self.midi_label = QLabel("MIDI Output Port:")
        self.midi_dropdown = QComboBox()
        self.midi_dropdown.addItems(mido.get_output_names())
        self.settings_layout.addWidget(self.midi_label)
        self.settings_layout.addWidget(self.midi_dropdown)

        # Date Range
        self.start_date_label = QLabel("Data Start Date (YYYY-MM-DD):")
        self.start_date_input = QLineEdit("2024-01-01")
        self.settings_layout.addWidget(self.start_date_label)
        self.settings_layout.addWidget(self.start_date_input)

        self.end_date_label = QLabel("Data End Date (YYYY-MM-DD):")
        self.end_date_input = QLineEdit("2024-01-07")
        self.settings_layout.addWidget(self.end_date_label)
        self.settings_layout.addWidget(self.end_date_input)

        # MIDI Note Range
        self.note_range_label = QLabel("MIDI Note Range:")
        self.note_range_layout = QFormLayout()
        self.min_note_input = QLineEdit("60")
        self.max_note_input = QLineEdit("72")
        self.note_range_layout.addRow("Min Note:", self.min_note_input)
        self.note_range_layout.addRow("Max Note:", self.max_note_input)
        self.settings_layout.addWidget(self.note_range_label)
        self.settings_layout.addLayout(self.note_range_layout)

        # MIDI Velocity Range
        self.velocity_range_label = QLabel("MIDI Velocity Range:")
        self.velocity_range_layout = QFormLayout()
        self.min_velocity_input = QLineEdit("64")
        self.max_velocity_input = QLineEdit("127")
        self.velocity_range_layout.addRow("Min Velocity:", self.min_velocity_input)
        self.velocity_range_layout.addRow("Max Velocity:", self.max_velocity_input)
        self.settings_layout.addWidget(self.velocity_range_label)
        self.settings_layout.addLayout(self.velocity_range_layout)

        # Key Signature
        self.ks_select_label = QLabel("Select Key:")
        self.ks_dropdown = QComboBox()
        self.ks_dropdown.addItems(key_notes_dict.keys())
        self.settings_layout.addWidget(self.ks_select_label)
        self.settings_layout.addWidget(self.ks_dropdown)

        # Tempo
        self.tempo_key_label = QLabel("Tempo (BPM):")
        self.tempo_key_input = QLineEdit("120")
        self.settings_layout.addWidget(self.tempo_key_label)
        self.settings_layout.addWidget(self.tempo_key_input)

        # Buttons
        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.save_settings)
        self.settings_layout.addWidget(self.save_button)

        # Clear Display button (to clear the log output)
        self.clear_button = QPushButton("Clear Display")
        self.clear_button.clicked.connect(self.clear_display)
        self.settings_layout.addWidget(self.clear_button)

        self.start_button = QPushButton("Start MIDI Generation")
        self.start_button.clicked.connect(self.start_midi_generation)
        self.settings_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop MIDI Generation")
        self.stop_button.clicked.connect(self.stop_midi_generation)
        self.settings_layout.addWidget(self.stop_button)

        self.main_layout.addLayout(self.settings_layout)
        self.setLayout(self.main_layout)

        # Load defaults if available
        self.load_settings()

    def load_settings(self):
        try:
            with open(CONFIG_FILE, "r") as file:
                config = json.load(file)
                self.api_key_input.setText(config.get("api_key", ""))
                self.api_dropdown.setCurrentText(config.get("selected_api", ""))
                self.midi_dropdown.setCurrentText(config.get("selected_midi_port", ""))
                self.start_date_input.setText(config.get("start_date", "2024-01-01"))
                self.end_date_input.setText(config.get("end_date", "2024-01-07"))
                self.min_note_input.setText(str(config.get("min_midi_note", 60)))
                self.max_note_input.setText(str(config.get("max_midi_note", 72)))
                self.min_velocity_input.setText(str(config.get("min_midi_velocity", 64)))
                self.max_velocity_input.setText(str(config.get("max_midi_velocity", 127)))
                self.ks_dropdown.setCurrentText(config.get("key", "C"))
                self.tempo_key_input.setText(str(config.get("tempo", 120)))
        except FileNotFoundError:
            self.output_display.append("No saved settings found. Please configure.")

    def save_settings(self):
        config = {
            "api_key": self.api_key_input.text(),
            "selected_api": self.api_dropdown.currentText(),
            "selected_midi_port": self.midi_dropdown.currentText(),
            "start_date": self.start_date_input.text(),
            "end_date": self.end_date_input.text(),
            "min_midi_note": int(self.min_note_input.text()),
            "max_midi_note": int(self.max_note_input.text()),
            "min_midi_velocity": int(self.min_velocity_input.text()),
            "max_midi_velocity": int(self.max_velocity_input.text()),
            "key": self.ks_dropdown.currentText(),
            "tempo": int(self.tempo_key_input.text()),
        }
        with open(CONFIG_FILE, "w") as file:
            json.dump(config, file, indent=4)
        self.output_display.append("Settings saved successfully.")

    def clear_display(self):
        self.output_display.clear()

    def fetch_nasa_data(self, api_url, api_key, start_date, end_date):
        try:
            params = {"api_key": api_key, "start_date": start_date, "end_date": end_date}
            response = requests.get(api_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.output_display.append(f"Error fetching data from NASA API: {e}")
            return None

    def run_midi_generation(self, api_key, selected_api, midi_port, start_date, end_date,
                              min_note, max_note, min_velocity, max_velocity, key, tempo):
        self.output_display.append(f"Fetching data from {selected_api}...")
        api_url = NASA_APIS[selected_api]
        data = self.fetch_nasa_data(api_url, api_key, start_date, end_date)
        if not data:
            self.output_display.append("No data fetched. Exiting MIDI generation.")
            return

        try:
            midi_out = mido.open_output(midi_port)
            self.output_display.append(f"Connected to MIDI port: {midi_port}")
        except Exception as e:
            self.output_display.append(f"Error connecting to MIDI port: {e}")
            return

        self.output_display.append("Generating MIDI notes...")
        key_notes = key_notes_dict[key]
        beat_duration = 60.0 / tempo  # Duration of one beat in seconds

        self.stop_midi_flag = False
        try:
            while not self.stop_midi_flag:
                note = random.choice(key_notes)
                velocity = random.randint(min_velocity, max_velocity)
                duration = beat_duration * random.uniform(0.5, 1.5)
                midi_out.send(mido.Message("note_on", note=note, velocity=velocity))
                self.output_display.append(f"Note On: {note}, Velocity: {velocity}")
                time.sleep(duration)
                midi_out.send(mido.Message("note_off", note=note))
                self.output_display.append(f"Note Off: {note}")
        except Exception as e:
            self.output_display.append(f"Error during MIDI generation: {e}")
        finally:
            midi_out.close()
            self.output_display.append("MIDI generation stopped. MIDI port closed.")

    def start_midi_generation(self):
        try:
            api_key = self.api_key_input.text()
            selected_api = self.api_dropdown.currentText()
            midi_port = self.midi_dropdown.currentText()
            start_date = self.start_date_input.text()
            end_date = self.end_date_input.text()
            min_note = int(self.min_note_input.text())
            max_note = int(self.max_note_input.text())
            min_velocity = int(self.min_velocity_input.text())
            max_velocity = int(self.max_velocity_input.text())
            key = self.ks_dropdown.currentText()
            tempo = int(self.tempo_key_input.text())

            if not api_key:
                self.output_display.append("Error: NASA API Key is required.")
                return

            self.midi_thread = threading.Thread(
                target=self.run_midi_generation,
                args=(api_key, selected_api, midi_port, start_date, end_date,
                      min_note, max_note, min_velocity, max_velocity, key, tempo)
            )
            self.midi_thread.start()
        except ValueError:
            self.output_display.append("Error: Invalid input in MIDI note range, velocity, or tempo fields.")

    def stop_midi_generation(self):
        self.stop_midi_flag = True
        self.output_display.append("Stop signal sent. Waiting for MIDI generation to halt...")
        if self.midi_thread:
            self.midi_thread.join()
            self.output_display.append("MIDI generation thread has stopped.")
            self.midi_thread = None


if __name__ == "__main__":
    app = QApplication([])
    window = AppWindow()
    window.show()
    app.exec_()
