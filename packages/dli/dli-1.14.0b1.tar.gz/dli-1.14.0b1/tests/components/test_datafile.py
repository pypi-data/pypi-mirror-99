import os

import pytest
import tempfile

from unittest.mock import MagicMock, call, patch
from dli.client.s3 import Client
from dli.client.exceptions import (
    CatalogueEntityNotFoundException,
    DatalakeException,
    DownloadFailed,
)
from tests.common import SdkIntegrationTestCase


@pytest.mark.integration
class DatafileTestCase(SdkIntegrationTestCase):

    def setUp(self):
        super().setUp()

        self.package_id = self.create_package("test_datafile_functions")
        self.dataset_name = "test_datafile_functions"
        self.builder = self.dataset_builder(
            self.package_id, self.dataset_name)

    def create_s3_dataset(self, bucket_name, prefix="prefix"):
        return self.register_s3_dataset(self.package_id, self.dataset_name, bucket_name, prefix=prefix)

    def create_dummy_datafile(self):
        dataset = self.register_s3_dataset(self.package_id, self.dataset_name, "test-bucket", "prefix")
        datafile = self.client.register_s3_datafile(
            dataset.dataset_id,
            "dummy",
            [os.path.relpath(__file__)],
            "prefix",
            data_as_of='2000-01-01'
        )

        return datafile

    def test_get_unknown_datafile_raises_exception(self):
        with self.assertRaises(CatalogueEntityNotFoundException):
            self.client.get_datafile("unknown")

    def test_get_unknown_s3_datafile_returns_error(self):
        with self.assertRaises(CatalogueEntityNotFoundException):
            self.client.get_s3_datafile("unknown")

    def test_can_get_s3_datafile(self):
        s3_dataset = self.create_s3_dataset("test-bucket")
        datafile = self.client.register_s3_datafile(
            s3_dataset.dataset_id,
            "test_get_s3_datafile",
            [os.path.relpath(__file__)],
            "prefix",
            data_as_of='2000-01-01'
        )


        s3_datafile = self.client.get_s3_datafile(datafile.datafile_id)
        self.assertEqual(s3_datafile.datafile_id, datafile.datafile_id)

    def test_register_datafile_metadata(self):
        files = [{'path': "/path/to/file/A", 'size': 99999},
                 {'path': "/path/to/file/B", 'size': 88888}]
        dataset = self.client.register_dataset(
            self.builder.with_external_storage(
                location="jdbc://connectionstring:1232/my-db"
            )
        )
        datafile = self.client.register_datafile_metadata(
            dataset.dataset_id,
            "test_register_dataset_metadata",
            files,
            data_as_of='2000-01-01'
        )

        self.assertEqual(datafile.dataset_id, dataset.dataset_id)
        self.assertEqual(datafile.files, files)

    def test_register_datafile_metadata_fails_when_data_as_of_is_invalid(self):
        files = [{'path': "/path/to/file/A", 'size': 99999},
                 {'path': "/path/to/file/B", 'size': 88888}]
        dataset = self.client.register_dataset(
            self.builder.with_external_storage(
                location="jdbc://connectionstring:1232/my-db"
            )
        )

        with self.assertRaises(ValueError):
            self.client.register_datafile_metadata(
                dataset.dataset_id,
                "test_register_dataset_metadata",
                files,
                data_as_of='2000-111-01'
            )

    def test_register_datafile_metadata_fails_when_no_files_provided(self):
        dataset = self.client.register_dataset(self.builder.with_external_storage(
            location="jdbc://connectionstring:1232/my-db"))
        with self.assertRaises(Exception):
            self.client.register_datafile_metadata(
                dataset.dataset_id,
                "test_register_datafile_metadata_fails_when_no_files_provided",
                files=[]
            )

    def test_update_datafile_fails_for_unknown_datafile(self):
        with self.assertRaises(CatalogueEntityNotFoundException):
            self.client.edit_datafile_metadata("unknown")

    def test_register_s3_datafile_can_create_datafile_uploading_files(self):
        with patch('dli.client.s3.Client.upload_files_to_s3',
                   self.patch_upload_files_to_s3) as s3_upload:
            dataset = self.create_s3_dataset("dev-ihsm-dl-pkg-test")
            file = os.path.relpath(__file__)  # upload ourselves as a dataset
            datafile = self.client.register_s3_datafile(
                dataset.dataset_id,
                "test_register_s3_datafile_can_create_datafile_uploading_files",
                [file],
                "prefix",
                data_as_of='2000-01-01'
            )


            self.assertIsNotNone(datafile)
            self.assertEqual(datafile.dataset_id, dataset.dataset_id)
            self.assertEqual(datafile.files, [
                {"path": "s3://dev-ihsm-dl-pkg-test/prefix/" +
                    os.path.basename(file)}
            ])

    def test_register_datafile_metadata_on_datalake_dataset(self):
        dataset = self.create_s3_dataset("dev-ihsm-dl-pkg-test")
        file = os.path.relpath(__file__)  # upload ourselves as a dataset
        datafile = self.client.register_datafile_metadata(
            dataset.dataset_id,
            "test_register_datafile_metadata_on_datalake_dataset",
            [
                {"path": "s3://dev-ihsm-dl-pkg-test/prefix/test"}
            ],
            data_as_of='2000-01-01'
        )

        self.assertIsNotNone(datafile)
        self.assertEqual(datafile.dataset_id, dataset.dataset_id)

    def test_update_datafile_metadata_fails_when_data_as_of_is_invalid(self):
        datafile = self.create_dummy_datafile()
        with self.assertRaises(ValueError):
            self.client.edit_datafile_metadata(
                datafile.datafile_id,
                name="correct name",
                data_as_of="dataAsOf"
            )

    def test_update_datafile_merges_changes_with_existing_datafile(self):
        datafile = self.create_dummy_datafile()
        updated = self.client.edit_datafile_metadata(
            datafile.datafile_id,
            name="correct name"
        )

        self.assertEqual(datafile.datafile_id, updated.datafile_id)
        self.assertEqual(datafile.dataset_id, updated.dataset_id)
        self.assertEqual(datafile.files, updated.files)
        self.assertEqual(updated.name, "correct name")

    def test_can_delete_datafile(self):
        datafile = self.create_dummy_datafile()
        # delete the datafile
        self.client.delete_datafile(datafile.datafile_id)
        # can't read it back
        with self.assertRaises(CatalogueEntityNotFoundException):
            self.client.get_datafile(datafile.datafile_id)

    def test_delete_unknown_datafile_raises_exception(self):
        with self.assertRaises(CatalogueEntityNotFoundException):
            self.client.delete_datafile("unknown")

    def test_can_add_files_to_existing_datafile(self):
        with patch('dli.client.s3.Client.upload_files_to_s3',
                   self.patch_upload_files_to_s3) as s3_upload:
            file = os.path.relpath(__file__)  # upload ourselves as a dataset
            file2 = '../test_sandbox/samples/data/AAPL.csv'

            dataset = self.create_s3_dataset("dev-ihsm-dl-pkg-test")
            datafile = self.client.register_s3_datafile(
                dataset.dataset_id,
                "test_can_add_files_to_existing_datafile",
                [file],
                "prefix",
                data_as_of='2000-01-01'
            )


            updated = self.client.add_files_to_datafile(
                datafile.datafile_id, 'prefix', [file2])

            # countEqual asserts that the collections match disrespect of order
            # talk about naming stuff
            self.assertCountEqual(
                [
                    {"path": "s3://dev-ihsm-dl-pkg-test/prefix/" +
                        os.path.basename(file)},
                    {"path": "s3://dev-ihsm-dl-pkg-test/prefix/" +
                        os.path.basename(file2)}
                ],
                updated.files
            )

    def test_add_files_to_unknown_datafile_raises_exception(self):
        with self.assertRaises(CatalogueEntityNotFoundException):
            self.client.add_files_to_datafile(
                'unknown', 'prefix', ["/path/to/file/A"])

    def test_register_datafile_to_nonexisting_dataset_raises_exception(self):
        with self.assertRaises(DatalakeException) as context:
            self.client.register_datafile_metadata(
                "unkknown",
                "test_register_datafile_to_nonexisting_dataset_raises_exception",
                [{'path': "/path/to/file/A"}, {'path': "/path/to/file/B"}],
                data_as_of='2000-01-01'
            )
            self.assertTrue(
                'Dataset with id unknown not found' in context.exception)


