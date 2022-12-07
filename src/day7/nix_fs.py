from __future__ import annotations
from typing import TypeVar, Optional, Iterable, Dict
import os
import pathlib
import logging

FSDirT = TypeVar('FSDirT', bound='FSDir')

class FSDir:
    """Filesystem Directory"""

    def __init__(self, name: str, parent: Optional[FSDirT] = None):
        self._name = name
        self._parent = parent
        self._subdirs = dict()
        self._files = dict()

    def add_subdir(self, subdir_name: str) -> None:
        """Add a subdirectory"""
        self._subdirs[subdir_name] = FSDir(name=subdir_name, parent=self)

    def add_file(self, filename: str, size: int) -> None:
        """Add a file to the current directory"""
        self._files[filename] = size

    def cd(self, subdir_name: str) -> FSDirT:
        """Return a subdirectory"""
        if subdir_name == '..':
            if self._parent is None:
                raise ValueError(f"Attempt to grab parent of root")
            return self._parent
        elif not subdir_name in self._subdirs:
            raise FileNotFoundError(f"You haven't told me about this subdirectory yet: {subdir_name}")
        return self._subdirs[subdir_name]

    def subdir_sizes(self) -> Dict[str, int]:
        """Recursively return a list of all subdirectories and their sizes"""
        global logger
        all_sizes = dict()
        this_dir_size = 0
        # subdirs
        logger.debug(f"f: subdir_sizes; name={self._name}")
        for subdir_name in self._subdirs:
            logger.debug(f"subdir_name={subdir_name}; size processing follows:")
            subsubdir_sizes = self._subdirs[subdir_name].subdir_sizes()
            for k, v in subsubdir_sizes.items():
                logger.debug(f"subsubdir={k}, size={v}")
                if self._name != '/':
                    name_ = f"{self._name}/{k}"
                else:
                    name_ = f"/{k}"
                logger.debug(f"name_={name_}")
                all_sizes[name_] = v
                this_dir_size += v
                logger.debug(f"this_dir_size={this_dir_size}")
        # files
        logger.debug(f"... file processing follows:")
        for k, v in self._files.items():
            logger.debug(f"file={k}, size={v}")
            this_dir_size += v
            logger.debug(f"this_dir_size={this_dir_size}")

        logger.debug(f"Adding size entry: k={self._name}, v={this_dir_size}")
        all_sizes[self._name] = this_dir_size
        return all_sizes

    def __repr__(self):
        return f"FSDir({self._name})"

def split_lines(lines: str) -> Iterable[str]:
    return lines.split('\n')

def get_FSDir_from_shell_transcript(lines: Iterable[str]) -> FSDirT:
    """Parse a list of lines from a shell session, return an FSDir with all known file sizes"""
    global logger
    root: FSDirT = FSDir(name='/', parent=None)
    cwd: Optional[FSDirT] = None
    for line in lines:
        if line == '':
            logger.debug('empty line - skipping')
            continue
        split_line = line.split(' ')
        first, *rest = split_line
        if first == '$': # command
            logger.debug('branch: command')
            second, *rest_ = rest
            if second == 'cd':
                subdir_name = rest_[0]
                logger.debug(f'branch: cd; subdir_name={subdir_name}')
                if subdir_name == '/':
                    cwd = root
                else:
                    cwd = cwd.cd(subdir_name)
            elif second == 'ls':
                logger.debug('branch: ls')
                pass # no useful info
            else:
                raise NotImplementedError
        elif first == 'dir': # info: name of a subdirectory
            subdir_name = rest[0]
            logger.debug(f'branch: dir; subdir_name={subdir_name}')
            cwd.add_subdir(subdir_name)
        else: # super-safe assumption: this is a file size
            size = int(first)
            filename = rest[0]
            logger.debug(f'branch: default/file; size={size}, filename={filename}')
            cwd.add_file(filename, size)
    return root

def size_of_filtered_dirs(dirs: Dict[str, int]) -> int:
    global logger
    #dirs_ = dirs
    dirs_ = dict()
    logger.debug('f: size_of_filtered_dirs: getting directories meeting filter requirement')
    for k, v in dirs.items():
        in_scope = v<=100000
        if in_scope:
            dirs_[k] = v
        logger.debug(f"k={k}, v={v}, in_scope={in_scope}")
    #dirs_ = {k: v for k, v in dirs.items() if v<=100000}
    #breakpoint()
    size = sum(dirs_.values())
    logger.debug(f"size={size}")
    return size

def main():
    global logger
    logger = logging.Logger(__name__)
    h = logging.StreamHandler()
    logger.addHandler(h)
    logger.setLevel(logging.DEBUG)

    filepath = os.environ['INPUT_FILE']
    p = pathlib.Path(filepath)
    assert p.exists(), f"Want input, got: {filepath}"
    logger.debug('Opening input file')
    with open(p, 'r') as f:
        lines = split_lines(f.read())
    logger.debug('Getting FSDir from shell transcript')
    fsd = get_FSDir_from_shell_transcript(lines)

    # part 1
    tot = size_of_filtered_dirs(fsd.subdir_sizes())
    print(f"Total size of dirs of size <=100000: {tot}")

if __name__ == '__main__':
    main()



