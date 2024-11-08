import os
import sys

from resolve_connection import ResolveConnection

resolve = ResolveConnection()
valid_extensions = ["mxf", "mov", "arx", "ari", "r3d", 'mp4', 'dpx', 'exr']


def import_folder_as_roll(source_folder: str):
    files_to_import = []

    for walk_root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.lower().split(".")[-1] in valid_extensions:
                files_to_import.append(os.path.join(walk_root, file))

    if not files_to_import:
        print("No valid files in that folder")
        notify("Resolve Auto Import", "No valid files in that folder")
        return

    mp = resolve.load_project().GetMediaPool()
    new_bin_name = os.path.basename(source_folder)

    mp.SetCurrentFolder(mp.GetRootFolder())

    folder_names = [sf.GetName() for sf in mp.GetCurrentFolder().GetSubFolderList()]

    if new_bin_name in folder_names:
        print("Already imported this folder")
        notify("Resolve Auto Import", "Already imported this folder")
        return

    roll_bin = mp.AddSubFolder(mp.GetCurrentFolder(), new_bin_name)

    mp.SetCurrentFolder(roll_bin)

    clips_imported = mp.ImportMedia(files_to_import)

    return clips_imported


def timeline_from_clips(clips_list, timeline_name):
    mp = resolve.load_project().GetMediaPool()
    created_timeline = mp.CreateTimelineFromClips(timeline_name, clips_list)
    return created_timeline


def import_from_folders(folders):
    for root in folders:

        if root.endswith('/'):
            root = root[:-1]

        project = resolve.load_project()
        clips = import_folder_as_roll(root)

        if not clips:
            return

        name = os.path.basename(root)
        timeline_from_clips(clips, name)


def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))


if __name__ == '__main__':

    input_folders = sys.argv[1:]
    import_from_folders(input_folders)
