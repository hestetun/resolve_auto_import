import os
import shutil

destination = os.path.join(os.path.expanduser("~"), "Library/Services/resolve_auto_import")

files = ["DaVinciResolveScript.py", "resolve_auto_import.py", "resolve_connection.py"]

for file in files:
    shutil.copyfile(file, os.path.join(destination, file))
