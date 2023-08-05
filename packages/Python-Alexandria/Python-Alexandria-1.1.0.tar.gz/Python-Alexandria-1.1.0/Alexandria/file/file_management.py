import os
import re
from itertools import chain

from Alexandria.general.project import root


def find_file(extension, path=None):
    """
    :param extension: File extension
    :param path: root/path
    :return: Single file.extension in folder
    """
    r = re.compile(f'.*{extension}?')
    tgt = os.path.join(root(), path) if not isinstance(path, type(None)) else root()
    f = list((filter(r.match, list(chain.from_iterable(chain.from_iterable(os.walk(tgt)))))))[0]
    return os.path.join(str(root()), f)
