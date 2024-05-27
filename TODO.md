# CSV Merger Tool Development Plan

## Project Initialization
- [x] Set up the project repository.
- [x] Create a virtual environment.
- [x] Install necessary Python packages (pandas, PyQt5).

## GUI Design
- [x] Design the main application window.
- [x] Create a file selection interface.
  - [x] Add functionality to select multiple CSV files.
  - [x] Add checkboxes for selecting columns.
  - [x] Add options for rearranging columns.
  - [x] Add options for handling duplicate records (keep first, keep last, keep all).
- [x] Add a preview panel to display the selected files and columns.
- [x] Add a save button to execute the save procesis.
- [ ] Add a status bar to display messages and progress.

## Core Functionality
- [x] Implement file selection logic.
  - [x] Validate selected files (check if they are CSV).
- [x] Implement CSV parsing logic using pandas.
  - [x] Read data from selected CSV files.
- [x] Implement column selection and rearrangement logic.
  - [x] Allow users to select and rearrange columns.
- [x] Implement duplicate handling logic.
  - [x] Provide options to handle duplicates as per user selection.
- [x] Implement the merging process.
  - [x] Merge data from selected CSV files based on user options.
  - [x] Ensure data integrity and handle any potential errors.
- [x] Implement the export functionality to save the merged CSV file.

## User Interface Enhancements
- [ ] Add file drag-and-drop functionality.
- [ ] Implement additional options for data customization (e.g., filtering rows, sorting data).
- [ ] Add tooltips and help messages for better user guidance.

## Testing
- [ ] Write unit tests for core functionality (CSV parsing, merging logic).
- [ ] Perform integration testing to ensure all components work together.
- [ ] Conduct usability testing to gather feedback on the user interface.

## Documentation
- [ ] Write user documentation explaining how to use the tool.
- [ ] Write developer documentation for code maintenance and future enhancements.

## Deployment
- [ ] Package the application for distribution.
  - [ ] Create executables for different platforms (Windows, macOS, Linux).
- [ ] Provide installation instructions.

## Post-Deployment
- [ ] Set up a feedback mechanism for users.
- [ ] Plan for future updates and feature enhancements.

