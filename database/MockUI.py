from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel


class MockUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('EMG Configuration and Data Display')

        layout = QVBoxLayout()

        self.label = QLabel('EMG Data Display')
        layout.addWidget(self.label)

        self.configButton = QPushButton('Configure EMG')
        self.configButton.clicked.connect(self.configure_emg)
        layout.addWidget(self.configButton)

        self.importButton = QPushButton('Import Database')
        self.importButton.clicked.connect(self.import_database)
        layout.addWidget(self.importButton)

        self.exportButton = QPushButton('Export Database')
        self.exportButton.clicked.connect(self.export_database)
        layout.addWidget(self.exportButton)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def configure_emg(self):
        # Add your EMG configuration code here
        print('Configuring EMG...')

    def import_database(self):
        # Add your database import code here
        print('Importing database...')

    def export_database(self):
        # Add your database export code here
        print('Exporting database...')

