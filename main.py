import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QFileDialog,
    QListWidget,
    QHBoxLayout,
    QGroupBox,
    QComboBox,
    QLabel,
    QAbstractItemView,
)
from PySide6.QtCore import Qt
import pandas as pd


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CSV Merger Tool")
        self.setGeometry(100, 100, 800, 600)

        main_layout = QVBoxLayout()

        # Button to select files
        self.select_files_button = QPushButton("Select CSV Files")
        self.select_files_button.clicked.connect(self.open_file_dialog)
        main_layout.addWidget(self.select_files_button)

        # File List Widget
        self.file_list_widget = QListWidget()
        main_layout.addWidget(self.file_list_widget)

        # Options Panel
        options_layout = QVBoxLayout()

        # Column Selection Group
        column_group = QGroupBox("Select Columns")
        column_layout = QVBoxLayout()

        self.column_list_widget = QListWidget()
        self.column_list_widget.setSelectionMode(QAbstractItemView.MultiSelection)
        column_layout.addWidget(self.column_list_widget)

        column_group.setLayout(column_layout)
        options_layout.addWidget(column_group)

        # Duplicate Handling Group
        duplicate_group = QGroupBox("Handle Duplicate Records")
        duplicate_layout = QVBoxLayout()

        self.duplicate_combo_box = QComboBox()
        self.duplicate_combo_box.addItems(
            ["Keep First Occurrence", "Keep Last Occurrence", "Keep All"]
        )
        duplicate_layout.addWidget(self.duplicate_combo_box)

        duplicate_group.setLayout(duplicate_layout)
        options_layout.addWidget(duplicate_group)

        # Rearrange Columns Group
        rearrange_group = QGroupBox("Rearrange Columns")
        rearrange_layout = QHBoxLayout()

        self.rearrange_list_widget = QListWidget()
        rearrange_layout.addWidget(self.rearrange_list_widget)

        move_up_button = QPushButton("Move Up")
        move_up_button.clicked.connect(self.move_up)
        rearrange_layout.addWidget(move_up_button)

        move_down_button = QPushButton("Move Down")
        move_down_button.clicked.connect(self.move_down)
        rearrange_layout.addWidget(move_down_button)

        rearrange_group.setLayout(rearrange_layout)
        options_layout.addWidget(rearrange_group)

        main_layout.addLayout(options_layout)

        # Merge Button
        self.merge_button = QPushButton("Merge CSV Files")
        self.merge_button.clicked.connect(self.merge_files)
        main_layout.addWidget(self.merge_button)

        # Central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def open_file_dialog(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter("CSV Files (*.csv)")
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            self.file_list_widget.addItems(selected_files)
            self.populate_column_list(
                selected_files[0]
            )  # Load columns from the first file for selection

    def populate_column_list(self, file_path):
        df = pd.read_csv(file_path)
        self.column_list_widget.clear()
        self.column_list_widget.addItems(list(df.columns))
        self.rearrange_list_widget.clear()
        self.rearrange_list_widget.addItems(list(df.columns))

    def move_up(self):
        current_row = self.rearrange_list_widget.currentRow()
        if current_row > 0:
            item = self.rearrange_list_widget.takeItem(current_row)
            self.rearrange_list_widget.insertItem(current_row - 1, item)
            self.rearrange_list_widget.setCurrentRow(current_row - 1)

    def move_down(self):
        current_row = self.rearrange_list_widget.currentRow()
        if current_row < self.rearrange_list_widget.count() - 1:
            item = self.rearrange_list_widget.takeItem(current_row)
            self.rearrange_list_widget.insertItem(current_row + 1, item)
            self.rearrange_list_widget.setCurrentRow(current_row + 1)

    def merge_files(self):
        selected_files = [
            self.file_list_widget.item(i).text()
            for i in range(self.file_list_widget.count())
        ]

        if not selected_files:
            QMessageBox.warning(self, "Warning", "No CSV Files selected")
            return

        # Read and merge CSV files
        dataframes = [pd.read_csv(file) for file in selected_files]
        merged_df = pd.concat(dataframes, ignore_index=True)

        # Handle duplicate records
        duplicate_handling = self.duplicate_combo_box.currentText()
        if duplicate_handling == "Keep First Occurrence":
            merged_df = merged_df.drop_duplicates(keep="first")
        elif duplicate_handling == "Keep Last Occurrence":
            merged_df = merged_df.drop_duplicates(keep="last")
            # Keep all means no duplicate handling

        # Select and arrange columns
        selected_columns = [
            item.text() for item in self.column_list_widget.selectedItems()
        ]
        if selected_columns:
            merged_df = merged_df[selected_columns]

        rearranged_columns = [
            self.rearrange_list_widget.item(i).text()
            for i in range(self.rearrange_list_widget.count())
        ]
        merged_df = merged_df[rearranged_columns]

        # Save merged file
        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save Merged CSV", "", "CSV Files (*.csv)"
        )
        if save_path:
            merged_df.to_csv(save_path, index=False)
            QMessageBox.information(
                self, "Success", "CSV files are merged successfully!"
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
