import os

# Define the license text
LICENSE_TEXT = """# Licensed under the Apache License, Version 2.0
# Copyright 2024 Zahid Hossain <zhossainny@gmail.com>
#
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""

# File extensions to process
FILE_EXTENSIONS = [".py", ".txt", ".md"]  # Add more extensions as needed

# Function to add the license text to the top of a file
def add_license_to_file(file_path):
    with open(file_path, "r+") as file:
        content = file.read()
        # Skip files that already have the license text
        if LICENSE_TEXT.splitlines()[0] in content:
            print(f"License already exists in {file_path}")
            return
        # Add the license at the top
        file.seek(0, 0)
        file.write(LICENSE_TEXT + "\n" + content)
        print(f"License added to {file_path}")

# Traverse the directory and process files
def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            # Skip __init__.py files
            if file == "__init__.py":
                print(f"Skipping {os.path.join(root, file)}")
                continue
            # Process files with the specified extensions
            if any(file.endswith(ext) for ext in FILE_EXTENSIONS):
                file_path = os.path.join(root, file)
                add_license_to_file(file_path)

# Start processing from the current directory
if __name__ == "__main__":
    process_directory(".")
