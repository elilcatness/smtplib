import os
from zipfile import ZipFile


def make_archive(source, dest, filename):
    try:
        prev_cwd = os.getcwd()
        source, dest = map(lambda x: os.path.abspath(x), (source, dest))
        os.chdir(source)
    except OSError:
        return False
    zf = ZipFile(os.path.join(dest, filename), 'w')
    for current_dir, _, files in os.walk(source):
        for file in files:
            if file != filename:
                zf.write(os.path.relpath(os.path.join(current_dir, file)))
    os.chdir(prev_cwd)
    return True