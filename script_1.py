import os
import re

categories = ["Proposal", "Reporting", "Meetings", "Pictures", "Posters", "Photos", "Presentations", "Data", "Code"]

pictures_extensions = ["tif", "tiff", "png", "jpg"]
document_extensions = ["pdf", "txt", "docx", "pptx"]
data_extensions = ["csv", "dat"]
coding_extensions = ["r", "h"]


def create_blank_metadata():
    metadata = {}
    metadata["category"] = []
    metadata["year"] = None
    metadata["month"] = None
    metadata["day"] = None
    metadata["tags"] = []
    return metadata


def info_from_extension(extension, metadata):
    if extension in pictures_extensions:
        metadata["category"].append("Pictures")
    if extension in data_extensions:
        metadata["category"].append("Data")
    if extension in coding_extensions:
        metadata["category"].append("Code")
    return metadata


def info_from_subfolder(subfolder, metadata):
    if subfolder in ['0000SET', '001', '100MSDCF', 'APV Greenhouse', 'APV greenhouse Pointcloud', 'Brainergy Field', 'CO2-Board', 'DIY-Stations', 
                     'Environmental stations', 'Farmdroid', 'FieldDeer', 'FieldNotes', 'Harvest', 'JAI camera', 'JAI-8 Kamera', 'LIFT', 'Mica', 'MicaSense Red', 'OSDK', 'RGB', 'Red', 'Robots', 'SYNC0000SET', 'Sampling Points', 'Test Scene', 'UAV', 'V3', 
                     'multi', 'rgb']:
        metadata["tags"].append(subfolder)
    if subfolder in ["Data sources", "Experiments and data", "data", "experiments", 'test data', 'test data set']:
        metadata["category"].append("Data")
    if subfolder in ["bilder"]:
        metadata["category"].append("Pictures")
    if re.match("\\d\\d_.*", subfolder):
        if subfolder.split("_")[-1] in categories:
            metadata["category"].append(subfolder.split("_")[-1])
        else: 
            metadata["tags"].append(subfolder.split("_")[-1])
    if re.match("\\d\\d\\d\\d_.*", subfolder):
        metadata["year"] = subfolder.split("_")[0]
        metadata["tags"].append(subfolder.split("_")[1])
    if len(subfolder) == 4 and re.match("\\d\\d\\d\\d", subfolder):
        metadata["year"] = subfolder
    if len(subfolder) == 6 and re.match("\\d\\d\\d\\d\\d\\d", subfolder):
        metadata["year"] = "20" + subfolder[:2]
        metadata["month"] = subfolder[2:4]
        metadata["day"] = subfolder[4:]
    if len(subfolder) == 8 and re.match("\\d\\d\\d\\d\\d\\d\\d\\d", subfolder):
        metadata["year"] = subfolder[:4]
        metadata["month"] = subfolder[4:6]
        metadata["day"] = subfolder[6:]
    if subfolder == 'July':
        metadata["month"] = 7
    if subfolder == 'June':
        metadata["month"] = 6
    return metadata


def create_filename(metadata, filename):
    new_fn = ""
    if len(metadata["category"]) == 0:
        new_fn = "unstructured"
    else:
        new_fn = metadata["category"][0]
    new_fn += "/"
    metadata["tags"].sort()
    for tag in metadata["tags"]:
        new_fn += tag + "_"
    if metadata["year"]:
        new_fn += str(metadata["year"]) + "_"
    if metadata["month"]:
        new_fn += str(metadata["month"]) + "_"
    if metadata["day"]:
        new_fn += str(metadata["day"]) + "_"
    new_fn += filename
    return new_fn    


fp = "/home/afeiden/Documents/metadata_dkz2r/BrainergyLab"
files_by_extensions = {}
subfolders = []
new_filenames = []
for (dirpath, dirnames, filenames) in os.walk(fp):
    for filename in filenames:
        extension = filename.split(".")[-1].lower()
        if not extension in files_by_extensions.keys():
            files_by_extensions[extension] = []
        rel_dir = dirpath.replace("/home/afeiden/Documents/metadata_dkz2r/BrainergyLab/", "")
        subfolders += rel_dir.split("/")
        files_by_extensions[extension].append(rel_dir + "/" + filename)
        metadata = create_blank_metadata()
        metadata = info_from_extension(extension, metadata)
        for subfolder in rel_dir.split("/"):
            metadata = info_from_subfolder(subfolder, metadata)
        # print(rel_dir + "/" + filename)
        metadata["filename"] = filename
        metadata["category"] = list(set(metadata["category"]))
        new_filename = create_filename(metadata, filename)
        new_filenames.append(new_filename)


new_filenames.sort()
for fn in new_filenames:
    print(fn)

subfolders = set(subfolders)
subfolders = list(subfolders)
subfolders.sort()
