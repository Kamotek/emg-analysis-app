from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

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
        layout.addWidget(self.sample_rate_label)
        layout.addWidget(self.sample_rate_input)

        # Channel Mask
        self.channel_mask_label = QLabel("Channel Mask (Hex):")
        self.channel_mask_input = QLineEdit()
        self.channel_mask_input.setPlaceholderText("e.g., 0xFF")
        self.channel_mask_input.setText("0xFF")  # Example value
        layout.addWidget(self.channel_mask_label)
        layout.addWidget(self.channel_mask_input)

        # Data Length
        self.data_length_label = QLabel("Data Length:")
        self.data_length_input = QLineEdit()
        self.data_length_input.setPlaceholderText("e.g., 128")
        self.data_length_input.setText("128")  # Example value
        layout.addWidget(self.data_length_label)
        layout.addWidget(self.data_length_input)

        # Resolution
        self.resolution_label = QLabel("Resolution (bits):")
        self.resolution_input = QLineEdit()
        self.resolution_input.setPlaceholderText("e.g., 8")
        self.resolution_input.setText("8")  # Example value
        layout.addWidget(self.resolution_label)
        layout.addWidget(self.resolution_input)

        # OK button
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

    def get_values(self):
        return {
            'sample_rate': int(self.sample_rate_input.text()),
            'channel_mask': int(self.channel_mask_input.text(), 16),  # Assuming hex input
            'data_length': int(self.data_length_input.text()),
            'resolution': int(self.resolution_input.text())
        }
