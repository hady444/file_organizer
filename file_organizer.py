import os
import shutil
import argparse
from collections import defaultdict

# Define file type categories
FILE_CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp"},
    "Documents": {".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx"},
    "Videos": {".mp4", ".avi", ".mov", ".mkv"}
}


def categorize_file(filename):
    """Return the category for a given file based on its extension."""
    ext = os.path.splitext(filename)[1].lower()
    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
    return "Others"


def organize_files(folder_path, simulate=False):
    """Organize files in the given folder by type."""
    if not os.path.isdir(folder_path):
        raise NotADirectoryError(f"Path '{folder_path}' is not a valid directory.")

    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    summary = defaultdict(int)

    for file in files:
        category = categorize_file(file)
        category_folder = os.path.join(folder_path, category)

        if not simulate:
            os.makedirs(category_folder, exist_ok=True)
            shutil.move(os.path.join(folder_path, file), os.path.join(category_folder, file))

        summary[category] += 1

    return dict(summary)


def main():
    parser = argparse.ArgumentParser(description="Organize files in a folder by type.")
    parser.add_argument("--path", required=True, help="Path to the folder.")
    parser.add_argument("--simulate", action="store_true", help="Simulate the operation without moving files.")
    args = parser.parse_args()

    summary = organize_files(args.path, simulate=args.simulate)

    print("\nSummary of files:")
    for category, count in summary.items():
        print(f"{category}: {count} file(s)")


if __name__ == "__main__":
    main()
