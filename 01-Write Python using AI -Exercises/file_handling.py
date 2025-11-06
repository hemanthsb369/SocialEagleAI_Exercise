# file_handling_example.py

# Step 1: Create and write to a file
with open("sample.txt", "w") as file:
    file.write("Hello, Hemanth!\n")
    file.write("This is a file handling demo.\n")

# Step 2: Read the file content
with open("sample.txt", "r") as file:
    content = file.read()
    print("File content after initial write:")
    print(content)

# Step 3: Append new content
with open("sample.txt", "a") as file:
    file.write("Appending a new line.\n")

# Step 4: Read the updated content
with open("sample.txt", "r") as file:
    updated_content = file.read()
    print("\nFile content after appending:")
    print(updated_content)