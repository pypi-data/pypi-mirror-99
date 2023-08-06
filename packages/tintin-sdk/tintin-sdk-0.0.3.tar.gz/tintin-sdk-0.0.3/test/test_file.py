import os
import unittest
from unittest import mock

from tintin.file import FileManager 

debug = False
host = 'https://api.tintin.footprint-ai.com'
m = mock.patch.dict(os.environ, { 'TINTIN_SESSION_TEMPLATE_PROJECT_ID': '427wr4e8lno9gjgzmd6kp03vxyz51w',
'TINTIN_SESSION_TEMPLATE_PROJECT_TOKEN_MINIO_DOWNLOAD': 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiIqLmZvb3RwcmludC1haS5jb20iLCJleHAiOjIyNDczNzI0ODMsImp0aSI6IjYwNjc5YzRhLTA2MzItNDJjYS05NjdiLTNiYTIwNTVmZjlhMiIsImlhdCI6MTYxNjY1MjQ4MywiaXNzIjoiYXV0aG9yaXphdGlvbi5mb290cHJpbnQtYWkuY29tIiwibmJmIjoxNjE2NjUyNDgzfQ.U5xM9jryw-nMXHN6Ly55juDPiiYgLFj3xC5s9J0B3BcH43MoQn8Gs-2WXG8CZs7tCZbasysjc2X1oQyL4_5DQg',
})

class TestFileDownload(unittest.TestCase):
    global m
    global host
    global debug

    def test_http_file_download(self):
        m.start()
        mgr = FileManager(host, debug)
        self.assertEqual(mgr.download('/tmp',
            ['https://api.tintin.footprint-ai.com/api/v1/project/427wr4e8lno9gjgzmd6kp03vxyz51w/minio/object/testdata/1.jpg'],
        ), True)
        m.stop()

    def test_localpath_file_download(self):
        m.start()
        mgr = FileManager(host, debug)
        self.assertEqual(mgr.download('/tmp',
            ['/testdata/1.jpg'],
        ), True)
        m.stop()

    def test_localpath_download_notfound(self):
        m.start()
        mgr = FileManager(host, debug)
        self.assertEqual(mgr.download('/tmp',
            ['/testdata/notfound.jpg'],
        ), False)
        m.stop()

    def test_localpath_dir_download(self):
        m.start()
        mgr = FileManager(host, debug)
        self.assertEqual(mgr.download('/tmp',
            ['/testdata'],
            debug,
        ), True)
        m.stop()

class TestFileUpload(unittest.TestCase):
    global m
    global host
    global debug

    def test_folder_upload(self):
        m.start()
        mgr = FileManager(host, debug)
        # should upload to /testupload/testdata/...
        self.assertEqual(mgr.upload('/testupload', './testdata'), True)
        m.stop()

    def test_file_upload(self):
        m.start()
        mgr = FileManager(host, debug)
        # should upload to /testupload/testdata/1.txt individual file
        self.assertEqual(mgr.upload('/testupload', './testdata/1.txt'), True)
        m.stop()

if __name__ == '__main__':
    unittest.main()