@pytest.mark.integration
class DownloadDatafileTestCase(SdkIntegrationTestCase):

    def setUp(self):
        super().setUp()
        # create a package
        self.package_id = self.create_package("test download datafile")
        self.dataset_name = "test download datafile"
        self.builder = self.dataset_builder(
            self.package_id, self.dataset_name)

    def create_s3_dataset(self, bucket_name, prefix="prefix"):
        return self.register_s3_dataset(self.package_id, self.dataset_name, bucket_name, prefix)

    def test_download_datafile_for_unknown_datafile_fails(self):
        with self.assertRaises(Exception):
            self.client.download_datafile("unknown")

    def test_download_datafile_retrieves_all_files_in_datafile(self):
        with patch('dli.client.s3.Client.upload_files_to_s3',
                   self.patch_upload_files_to_s3) as s3_upload:
            dataset = self.create_s3_dataset("dev-ihsm-dl-pkg-test")
            datafile = self.client.register_s3_datafile(
                dataset.dataset_id,
                "test_download_dataset_retrieves_all_files_in_dataset",
                [
                    '../test_sandbox/samples/data/AAPL.csv',
                    '../test_sandbox/samples/data/MSFT.csv'
                ],
                "prefix",
                '2000-01-01'
            )

            with patch('dli.client.s3.Client.download_files_from_s3_path') \
                    as s3_download:
                with tempfile.TemporaryDirectory() as dest:
                    self.client.download_datafile(
                        datafile.datafile_id,
                        dest,
                        flatten=False
                    )

                    # validate we got the expected calls
                    s3_download.assert_has_calls([
                        call(
                            destination=dest,
                            flatten=False,
                            s3_path="s3://dev-ihsm-dl-pkg-test/prefix/MSFT.csv",
                        ),
                        call(
                            destination=dest,
                            flatten=False,
                            s3_path = "s3://dev-ihsm-dl-pkg-test/prefix/AAPL.csv",
                        ),
                    ], any_order=True)

    def test_download_dataset_keeps_going_if_a_file_in_the_dataset_fails(self):
        with patch('dli.client.s3.Client.upload_files_to_s3',
                   self.patch_upload_files_to_s3) as s3_upload:
            def _download(_, file, dest):
                if file.endswith("AAPL.csv"):
                    raise Exception("")

            dataset = self.create_s3_dataset("dev-ihsm-dl-pkg-test")
            datafile = self.client.register_s3_datafile(
                dataset.dataset_id,
                "test_download_dataset_keeps_going_if_a_file_in_the_dataset_fails",
                [
                    '../test_sandbox/samples/data/AAPL.csv',
                    '../test_sandbox/samples/data/MSFT.csv'
                ],
                "prefix",
                '2000-01-01'
            )


            with self.assertRaises(DownloadFailed):
                with patch('dli.client.s3.Client.download_files_from_s3_path', _download) as s3_download:
                    with tempfile.TemporaryDirectory() as dest:
                        self.client.download_datafile(datafile.datafile_id, dest)

                        # validate we got the expected calls
                        s3_download.assert_has_calls([
                            call("s3://dev-ihsm-dl-pkg-test/prefix/MSFT.csv", dest),
                            call("s3://dev-ihsm-dl-pkg-test/prefix/AAPL.csv", dest),
                        ],
                            any_order=True
                        )


