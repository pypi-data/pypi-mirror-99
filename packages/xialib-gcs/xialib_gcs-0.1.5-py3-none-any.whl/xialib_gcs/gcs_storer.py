import io
import os
import google.auth
import gcsfs
from xialib.storer import IOStorer

class GcsStorer(IOStorer):
    """Google Cloud Plateform Based
    """
    store_types = ['gcs']
    path_separator = "/"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'fs' in kwargs:
            if not isinstance(kwargs['fs'], gcsfs.GCSFileSystem):
                self.logger.error("GCSStorer Must have GCS based Filesystem")
                raise TypeError("XIA-000032")
            self.fs = kwargs['fs']
        else:
            self.fs = gcsfs.GCSFileSystem(**kwargs)
        self.project_id = google.auth.default()[1]

    def exists(self, location: str):
        return self.fs.exists(location)

    def walk_file(self, root_path):
        for root, dirs, files in self.fs.walk(root_path, topdown=False):
            for name in files:
                yield self.join(root, name)

    def join(self, *args):
        return '/'.join([item for item in args])

    def read(self, location: str) -> bytes:
        with self.fs.open(location, 'rb') as fp:
            return fp.read()

    def write(self, data_or_io, location: str) -> str:
        if isinstance(data_or_io, io.IOBase):
            with self.fs.open(location, 'wb') as fp:
                data_or_io.seek(0)
                chunk = data_or_io.read(2 ** 20)
                while chunk:
                    fp.write(chunk)
                    chunk = data_or_io.read(2 ** 20)
        elif isinstance(data_or_io, bytes):
            with self.fs.open(location, 'wb') as fp:
                fp.write(data_or_io)
        return location

    def remove(self, location: str) -> bool:
        if self.fs.exists(location):
            self.fs.rm(location)
            return True
        else:
            return False

    def mkdir(self, path: str):
        pass

    def get_io_stream(self, location: str):
        with self.fs.open(location, 'rb') as fp:
            yield fp

    def get_io_wb_stream(self, location: str):
        with self.fs.open(location, 'wb') as fp:
            yield fp
