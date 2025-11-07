import os

metadata = {}
metadata["category"] = None
metadata["year"] = None
metadata["month"] = None
metadata["tags"] = []

fp = "/home/afeiden/Documents/metadata_dkz2r/BrainergyLab"
files_by_extensions = {}
subfolders = []
for (dirpath, dirnames, filenames) in os.walk(fp):
    for filename in filenames:
        extension = filename.split(".")[-1].lower()
        if not extension in files_by_extensions.keys():
            files_by_extensions[extension] = []
        rel_dir = dirpath.replace("/home/afeiden/Documents/metadata_dkz2r/BrainergyLab/", "")
        subfolders += rel_dir.split("/")
        files_by_extensions[extension].append(rel_dir + "/" + filename)


subfolders = set(subfolders)
subfolders = list(subfolders)
subfolders.sort()
pictures_extensions = ["tif", "tiff", "png", "jpg"]
document_extensions = ["pdf", "txt", "docx", "pptx"]
data_extensions = ["csv", "dat"]


