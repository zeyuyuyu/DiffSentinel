import os
import difflib
import hashlib

class DiffAnalyzer:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.previous_hashes = {}

    def analyze_changes(self):
        """Analyze changes in the repository and detect new or modified files."""
        changed_files = []
        for root, dirs, files in os.walk(self.repo_path):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, self.repo_path)
                new_hash = self.calculate_hash(file_path)
                if relative_path not in self.previous_hashes or self.previous_hashes[relative_path] != new_hash:
                    changed_files.append(relative_path)
                self.previous_hashes[relative_path] = new_hash
        return changed_files

    def calculate_hash(self, file_path):
        """Calculate the SHA-256 hash of a file."""
        with open(file_path, 'rb') as f:
            file_hash = hashlib.sha256()
            while chunk := f.read(8192):
                file_hash.update(chunk)
        return file_hash.hexdigest()

    def generate_diff(self, file_path):
        """Generate a unified diff for a given file."""
        with open(file_path, 'r') as f:
            new_content = f.readlines()
        if file_path in self.previous_hashes:
            old_content = self.load_previous_content(file_path)
            diff = difflib.unified_diff(old_content, new_content, fromfile=file_path, tofile=file_path)
            return ''.join(diff)
        else:
            return None

    def load_previous_content(self, file_path):
        """Load the previous content of a file from the hash map."""
        relative_path = os.path.relpath(file_path, self.repo_path)
        if relative_path in self.previous_hashes:
            with open(file_path, 'r') as f:
                return f.readlines()
        else:
            return []