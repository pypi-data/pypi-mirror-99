#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from concurrent import futures
from typing import List

from google.api_core.exceptions import GoogleAPIError, NotFound

from polyaxon.connections.gcp.base import GCPService
from polyaxon.exceptions import (
    PolyaxonPathException,
    PolyaxonSchemaError,
    PolyaxonStoresException,
)
from polyaxon.logger import logger
from polyaxon.parser import parser
from polyaxon.stores.base_store import StoreMixin
from polyaxon.utils.date_utils import file_modified_since
from polyaxon.utils.path_utils import (
    append_basename,
    check_dirname_exists,
    get_files_in_path_context,
)


class GCSService(GCPService, StoreMixin):
    """
    Google cloud store Service.
    """

    @staticmethod
    def parse_gcs_url(gcs_url):
        """
        Parses and validates a google cloud storage url.

        Returns:
            tuple(bucket_name, blob).
        """
        try:
            spec = parser.parse_gcs_path(gcs_url)
            return spec.bucket, spec.blob
        except PolyaxonSchemaError as e:
            raise PolyaxonStoresException(e)

    def get_bucket(self, bucket_name):
        """
        Gets a bucket by name.

        Args:
            bucket_name: `str`. Name of the bucket
        """
        return self.connection.get_bucket(bucket_name)

    def check_blob(self, blob, bucket_name=None):
        """
        Checks for the existence of a file in Google Cloud Storage.

        Args:
            blob: `str`. the path to the object to check in the Google cloud storage bucket.
            bucket_name: `str`. Name of the bucket in which the file is stored
        """
        try:
            return bool(self.get_blob(blob=blob, bucket_name=bucket_name))
        except Exception as e:
            logger.info("Block does not exist %s", e)
            return False

    def get_blob(self, blob, bucket_name=None):
        """
        Get a file in Google Cloud Storage.

        Args:
            blob: `str`. the path to the object to check in the Google cloud storage bucket.
            bucket_name: `str`. Name of the bucket in which the file is stored
        """
        if not bucket_name:
            bucket_name, blob = self.parse_gcs_url(blob)

        bucket = self.get_bucket(bucket_name)
        # Wrap google.cloud.storage's blob to raise if the file doesn't exist
        obj = bucket.get_blob(blob)

        if obj is None:
            raise PolyaxonStoresException("File does not exist: {}".format(blob))

        return obj

    def ls(self, path):
        results = self.list(key=path)
        return {"files": results["blobs"], "dirs": results["prefixes"]}

    def list(
        self, key, bucket_name=None, path=None, delimiter="/", blobs=True, prefixes=True
    ):
        """
        List prefixes and blobs in a bucket.

        Args:
            key: `str`. a key prefix.
            bucket_name: `str`. the name of the bucket.
            path: `str`. an extra path to append to the key.
            delimiter: `str`. the delimiter marks key hierarchy.
            blobs: `bool`. if it should include blobs.
            prefixes: `bool`. if it should include prefixes.

        Returns:
             Service client instance
        """
        if not bucket_name:
            bucket_name, key = self.parse_gcs_url(key)

        bucket = self.get_bucket(bucket_name)

        if key and not key.endswith("/"):
            key += "/"

        prefix = key
        if path:
            prefix = os.path.join(prefix, path)

        if prefix and not prefix.endswith("/"):
            prefix += "/"

        def get_iterator():
            return bucket.list_blobs(prefix=prefix, delimiter=delimiter)

        def get_blobs(_blobs):
            list_blobs = []
            for blob in _blobs:
                name = blob.name[len(key) :]
                size = blob.size
                if all([name, size]):
                    list_blobs.append((name, blob.size))
            return list_blobs

        def get_prefixes(_prefixes):
            list_prefixes = []
            for folder_path in _prefixes:
                name = folder_path[len(key) : -1]
                list_prefixes.append(name)
            return list_prefixes

        results = {"blobs": [], "prefixes": []}

        if blobs:
            iterator = get_iterator()
            results["blobs"] = get_blobs(list(iterator))

        if prefixes:
            iterator = get_iterator()
            for page in iterator.pages:
                results["prefixes"] += get_prefixes(page.prefixes)

        return results

    def upload_file(self, filename, blob, bucket_name=None, use_basename=True):
        """
        Uploads a local file to Google Cloud Storage.

        Args:
            filename: `str`. the file to upload.
            blob: `str`. blob to upload to.
            bucket_name: `str`. the name of the bucket.
            use_basename: `bool`. whether or not to use the basename of the filename.
        """
        if not bucket_name:
            bucket_name, blob = self.parse_gcs_url(blob)

        if use_basename:
            blob = append_basename(blob, filename)

        bucket = self.get_bucket(bucket_name)
        bucket.blob(blob).upload_from_filename(filename)

    def download_file(self, blob, local_path, bucket_name=None, use_basename=True):
        """
        Downloads a file from Google Cloud Storage.

        Args:
            blob: `str`. blob to download.
            local_path: `str`. the path to download to.
            bucket_name: `str`. the name of the bucket.
            use_basename: `bool`. whether or not to use the basename of the blob.
        """
        if not bucket_name:
            bucket_name, blob = self.parse_gcs_url(blob)

        local_path = os.path.abspath(local_path)

        if use_basename:
            local_path = append_basename(local_path, blob)

        try:
            check_dirname_exists(local_path)
        except PolyaxonPathException as e:
            raise PolyaxonStoresException("Connection error: %s" % e) from e

        try:
            blob = self.get_blob(blob=blob, bucket_name=bucket_name)
            blob.download_to_filename(local_path)
        except (NotFound, GoogleAPIError) as e:
            raise PolyaxonStoresException("Connection error: %s" % e) from e

    def upload_dir(
        self,
        dirname,
        blob,
        bucket_name=None,
        use_basename=True,
        workers=0,
        last_time=None,
        exclude: List[str] = None,
    ):
        """
        Uploads a local directory to Google Cloud Storage.

        Args:
            dirname: `str`. name of the directory to upload.
            blob: `str`. blob to upload to.
            bucket_name: `str`. the name of the bucket.
            use_basename: `bool`. whether or not to use the basename of the directory.
            last_time: `datetime`. if provided,
                        it will only upload the file if changed after last_time.
            exclude: `list`. List of paths to exclude.
        """
        if not bucket_name:
            bucket_name, blob = self.parse_gcs_url(blob)

        if use_basename:
            blob = append_basename(blob, dirname)

        pool, future_results = self.init_pool(workers)

        # Turn the path to absolute paths
        dirname = os.path.abspath(dirname)
        with get_files_in_path_context(dirname, exclude=exclude) as files:
            for f in files:

                # If last time is provided we check if we should re-upload the file
                if last_time and not file_modified_since(
                    filepath=f, last_time=last_time
                ):
                    continue

                file_blob = os.path.join(blob, os.path.relpath(f, dirname))
                future_results = self.submit_pool(
                    workers=workers,
                    pool=pool,
                    future_results=future_results,
                    fn=self.upload_file,
                    filename=f,
                    blob=file_blob,
                    bucket_name=bucket_name,
                    use_basename=False,
                )

        if workers:
            futures.wait(future_results)
            self.close_pool(pool=pool)

    def download_dir(
        self, blob, local_path, bucket_name=None, use_basename=True, workers=0
    ):
        """
        Download a directory from Google Cloud Storage.

        Args:
            blob: `str`. blob to download.
            local_path: `str`. the path to download to.
            bucket_name: `str`. Name of the bucket in which to store the file.
            use_basename: `bool`. whether or not to use the basename of the key.
            workers: number of workers threads to use for parallel execution.
        """
        if not bucket_name:
            bucket_name, blob = self.parse_gcs_url(blob)

        local_path = os.path.abspath(local_path)

        if use_basename:
            local_path = append_basename(local_path, blob)

        try:
            check_dirname_exists(local_path, is_dir=True)
        except PolyaxonPathException:
            os.makedirs(local_path)

        results = self.list(bucket_name=bucket_name, key=blob, delimiter="/")

        # Create directories
        for prefix in sorted(results["prefixes"]):
            direname = os.path.join(local_path, prefix)
            prefix = os.path.join(blob, prefix)
            # Download files under
            self.download_dir(
                blob=prefix,
                local_path=direname,
                bucket_name=bucket_name,
                use_basename=False,
            )

        pool, future_results = self.init_pool(workers)

        # Download files
        for file_key in results["blobs"]:
            file_key = file_key[0]
            filename = os.path.join(local_path, file_key)
            file_key = os.path.join(blob, file_key)
            future_results = self.submit_pool(
                workers=workers,
                pool=pool,
                future_results=future_results,
                fn=self.download_file,
                blob=file_key,
                local_path=filename,
                bucket_name=bucket_name,
                use_basename=False,
            )

        if workers:
            futures.wait(future_results)
            self.close_pool(pool=pool)

    def delete(self, key, bucket_name=None, workers=0):
        if not bucket_name:
            bucket_name, key = self.parse_gcs_url(key)

        results = self.list(bucket_name=bucket_name, key=key, delimiter="/")
        if not any([results["prefixes"], results["blobs"]]):
            self.delete_file(key=key, bucket_name=bucket_name)

        # Delete directories
        for prefix in sorted(results["prefixes"]):
            prefix = os.path.join(key, prefix)
            # Download files under
            self.delete(key=prefix, bucket_name=bucket_name)

        pool, future_results = self.init_pool(workers)

        # Delete files
        for file_key in results["blobs"]:
            file_key = file_key[0]
            file_key = os.path.join(key, file_key)
            future_results = self.submit_pool(
                workers=workers,
                pool=pool,
                future_results=future_results,
                fn=self.delete_file,
                key=file_key,
                bucket_name=bucket_name,
            )

        if workers:
            futures.wait(future_results)
            self.close_pool(pool=pool)

    def delete_file(self, key, bucket_name=None):
        if not bucket_name:
            bucket_name, key = self.parse_gcs_url(key)
        bucket = self.get_bucket(bucket_name)
        try:
            return bucket.delete_blob(key)
        except (NotFound, GoogleAPIError) as e:
            raise PolyaxonStoresException("Connection error: %s" % e) from e
