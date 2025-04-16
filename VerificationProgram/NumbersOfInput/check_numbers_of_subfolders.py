import os  # Import the os module for interacting with the file system

# Define the path to the main folder containing all university subfolders
folder_path = '/Users/helanwang/PycharmProjects/divHelan/Wave3/2021UniversityFiles'

# List all items in the folder and keep only those that are directories (i.e., subfolders)
subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]

# Print the total number of university subfolders found
print(f"Number of subfolders: {len(subfolders)}")