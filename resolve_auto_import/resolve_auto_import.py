import os
import sys

# version 0.1.0

valid_extensions = ["mxf", "mov", "arx", "ari", "r3d", 'mp4', 'dpx', 'exr', 'wav']


def import_folder_as_roll(source_folder: str):
    files_to_import = []

    new_bin_name = os.path.basename(source_folder)

    for walk_root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.lower().split(".")[-1] in valid_extensions:
                files_to_import.append(os.path.join(walk_root, file))

    if not files_to_import:
        print("No valid files in that folder")
        notify("Resolve Auto Import", f"No valid files in {new_bin_name}")
        return

    mp = resolve.load_project().GetMediaPool()

    mp.SetCurrentFolder(mp.GetRootFolder())

    folder_names = [sf.GetName() for sf in mp.GetCurrentFolder().GetSubFolderList()]

    if new_bin_name in folder_names:
        print("Already imported this folder")
        notify("Resolve Auto Import", f"Already imported {new_bin_name}")
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
    folders.sort()
    for root in folders:

        if root.endswith('/'):
            root = root[:-1]

        project = resolve.load_project()
        clips = import_folder_as_roll(root)

        if not clips:
            continue

        name = os.path.basename(root)
        timeline_from_clips(filter_clips_for_timeline(clips), name)
        notify("Resolve Auto Import", f'Imported {name}')


def filter_clips_for_timeline(clips):
    clips_for_timeline = []

    for clip in clips:

        if clip.GetName().lower().endswith('.wav'):
            continue

        clips_for_timeline.append(clip)


def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))


if __name__ == '__main__':

    from resolve_connection import ResolveConnection

    try:
        resolve = ResolveConnection()
    except Exception as e:
        notify("Resolve Auto Import", f'Failed to connect to Resolve. {e}')
        sys.exit()

    input_folders = sys.argv[1:]
    import_from_folders(input_folders)
