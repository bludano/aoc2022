from __future__ import annotations
from typing import TypeVar, Optional, Iterable, Dict
import os
import pathlib
import logging

FSDirT = TypeVar('FSDirT', bound='FSDir')

class FSDir:
    """Filesystem Directory"""

    # variables held by the FSDir at the root of the system, to give us UUIDs on tap
    _max_uuid: int = -1
    _registry: Dict[int, FSDirT] = dict()

    @property
    def root(self) -> FSDirT:
        return self._root

    def register(self, fsdir: FSDirT) -> None:
        """Register an FSDir with the root node"""
        global logger
        if self.root == self:
            self._max_uuid += 1
            self._registry[self._max_uuid] = fsdir
            logger.debug(f"FSDir.register: UUID={self.root._max_uuid}, fsdir={fsdir!r}, root={self.root!r}")
            return
        else:
            return self.root.register(fsdir)

    def __iter__(self) -> Iterable[FSDirT]:
        if self.root == self:
            return iter(self._registry.items())
        return iter(self.root)

    @property
    def size(self) -> int:
        global logger
        size_ = self._size
        logger.debug(f"FSDir.size: FSDir={self!r}, own size={size_}")
        for subdir in self._subdirs.values():
            subdir_size = subdir.size
            size_ += subdir_size
            logger.debug(f"FSDir.size: FSDir={self!r}, subdir={subdir!r}, subdir_size={subdir_size}, new size={size_}")
        return size_

    def __init__(self, name: str, parent: Optional[FSDirT] = None):
        global logger
        if not parent:
            self._root = self
        else:
            self._root = parent.root
        self._name = name
        self._parent = parent
        self._subdirs: Dict[str, FSDirT] = dict()
        self._files = set()
        self.register(self)
        self._size = 0
        logger.debug(f"FSDir.__init__: name={name}, parent={parent!r}, root={self._root}")

    def add_subdir(self, subdir_name: str) -> None:
        """Add a subdirectory"""
        global logger
        logger.debug(f"FSDir.add_subdir: subdir_name={subdir_name}")
        self._subdirs[subdir_name] = FSDir(name=subdir_name, parent=self)

    def add_file(self, filename: str, size: int) -> None:
        """Add a file to the current directory"""
        global logger
        self._files.add(filename)
        self._size += size
        logger.debug(f"FSDir.add_file: filename={filename}, size={size}")

    def cd(self, subdir_name: str) -> FSDirT:
        """Return a subdirectory"""
        global logger
        logger.debug(f"FSDir.cd: subdir_name={subdir_name}")
        if subdir_name == '..':
            if self._parent is None:
                raise ValueError(f"Attempt to grab parent of root")
            return self._parent
        elif not subdir_name in self._subdirs:
            raise FileNotFoundError(f"You haven't told me about this subdirectory yet: {subdir_name}")
        return self._subdirs[subdir_name]

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
    dirs_ = dict()
    logger.debug('f: size_of_filtered_dirs: getting directories meeting filter requirement')
    for uuid, fsd in dirs:
        size = fsd.size
        in_scope = size<=100000
        if in_scope:
            dirs_[uuid] = size
        logger.debug(f"uuid={uuid}, fsd={fsd}, size={size} in_scope={in_scope}")
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
    tot = size_of_filtered_dirs(list(fsd))
    print(f"Total size of dirs of size <=100000: {tot}")

if __name__ == '__main__':
    main()



