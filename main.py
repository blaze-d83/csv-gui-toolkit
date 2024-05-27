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
    QLabel,
    QComboBox,
    QAbstractItemView,
    QHBoxLayout,
    QFrame,
)
from PySide6.QtCore import Qt
import pandas as pd
from pandas.core.dtypes.dtypes import re


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CSV Merger Tool")
        self.setGeometry(100, 100, 900, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_layout = QHBoxLayout(self.central_widget)

        # Left side layout for file list and buttons
        self.left_layout = QVBoxLayout()
        self.central_layout.addLayout(self.left_layout)

        # File List Label
        self.file_list_label = QLabel("File List")
        self.file_list_label.setAlignment(Qt.AlignCenter)
        self.left_layout.addWidget(self.file_list_label)

        # File List Widget
        self.file_list_widget = QListWidget()
        self.file_list_widget.setFrameShape(QFrame.Box)
        self.left_layout.addWidget(self.file_list_widget)

        # Add Files Button
        self.add_files_button = QPushButton("Add Files")
        self.add_files_button.clicked.connect(self.open_file_dialog)
        self.left_layout.addWidget(self.add_files_button)

        # Right side layout for options and lists
        self.right_layout = QVBoxLayout()
        self.central_layout.addLayout(self.right_layout)

        # Options Label
        self.options_label = QLabel("Options")
        self.options_label.setAlignment(Qt.AlignCenter)
        self.right_layout.addWidget(self.options_label)

        # Options Widget
        self.options_widget = QWidget()
        self.options_layout = QVBoxLayout(self.options_widget)
        self.right_layout.addWidget(self.options_widget)

        # Data Extraction Label
        self.data_extraction_label = QLabel("Data Extraction")
        self.options_layout.addWidget(self.data_extraction_label)

        # Column List for Selection
        self.column_list_widget = QListWidget()
        self.column_list_widget.setFrameShape(QFrame.Box)
        self.column_list_widget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.options_layout.addWidget(self.column_list_widget)

        # Include/Exclude ComboBox
        self.include_exclude_combo_box = QComboBox()
        self.include_exclude_combo_box.addItems(["Include", "Exclude"])
        self.options_layout.addWidget(self.include_exclude_combo_box)

        # Rearrange Columns Label
        self.rearrange_columns_label = QLabel("Rearrange Columns")
        self.options_layout.addWidget(self.rearrange_columns_label)

        # Rearrange Columns Layout
        self.rearrange_layout_widget = QWidget()
        self.rearrange_layout = QVBoxLayout(self.rearrange_layout_widget)
        self.options_layout.addWidget(self.rearrange_layout_widget)

        # Rearrange Columns List Widget
        self.rearrange_column_list_widget = QListWidget()
        self.rearrange_column_list_widget.setFrameShape(QFrame.Box)
        self.rearrange_layout.addWidget(self.rearrange_column_list_widget)

        # Rearrange Columns Buttons Layout
        self.rearrange_buttons_layout = QHBoxLayout()
        self.move_up_button = QPushButton("Move Up")
        self.move_down_button = QPushButton("Move Down")
        self.rearrange_buttons_layout.addWidget(self.move_up_button)
        self.rearrange_buttons_layout.addWidget(self.move_down_button)
        self.rearrange_layout.addLayout(self.rearrange_buttons_layout)

        # Connect buttons to functions
        self.move_up_button.clicked.connect(self.move_up)
        self.move_down_button.clicked.connect(self.move_down)

        # Duplicate Handling Layout
        self.duplicate_handling_layout = QHBoxLayout()
        self.right_layout.addLayout(self.duplicate_handling_layout)

        # Duplicate Handling ComboBox
        self.duplicate_handling_combo_box = QComboBox()
        self.duplicate_handling_combo_box.addItems(["Keep First", "Keep Last", "Keep All Ocurrences"])
        self.duplicate_handling_layout.addWidget(self.duplicate_handling_combo_box)

        # Save Button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.merge_files)
        self.duplicate_handling_layout.addWidget(self.save_button)

    def open_file_dialog(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter("CSV Files (*.csv)")
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            self.file_list_widget.addItems(selected_files)
            self.populate_column_list(selected_files[0])

    def populate_column_list(self, file_path):
        df = pd.read_csv(file_path)
        self.column_list_widget.clear()
        self.column_list_widget.addItems(list(df.columns))
        self.rearrange_column_list_widget.clear()
        self.rearrange_column_list_widget.addItems(list(df.columns))

    def move_up(self):
        current_row = self.rearrange_column_list_widget.currentRow()
        if current_row > 0:
            current_item = self.rearrange_column_list_widget.takeItem(current_row)
            self.rearrange_column_list_widget.insertItem(current_row - 1, current_item)
            self.rearrange_column_list_widget.setCurrentRow(current_row - 1)

    def move_down(self):
        current_row = self.rearrange_column_list_widget.currentRow()
        if current_row < self.rearrange_column_list_widget.count() - 1:
            current_item = self.rearrange_column_list_widget.takeItem(current_row)
            self.rearrange_column_list_widget.insertItem(current_row + 1, current_item)
            self.rearrange_column_list_widget.setCurrentRow(current_row + 1)

    def merge_files(self):
        selected_files = [
            self.file_list_widget.item(i).text()
            for i in range(self.file_list_widget.count())
        ]

        if not selected_files:
            QMessageBox.warning(self, "Warning", "No CSV Files selected")
            return

        dataframes = [pd.read_csv(file) for file in selected_files]
        merged_df = pd.concat(dataframes, ignore_index=True)

        duplicate_handling = self.duplicate_handling_combo_box.currentText()
        if duplicate_handling == "Keep First":
            merged_df = merged_df.drop_duplicates(keep="first")
        elif duplicate_handling == "Keep Last":
            merged_df = merged_df.drop_duplicates(keep="last")

        selected_columns = [
            item.text() for item in self.column_list_widget.selectedItems()
        ]

        include_exclude_option = self.include_exclude_combo_box.currentText()

        if include_exclude_option == "Include":
            if selected_columns:
                merged_df = merged_df[selected_columns]
        elif include_exclude_option == "Exclude":
            if selected_columns:
                merged_df = merged_df.drop(columns=selected_columns)

        rearranged_columns = [
            self.rearrange_column_list_widget.item(i).text()
            for i in range(self.rearrange_column_list_widget.count())
        ]
        if set(rearranged_columns).issubset(merged_df.columns):
            merged_df = merged_df[rearranged_columns]

        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save Merged CSV", "", "CSV Files (*.csv)"
        )
        if save_path:
            merged_df.to_csv(save_path, index=False)
            QMessageBox.information(
                self, "Success", "File saved successfully!"
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
