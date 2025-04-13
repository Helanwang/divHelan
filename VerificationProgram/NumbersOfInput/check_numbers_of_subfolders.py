import os

folder_path = '/Users/helanwang/PycharmProjects/divHelan/Wave3/2021UniversityFiles'
subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]

print(f"Number of subfolders: {len(subfolders)}")