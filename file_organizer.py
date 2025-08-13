import os
import shutil
import argparse
from collections import defaultdict
import json

# Define file type categories
FILE_CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp"},
    "Documents": {".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx"},
    "Videos": {".mp4", ".avi", ".mov", ".mkv"}
}

LOG_FILE = "last_move_log.json"

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
    moves = []

    for file in files:
        category = categorize_file(file)
        category_folder = os.path.join(folder_path, category)
        src = os.path.join(folder_path, file)
        dest = os.path.join(category_folder, file)

        if not simulate:
            os.makedirs(category_folder, exist_ok=True)
            shutil.move(os.path.join(folder_path, file), os.path.join(category_folder, file))
            moves.append({"src": src, "dest": dest})

        summary[category] += 1
    if not simulate and moves:
        with open(LOG_FILE, "w") as f:
            json.dump(moves, f)

    return dict(summary)

def undo_last_move():
    if not os.path.exists(LOG_FILE):
        print("No previous move found to undo.")
        return

    with open(LOG_FILE, "r") as f:
        moves = json.load(f)

    for move in moves:
        if os.path.exists(move["dest"]):
            os.makedirs(os.path.dirname(move["src"]), exist_ok=True)
            shutil.move(move["dest"], move["src"])

    os.remove(LOG_FILE)
    print("Undo completed. Files have been restored to their original locations.")


def main():
    parser = argparse.ArgumentParser(description="Organize files in a folder by type.")
    parser.add_argument("--path", help="Path to the folder.")
    parser.add_argument("--simulate", action="store_true", help="Simulate the operation without moving files.")
    parser.add_argument("--undo", action="store_true", help="Undo the last file organization.")
    args = parser.parse_args()

    if args.undo:
        undo_last_move()
    elif args.path:
        summary = organize_files(args.path, simulate=args.simulate)

        print("\nSummary of files:")
        for category, count in summary.items():
            print(f"{category}: {count} file(s)")
    else:
        parser.error("Please provide either --path or --undo")


if __name__ == "__main__":
    main()
