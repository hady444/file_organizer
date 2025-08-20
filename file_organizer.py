import os
import shutil
import argparse
from collections import defaultdict
import json

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


def organize_files(folder_path, log_file, simulate=False):
    """Organize files in the given folder by type."""
    if not os.path.isdir(folder_path):
        raise NotADirectoryError(f"Path '{folder_path}' is not a valid directory.")

    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    summary = defaultdict(int)
    moves = []

    for file in files:
        if file == "file_organizer_log.json":
            continue
        category = categorize_file(file)
        category_folder = os.path.join(folder_path, category)
        src = os.path.join(folder_path, file)
        dest = os.path.join(category_folder, file)

        if not simulate:
            os.makedirs(category_folder, exist_ok=True)
            shutil.move(src, dest)
            moves.append({"src": src, "dest": dest})

        summary[category] += 1

    if not simulate and moves:
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                try:
                    history = json.load(f)
                except json.JSONDecodeError:
                    history = []
        else:
            history = []
        history.append(moves)

        with open(log_file, "w") as f:
            json.dump(history, f, indent=4)

    return dict(summary)


def undo_last_move(log_file):
    """Undo the most recent organize_files operation."""
    if not os.path.exists(log_file):
        print("No previous move found to undo.")
        return

    with open(log_file, "r") as f:
        try:
            history = json.load(f)
        except json.JSONDecodeError:
            print("Log file is corrupted.")
            return

    if not history:
        print("No previous move found to undo.")
        return

    last_session = history.pop()

    for move in reversed(last_session):  
        if os.path.exists(move["dest"]):
            os.makedirs(os.path.dirname(move["src"]), exist_ok=True)
            shutil.move(move["dest"], move["src"])

    # Save updated history
    with open(log_file, "w") as f:
        json.dump(history, f, indent=4)

    print("Undo completed. Last session has been restored.")


def main():
    parser = argparse.ArgumentParser(description="Organize files in a folder by type.")
    parser.add_argument("--path", required=True, help="Path to the folder.")
    parser.add_argument("--simulate", action="store_true", help="Simulate the operation without moving files.")
    parser.add_argument("--undo", action="store_true", help="Undo the last file organization.")
    args = parser.parse_args()
    log_file = os.path.join(args.path, "file_organizer_log.json")
    if args.undo:
        undo_last_move(log_file)
    elif args.path:
        summary = organize_files(args.path, log_file, simulate=args.simulate)

        print("\nSummary of files:")
        for category, count in summary.items():
            print(f"{category}: {count} file(s)")
    else:
        parser.error("Please provide either --path or --undo")


if __name__ == "__main__":
    main()
