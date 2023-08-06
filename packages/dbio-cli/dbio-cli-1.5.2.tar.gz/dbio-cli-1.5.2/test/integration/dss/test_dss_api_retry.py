#!/usr/bin/env python
# coding: utf-8
import io
import os
import socket
import sys
import tempfile
import unittest
import uuid
from datetime import datetime
from requests import ConnectTimeout
from urllib3 import Timeout
from unittest import mock

pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))  # noqa
sys.path.insert(0, pkg_root)  # noqa

import dbio.dss
from dbio.util import RetryPolicy
from dbio.dss import upload_to_cloud
from dbio.dss.util import check_s3_bucket_exists
from . import TEST_BUCKET_NAME


@unittest.skipIf(check_s3_bucket_exists(TEST_BUCKET_NAME), "Test bucket does not exist")
class TestDssApiRetry(unittest.TestCase):
    staging_bucket = TEST_BUCKET_NAME
    source_url = None

    @classmethod
    def setUpClass(cls):
        with tempfile.TemporaryDirectory() as src_dir:
            bundle_path = os.path.join(src_dir, "bundle")
            os.makedirs(bundle_path)
            hello_world_path = os.path.join(bundle_path, "hello_world")

            with io.open(hello_world_path, "wb+") as fh:
                fh.write(b"HELLO WORLD")
                fh.flush()
                fh.seek(0)
                _, uploaded_keys, _ = upload_to_cloud(
                    [fh],
                    staging_bucket=TestDssApiRetry.staging_bucket,
                    replica="aws",
                    from_cloud=False,
                )

            TestDssApiRetry.source_url = "s3://{}/{}".format(TestDssApiRetry.staging_bucket, uploaded_keys[0])

    def test_get_retry(self):
        """
        Test that GET methods are retried.  We instruct the server to fake a 504 with some probability, and we should
        retry until successful.
        """
        client = dbio.dss.DSSClient()
        file_uuid = str(uuid.uuid4())
        creator_uid = client.config.get("creator_uid", 0)
        version = datetime.utcnow().strftime("%Y-%m-%dT%H%M%S.%fZ")

        client.put_file._request(
            dict(
                uuid=file_uuid,
                version=version,
                bundle_uuid=str(uuid.uuid4()),
                creator_uid=creator_uid,
                source_url=TestDssApiRetry.source_url,
            ),
        )
        client.get_file._request(
            dict(
                uuid=file_uuid,
                replica="aws",
            ),
            headers={
                'DSS_FAKE_504_PROBABILITY': "0.5",
            },
        )

    def test_timeouts(self):
        # This doesn't cover the read timeout because that is harder to mock without adversely affecting the
        # environment we're running in, but if we observe that the `requests` library correctly applies the
        # connection timeout we can safely assume that would also apply the read timeout.
        client = dbio.dss.DSSClient()
        client.timeout_policy = Timeout(connect=.123, read=.234)
        # Prevent unnecessary retries on socket.connect() that don't contribute to code coverage
        client.retry_policy = RetryPolicy(connect=0)
        with mock.patch('socket.socket.settimeout') as mock_settimeout:
            with mock.patch('socket.socket.connect') as mock_connect:
                mock_connect.side_effect = socket.timeout
                self.assertRaises(ConnectTimeout, client.get_bundle, uuid=str(uuid.uuid4()), replica='gcp')
            settimeout_calls, connect_calls = mock_settimeout.mock_calls, mock_connect.mock_calls
            # If a domain name resolves to more than one IP (multiple A records with the same name), urllib3 will
            # try each one in turn. That's why we may observe multiple calls to settimeout() and connect(). But they
            # should come in pairs. We don't care what connect() was called with, only settimout().
            self.assertEqual(len(settimeout_calls), len(connect_calls))
            self.assertEqual(settimeout_calls, [mock.call(.123)] * len(settimeout_calls))


if __name__ == "__main__":
    unittest.main()
