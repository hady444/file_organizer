# File Organizer

A Python command-line tool that organizes files in a given folder into categorized subfolders such as **Images**, **Documents**, **Videos**, and **Others**.  
It also supports a simulation mode to preview changes before moving files.

---

## Features

- Organizes files by type into subfolders.
- Categories include:
  - Images (`.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`)
  - Documents (`.pdf`, `.docx`, `.doc`, `.txt`, `.xlsx`, `.pptx`)
  - Videos (`.mp4`, `.avi`, `.mov`, `.mkv`)
  - Others (any file not matching the above)
- **Simulation mode** to see what would happen without moving files.
- Summary report showing the number of files per category.

---

## Project Structure

```File_Organizer/
│── file_organizer.py # Main script
│── test/ # Test folder
│ └── test.py # Unit tests
```

---

## Installation

 **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/File_Organizer.git
   cd File_Organizer
   ```

## Usage
 **Organize Files**
  ```python file_organiser.py --path /path/to/folder```

 **Simulate Organization (no files moved)**
  ```python file_organiser.py --path /path/to/folder --simulate```
## Running Tests
The project uses Python’s built-in unittest framework.
  ```python -m unittest discover test -v```

## Undo Feature
  **How the Undo Works**
   Every time we move files for real (not simulate), we log:

```
[
    {"src": "/original/path/file1.jpg", "dest": "/Images/file1.jpg"},
    {"src": "/original/path/file2.pdf", "dest": "/Documents/file2.pdf"}
]
```
If --undo is called:
 - Reads this JSON file.
 - Moves each file back to its original location.
 - Deletes the log file so the undo only applies once.

## Future Enhancements
 - Recursive Mode: Organize files inside subfolders as well.

 - Custom Categories: Allow users to define categories and extensions via a config file.

 - Logging: Save an operation log with details of moved files.

 - Progress Bar: Show progress while processing large folders.

 - Undo Option: Restore files to their original location if needed. (done)