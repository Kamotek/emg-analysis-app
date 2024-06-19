from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox
from PySide6.QtGui import QColor

class EMGConfigDialog(QDialog):
    def __init__(self, parent=None):
        super(EMGConfigDialog, self).__init__(parent)
        self.setWindowTitle("Configure EMG Settings")

        # Set layout
        layout = QVBoxLayout()

        # Sample Rate
        self.sample_rate_label = QLabel("Sample Rate (Hz):")
        self.sample_rate_input = QLineEdit()
        self.sample_rate_input.setPlaceholderText("e.g., 500")
        self.sample_rate_input.setText("500")  # Example value
        self.sample_rate_label.setStyleSheet("color: white;")  # Set white font color
        self.sample_rate_input.setStyleSheet("color: white;")  # Set white font color
        layout.addWidget(self.sample_rate_label)
        layout.addWidget(self.sample_rate_input)

        # Channel Mask
        self.channel_mask_label = QLabel("Channel Mask (Hex):")
        self.channel_mask_input = QLineEdit()
        self.channel_mask_input.setPlaceholderText("e.g., 0xFF")
        self.channel_mask_input.setText("0xFF")  # Example value
        self.channel_mask_label.setStyleSheet("color: white;")  # Set white font color
        self.channel_mask_input.setStyleSheet("color: white;")  # Set white font color
        layout.addWidget(self.channel_mask_label)
        layout.addWidget(self.channel_mask_input)

        # Data Length
        self.data_length_label = QLabel("Data Length:")
        self.data_length_input = QLineEdit()
        self.data_length_input.setPlaceholderText("e.g., 128")
        self.data_length_input.setText("128")  # Example value
        self.data_length_label.setStyleSheet("color: white;")  # Set white font color
        self.data_length_input.setStyleSheet("color: white;")  # Set white font color
        layout.addWidget(self.data_length_label)
        layout.addWidget(self.data_length_input)

        # Resolution
        self.resolution_label = QLabel("Resolution (bits):")
        self.resolution_input = QLineEdit()
        self.resolution_input.setPlaceholderText("e.g., 8")
        self.resolution_input.setText("8")  # Example value
        self.resolution_label.setStyleSheet("color: white;")  # Set white font color
        self.resolution_input.setStyleSheet("color: white;")  # Set white font color
        layout.addWidget(self.resolution_label)
        layout.addWidget(self.resolution_input)

        # Gender
        self.gender_label = QLabel("Gender:")
        self.gender_combobox = QComboBox()
        self.gender_combobox.addItems(["Male", "Female", "Other"])
        self.gender_label.setStyleSheet("color: white;")  # Set white font color
        self.gender_combobox.setStyleSheet("color: white;")  # Set white font color
        layout.addWidget(self.gender_label)
        layout.addWidget(self.gender_combobox)

        # Age
        self.age_label = QLabel("Age:")
        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("e.g., 30")
        self.age_label.setStyleSheet("color: white;")  # Set white font color
        self.age_input.setStyleSheet("color: white;")  # Set white font color
        layout.addWidget(self.age_label)
        layout.addWidget(self.age_input)

        # Height
        self.height_label = QLabel("Height (cm):")
        self.height_input = QLineEdit()
        self.height_input.setPlaceholderText("e.g., 175")
        self.height_label.setStyleSheet("color: white;")  # Set white font color
        self.height_input.setStyleSheet("color: white;")  # Set white font color
        layout.addWidget(self.height_label)
        layout.addWidget(self.height_input)

        # Weight
        self.weight_label = QLabel("Weight (kg):")
        self.weight_input = QLineEdit()
        self.weight_input.setPlaceholderText("e.g., 70")
        self.weight_label.setStyleSheet("color: white;")  # Set white font color
        self.weight_input.setStyleSheet("color: white;")  # Set white font color
        layout.addWidget(self.weight_label)
        layout.addWidget(self.weight_input)

        # OK button
        self.ok_button = QPushButton("OK")
        self.ok_button.setStyleSheet("color: white;")  # Set white font color
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

    def get_values(self):
        return {
            'sample_rate': int(self.sample_rate_input.text()),
            'channel_mask': int(self.channel_mask_input.text(), 16),  # Assuming hex input
            'data_length': int(self.data_length_input.text()),
            'resolution': int(self.resolution_input.text()),
            'gender': self.gender_combobox.currentText(),
            'age': int(self.age_input.text()),
            'height': int(self.height_input.text()),
            'weight': int(self.weight_input.text())
        }
