import json
import gzip
from functools import reduce
from typing import List, Union
from xialib.adaptor import FileAdaptor
from xialib.storer import RWStorer

class JsonAdaptor(FileAdaptor):
    """Adaptor for exporting json files

    Notes:
        Each dataset is ordered by sequence and will be seperated into two files: Delete File and Insert File.
        The correction reconstruction order is: Seq-1-D -> Seq-1-I -> Seq-2-D -> Seq-2-I

    """
    def __init__(self, fs: RWStorer, location: str, compress: bool = False, **kwargs):
        super().__init__(fs=fs, location=location, **kwargs)
        self.compress = compress

    def _write_content(self, file_path: str, data: List[dict]):
        if not self.compress:
            content = json.dumps(data, ensure_ascii=False).encode()
            self.storer.write(content, file_path + ".json")
        else:
            content = gzip.compress(json.dumps(data, ensure_ascii=False).encode())
            self.storer.write(content, file_path + ".json.gz")
        return True