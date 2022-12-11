import pytest
import day07.nix_fs
from day07 import nix_fs
import textwrap
import logging

@pytest.fixture(autouse=True)
def logger():
    logger = logging.Logger(__name__)
    h = logging.StreamHandler()
    logger.addHandler(h)
    logger.setLevel(logging.DEBUG)
    day07.nix_fs.logger = logger

@pytest.fixture
def sample():
    return textwrap.dedent("""\
        $ cd /
        $ ls
        dir a
        14848514 b.txt
        8504156 c.dat
        dir d
        $ cd a
        $ ls
        dir e
        29116 f
        2557 g
        62596 h.lst
        $ cd e
        $ ls
        584 i
        $ cd ..
        $ cd ..
        $ cd d
        $ ls
        4060174 j
        8033020 d.log
        5626152 d.ext
        7214296 k
    """)

@pytest.fixture
def sample_file(sample, tmpdir):
    fp = tmpdir / 'sample-lines.txt'
    with open(fp, 'w') as f:
        f.write(sample)
    return fp

@pytest.fixture
def sample_lines(sample):
    return nix_fs.split_lines(sample)

def test_get_FSDir_from_shell_transcript(sample_lines):
    fsd = nix_fs.get_FSDir_from_shell_transcript(sample_lines)

def test_size_of_filtered_dirs(sample_lines):
    fsd = nix_fs.get_FSDir_from_shell_transcript(sample_lines)
    tot_filtered = nix_fs.size_of_filtered_dirs(list(fsd))
    assert tot_filtered == 95437

def test_directory_to_sacrifice(sample_lines):
    fsd = nix_fs.get_FSDir_from_shell_transcript(sample_lines)
    sacrifice_dir = nix_fs.directory_to_sacrifice(fsd)
    assert sacrifice_dir._name == 'd'

def test_main(sample_file, monkeypatch, capsys):
    monkeypatch.setenv('INPUT_FILE', str(sample_file))
    nix_fs.main()
    written_to_output = capsys.readouterr().out
    assert written_to_output == 'Total size of dirs of size <=100000: 95437\nTotal size of sacrifice directory: 24933642\n'
