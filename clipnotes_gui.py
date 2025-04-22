import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QComboBox, QSpinBox, QTextEdit, QCheckBox, QLineEdit, QMessageBox
from PyQt5.QtCore import QTimer, Qt
import clipnotes
import traceback
import pyperclip  # Add this import

class ClipNotesGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.clipnotes_instance = None
        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self.update_clipboard)

    def initUI(self):
        self.setWindowTitle('ClipNotes GUI')
        self.setGeometry(100, 100, 600, 500)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Output file selection
        file_layout = QHBoxLayout()
        self.output_file_label = QLabel('Output File:')
        self.output_file_path = QLabel('clipboard_contents.txt')
        self.select_file_button = QPushButton('Select File')
        self.select_file_button.clicked.connect(self.select_output_file)
        file_layout.addWidget(self.output_file_label)
        file_layout.addWidget(self.output_file_path)
        file_layout.addWidget(self.select_file_button)
        layout.addLayout(file_layout)

        # Format selection
        format_layout = QHBoxLayout()
        format_label = QLabel('Output Format:')
        self.format_combo = QComboBox()
        self.format_combo.addItems(['txt', 'json', 'csv'])
        format_layout.addWidget(format_label)
        format_layout.addWidget(self.format_combo)
        layout.addLayout(format_layout)

        # Add output structure options
        self.include_timestamp = QCheckBox('Include Timestamps')
        self.include_source = QCheckBox('Include Source Window')
        layout.addWidget(self.include_timestamp)
        layout.addWidget(self.include_source)

        # JSON structure options
        json_structure_layout = QHBoxLayout()
        json_structure_label = QLabel('JSON Structure:')
        self.json_structure_combo = QComboBox()
        self.json_structure_combo.addItems(['content_only', 'content_time', 'full'])
        self.json_structure_combo.setEnabled(False)
        json_structure_layout.addWidget(json_structure_label)
        json_structure_layout.addWidget(self.json_structure_combo)
        layout.addLayout(json_structure_layout)

        # Connect format combo to enable/disable JSON structure
        self.format_combo.currentTextChanged.connect(self.on_format_changed)

        # Interval selection
        interval_layout = QHBoxLayout()
        interval_label = QLabel('Polling Interval (seconds):')
        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(1, 60)
        self.interval_spin.setValue(1)
        interval_layout.addWidget(interval_label)
        interval_layout.addWidget(self.interval_spin)
        layout.addLayout(interval_layout)

        # Deduplication limit
        dedup_layout = QHBoxLayout()
        dedup_label = QLabel('Deduplication Limit:')
        self.dedup_spin = QSpinBox()
        self.dedup_spin.setRange(1, 10000)
        self.dedup_spin.setValue(1000)
        dedup_layout.addWidget(dedup_label)
        dedup_layout.addWidget(self.dedup_spin)
        layout.addLayout(dedup_layout)

        # Encryption options
        encrypt_layout = QHBoxLayout()
        self.encrypt_checkbox = QCheckBox('Enable Encryption')
        self.encrypt_checkbox.stateChanged.connect(self.toggle_password_field)
        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setEnabled(False)
        encrypt_layout.addWidget(self.encrypt_checkbox)
        encrypt_layout.addWidget(self.password_label)
        encrypt_layout.addWidget(self.password_input)
        layout.addLayout(encrypt_layout)

        # Regex filtering options
        include_layout = QHBoxLayout()
        include_label = QLabel('Include Regex:')
        self.include_input = QLineEdit()
        include_layout.addWidget(include_label)
        include_layout.addWidget(self.include_input)
        layout.addLayout(include_layout)

        exclude_layout = QHBoxLayout()
        exclude_label = QLabel('Exclude Regex:')
        self.exclude_input = QLineEdit()
        exclude_layout.addWidget(exclude_label)
        exclude_layout.addWidget(self.exclude_input)
        layout.addLayout(exclude_layout)

        # Start/Stop button
        self.start_stop_button = QPushButton('Start Monitoring')
        self.start_stop_button.clicked.connect(self.toggle_monitoring)
        layout.addWidget(self.start_stop_button)

        # Status and last copied content
        self.status_label = QLabel('Status: Not monitoring')
        layout.addWidget(self.status_label)

        self.content_text = QTextEdit()
        self.content_text.setReadOnly(True)
        layout.addWidget(self.content_text)

    def select_output_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, 'Select Output File')
        if file_name:
            self.output_file_path.setText(file_name)

    def toggle_password_field(self, state):
        self.password_input.setEnabled(state == Qt.Checked)

    def toggle_monitoring(self):
        if self.clipnotes_instance is None:
            self.start_monitoring()
        else:
            self.stop_monitoring()

    def on_format_changed(self, format):
        self.json_structure_combo.setEnabled(format == 'json')

    def start_monitoring(self):
        try:
            output_file = self.output_file_path.text()
            format = self.format_combo.currentText()
            interval = self.interval_spin.value()
            dedup_limit = self.dedup_spin.value()
            encrypt = self.encrypt_checkbox.isChecked()
            password = self.password_input.text() if encrypt else None
            include_regex = self.include_input.text()
            exclude_regex = self.exclude_input.text()

            if encrypt and not password:
                raise ValueError("Password is required when encryption is enabled.")

            class Args:
                pass
            args = Args()
            args.output = output_file
            args.format = format
            args.interval = interval
            args.dedup_limit = dedup_limit
            args.separator = '---'
            args.encrypt = encrypt
            args.password = password
            args.include = include_regex
            args.exclude = exclude_regex
            args.include_timestamp = self.include_timestamp.isChecked()
            args.include_source = self.include_source.isChecked()
            args.json_structure = self.json_structure_combo.currentText()

            self.clipnotes_instance = clipnotes.ClipboardMonitor(args)
            self.clipnotes_instance.start()

            self.monitor_timer.start(interval * 1000)
            self.start_stop_button.setText('Stop Monitoring')
            self.status_label.setText('Status: Monitoring')
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start monitoring: {str(e)}")
            self.status_label.setText('Status: Error')
            traceback.print_exc()

    def stop_monitoring(self):
        try:
            if self.clipnotes_instance:
                self.clipnotes_instance.stop()
                self.clipnotes_instance = None
                # Copy the absolute path to clipboard
                output_path = os.path.abspath(self.output_file_path.text())
                pyperclip.copy(output_path)
                self.status_label.setText('Status: Not monitoring (file path copied to clipboard)')
            self.monitor_timer.stop()
            self.start_stop_button.setText('Start Monitoring')
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to stop monitoring: {str(e)}")
            traceback.print_exc()

    def update_clipboard(self):
        try:
            if self.clipnotes_instance:
                content = self.clipnotes_instance.last_entry
                if content:
                    self.content_text.setPlainText(f"Last copied:\n{content.timestamp}\n{content.window_info}\n{content.content}")
        except Exception as e:
            QMessageBox.warning(self, "Warning", f"Failed to update clipboard display: {str(e)}")
            traceback.print_exc()

    def closeEvent(self, event):
        try:
            self.stop_monitoring()
            event.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to close properly: {str(e)}")
            traceback.print_exc()
            event.accept()

def main():
    app = QApplication(sys.argv)
    ex = ClipNotesGUI()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"An unhandled error occurred: {str(e)}")
        traceback.print_exc()
        sys.exit(1)
        print(f"An unhandled error occurred: {str(e)}")

        traceback.print_exc()
        sys.exit(1)