@pytest.mark.integration
class RegisterDatafileTestCase(SdkIntegrationTestCase):

    def set_s3_client_mock(self):
        """This prevents the s3 client from being mocked"""

    def create_and_get_dataset_id(self):
        package_id = self.create_package(
            "RegisterDatafileTestCase"
        )
        dataset = self.register_s3_dataset(
            package_id, "test", "dev-ihsm-dl-pkg-test"
        )

        return dataset.dataset_id

    def test_can_upload_datafile_when_provided_folder_with_relative_path(self):
        sample_data = os.path.join(
            os.path.dirname(__file__),
            '../../resources/yahoo'
        )

        datafile = self.client.register_s3_datafile(
            self.create_and_get_dataset_id(),
            "test_can_upload_datafile_when_provided_folder_with_relative_path",
            [sample_data],
            "prefix",
            '2000-01-01'
        )


        # assert the files were uploaded and that
        # their sizes have been resolved
        self.assertIn({
            "path": "s3://dev-ihsm-dl-pkg-test/prefix/AAPL.csv",
            "size": os.path.getsize(os.path.join(sample_data, "AAPL.csv"))
        },
            datafile.files
        )
        self.assertIn({
            "path": "s3://dev-ihsm-dl-pkg-test/prefix/MSFT.csv",
            "size": os.path.getsize(os.path.join(sample_data, "MSFT.csv"))
        },
            datafile.files
        )

    def test_can_upload_datafile_when_provided_s3_prefix_without_trailing_slash(self):
        sample_data = os.path.join(
            os.path.dirname(__file__),
            '../../resources/yahoo/AAPL.csv'
        )

        # Prefix Without trailing slash
        datafile = self.client.register_s3_datafile(
            self.create_and_get_dataset_id(),
            "test_can_upload_datafile_when_provided_s3_prefix_with_or_without_trailing_slashes 1",
            [sample_data],
            "prefix",
            '2000-01-01'
        )


        self.assertIn({
            "path": "s3://dev-ihsm-dl-pkg-test/prefix/AAPL.csv",
            "size": os.path.getsize(sample_data)
        },
            datafile.files
        )

    def test_can_upload_datafile_with_data_as_of_date_not_in_iso_format(self):
        sample_data = os.path.join(
            os.path.dirname(__file__),
            '../../resources/yahoo/AAPL.csv'
        )

        datafile = self.client.register_s3_datafile(
            self.create_and_get_dataset_id(),
            "test_can_upload_datafile_with_data_as_of_date_not_in_iso_format 1",
            [sample_data],
            "prefix",
            '3210-1-1'
        )


        assert self.client.get_datafile(datafile.datafile_id).data_as_of == '3210-01-01'
        assert {
            "path": "s3://dev-ihsm-dl-pkg-test/prefix/AAPL.csv",
            "size": os.path.getsize(sample_data)
        } in datafile.files

    def test_cannot_upload_datafile_with_invalid_data_as_of(self):
        sample_data = os.path.join(
            os.path.dirname(__file__),
            '../../resources/yahoo/AAPL.csv'
        )

        with self.assertRaises(ValueError):
            self.client.register_s3_datafile(
                self.create_and_get_dataset_id(),
                "test_can_upload_datafile_with_data_as_of_date_not_in_iso_format 1",
                [sample_data],
                "prefix",
                '2019-11-123'
            )

    def test_can_upload_datafile_files_recursively(self):
        sample_data = os.path.join(
            os.path.dirname(__file__),
            '../../resources/stocks'
        )

        datafile = self.client.register_s3_datafile(
            self.create_and_get_dataset_id(),
            "test_can_upload_datafile_files_recursively",
            [sample_data],
            "prefix",
            '2000-01-01'
        )


        # assert the files were uploaded and that
        # their sizes have been resolved
        self.assertIn({
            "path": "s3://dev-ihsm-dl-pkg-test/prefix/readme.txt",
            "size": os.path.getsize(os.path.join(sample_data, "readme.txt"))
        },
            datafile.files
        )
        self.assertIn({
            "path": "s3://dev-ihsm-dl-pkg-test/prefix/microsoft/MSFT.csv",
            "size": os.path.getsize(os.path.join(sample_data, "microsoft/MSFT.csv"))
        },
            datafile.files
        )
        self.assertIn({
            "path": "s3://dev-ihsm-dl-pkg-test/prefix/microsoft/AAPL.csv",
            "size": os.path.getsize(os.path.join(sample_data, "microsoft/AAPL.csv"))
        },
            datafile.files
        )
        self.assertIn({
            "path": "s3://dev-ihsm-dl-pkg-test/prefix/microsoft/cortana/master.txt",
            "size": os.path.getsize(os.path.join(sample_data, "microsoft/cortana/master.txt"))
        },
            datafile.files
        )


    def test_download_datafile_should_keep_folder_structure_as_in_datafile(self):
        download_file = MagicMock()

        class TestS3Client(Client):
            def __init__(self, *args):
                super().__init__(*args)
                self.s3_client.download_file = download_file

            def _list_objects(self, bucket, prefix):
                return [{
                    'Key': prefix
                }]

        with patch('dli.client.components.datafile.Client', TestS3Client) as client, \
             patch('dli.client.s3.os.makedirs') as makedirs_mock:
            sample_data = os.path.join(
                os.path.dirname(__file__),
                '../../resources/stocks'
            )
            datafile = self.client.register_s3_datafile(
                self.create_and_get_dataset_id(),
                "test_download_datafile_should_keep_folder_structure_as_in_datafile",
                [sample_data],
                "prefix",
                '2000-01-01'
            )

            self.client.download_datafile(datafile.datafile_id, '/var/abc/')

            directories_created = [
                d[0][0] for d in makedirs_mock.call_args_list if
                # Later version of boto I think create this automatically
                '.aws' not in d[0][0]
            ]

            files_created = [
                f[0][2] for f in download_file.call_args_list
            ]

            assert len(set(directories_created).intersection(set([
                '/var/abc/prefix',
                '/var/abc/prefix/microsoft',
                '/var/abc/prefix/microsoft/cortana'
            ]))) == len(set(directories_created))
            assert len(set(files_created).intersection(set([
                '/var/abc/prefix/readme.txt',
                '/var/abc/prefix/microsoft/MSFT.csv',
                '/var/abc/prefix/microsoft/AAPL.csv',
                '/var/abc/prefix/microsoft/cortana/master.txt'
            ]))) == len(files_created)

    def test_download_datafile_returns_paths_where_files_were_downloaded(self):
        download_file = MagicMock()

        class TestS3Client(Client):
            def __init__(self, *args):
                super().__init__(*args)
                self.s3_client.download_file = download_file

            def _list_objects(self, bucket, prefix):
                return [{
                    'Key': prefix
                }]

        with patch('dli.client.components.datafile.Client',
                   TestS3Client) as client, \
                patch('dli.client.s3.os.makedirs') as makedirs_mock:
            sample_data = os.path.join(
                os.path.dirname(__file__),
                '../../resources/stocks'
            )

            datafile = self.client.register_s3_datafile(
                self.create_and_get_dataset_id(),
                "test_download_datafile_should_keep_folder_structure_as_in_datafile",
                [sample_data],
                "prefix",
                '2000-01-01'
            )


            returned_list_of_files = self.client.download_datafile(
                datafile.datafile_id,'/var/abc/'
            )

            files_created = [
                '/var/abc/prefix/readme.txt',
                '/var/abc/prefix/microsoft/MSFT.csv',
                '/var/abc/prefix/microsoft/AAPL.csv',
                '/var/abc/prefix/microsoft/cortana/master.txt'
            ]
            assert len(set(returned_list_of_files).intersection(files_created)) == len(files_created)

    def test_flattened_download_datafile_returns_one_path(self):
        download_file = MagicMock()

        class TestS3Client(Client):
            def __init__(self, *args):
                super().__init__(*args)
                self.s3_client.download_file = download_file

            def _list_objects(self, bucket, prefix):
                return [{
                    'Key': prefix
                }]

        with patch('dli.client.components.datafile.Client',
                   TestS3Client) as client, \
                patch('dli.client.s3.os.makedirs') as makedirs_mock:
            sample_data = os.path.join(
                os.path.dirname(__file__),
                '../../resources/stocks'
            )

            datafile = self.client.register_s3_datafile(
                self.create_and_get_dataset_id(),
                "test_download_datafile_should_flatten_folder_structure",
                [sample_data],
                "prefix",
                '2000-01-01'
            )


            returned_list_of_files = self.client.download_datafile(
                datafile.datafile_id, '/var/abc/', flatten=True)

            files_created = [ # package_dataset_asof_filename
                '/var/abc/readme.txt',
                '/var/abc/MSFT.csv',
                '/var/abc/AAPL.csv',
                '/var/abc/master.txt'
            ]
            assert sorted(returned_list_of_files) == sorted(files_created)
