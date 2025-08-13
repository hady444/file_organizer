import os
import tempfile
import unittest
from file_organizer import organize_files, categorize_file, undo_last_move, LOG_FILE
import json

def create_test_files(base_dir, files):
    """Helper to create dummy files in a directory."""
    for file in files:
        with open(os.path.join(base_dir, file), 'w') as f:
            f.write("test")


class TestFileOrganizer(unittest.TestCase):

    def test_categorize_file(self):
        self.assertEqual(categorize_file("image.jpg"), "Images")
        self.assertEqual(categorize_file("document.pdf"), "Documents")
        self.assertEqual(categorize_file("video.mp4"), "Videos")
        self.assertEqual(categorize_file("unknown.xyz"), "Others")

    def test_organize_files_simulation(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            create_test_files(temp_dir, ["file1.jpg", "file2.pdf", "file3.mp4", "file4.xyz"])
            summary = organize_files(temp_dir, simulate=True)

            self.assertEqual(summary["Images"], 1)
            self.assertEqual(summary["Documents"], 1)
            self.assertEqual(summary["Videos"], 1)
            self.assertEqual(summary["Others"], 1)

            # Ensure no category folders are created in simulate mode
            dirs_created = [f for f in os.listdir(temp_dir) if os.path.isdir(os.path.join(temp_dir, f))]
            self.assertEqual(len(dirs_created), 0)

    def test_organize_files_real_move(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            create_test_files(temp_dir, ["file1.jpg", "file2.pdf", "file3.mp4", "file4.xyz"])
            summary = organize_files(temp_dir, simulate=False)

            self.assertTrue(os.path.exists(os.path.join(temp_dir, "Images", "file1.jpg")))
            self.assertTrue(os.path.exists(os.path.join(temp_dir, "Documents", "file2.pdf")))
            self.assertTrue(os.path.exists(os.path.join(temp_dir, "Videos", "file3.mp4")))
            self.assertTrue(os.path.exists(os.path.join(temp_dir, "Others", "file4.xyz")))

            self.assertEqual(summary["Images"], 1)
            self.assertEqual(summary["Documents"], 1)
            self.assertEqual(summary["Videos"], 1)
            self.assertEqual(summary["Others"], 1)
    def test_undo_last_move(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files
            create_test_files(temp_dir, ["file1.jpg", "file2.pdf"])

            # Perform real move
            organize_files(temp_dir, simulate=False)

            # Read log file to ensure it was created
            self.assertTrue(os.path.exists(LOG_FILE))
            with open(LOG_FILE, "r") as f:
                moves = json.load(f)
            self.assertEqual(len(moves), 2)

            # Undo the move
            undo_last_move()

            # Check that files are back in the original location
            self.assertTrue(os.path.exists(os.path.join(temp_dir, "file1.jpg")))
            self.assertTrue(os.path.exists(os.path.join(temp_dir, "file2.pdf")))

            # Check that log file is deleted after undo
            self.assertFalse(os.path.exists(LOG_FILE))


if __name__ == "__main__":
    unittest.main()
