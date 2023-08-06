import pytest
import io
import uuid
import warnings
from dli.client import builders
from dli.client.exceptions import (
    CatalogueEntityNotFoundException, InvalidPayloadException,
)
from tests.common import SdkIntegrationTestCase

@pytest.mark.integration
class DatasetTestCase(SdkIntegrationTestCase):

    @pytest.fixture(autouse=True)
    def capsys(self, capsys):
        self.capsys = capsys

    def setUp(self):
        super().setUp()

        self.package_id = self.create_package("test_dataset_functions")
        self.builder = self.dataset_builder(self.package_id, "test_dataset_functions")

    def create_datalake_dataset(self):
        return self.register_s3_dataset(
            package_id=self.package_id,
            dataset_name="test_dataset_functions",
            bucket_name="my-happy-bucket"
        )

    def test_get_unknown_dataset_raises_dataset_not_found_error(self):
        with self.assertRaises(CatalogueEntityNotFoundException):
            self.client.get_dataset("unknown")

    def test_can_create_with_data_preview(self):
        self._setup_bucket_and_prefix('test-bucket', 'test')

        csv = io.BytesIO(
            b'a,b,c\n'
            b'1,2,3'
        )

        csv.name = 'file/test.csv'
        dataset_name = f'datapreview-test-{uuid.uuid4()}'

        builder = self.dataset_builder(
            package_id=self.package_id,
            dataset_name=dataset_name,
            sample_data=csv,
            data_preview_type='STATIC'
        ).with_external_s3_storage(
            bucket_name='test-bucket',
            aws_account_id=self.aws_account_id,
            prefix='test'
        )

        dataset = self.client.register_dataset(builder)

        assert dataset.data_preview_file_name == 'test.csv'
        with dataset.sample_data.file() as f:
            assert f.read() == (
                b'a,b,c\n'
                b'1,2,3'
            )

    def test_builder_sample_data_validation(self):
        assert builders.DatasetBuilder(
            sample_data='1234',
            data_preview_type='STATIC'
        )

        assert builders.DatasetBuilder(
            sample_data='1234',
        )._data['sample_data']

        with pytest.raises(ValueError):
            assert builders.DatasetBuilder(
                sample_data='1234',
                data_preview_type='LIVE'
            )

    def test_can_edit_with_data_preview(self):
        self._setup_bucket_and_prefix('test-bucket', 'test')

        csv = io.BytesIO(
            b'a,b,c\n'
            b'1,2,3'
        )

        csv.name = 'test.csv'
        dataset_name = f'datapreview-test-{uuid.uuid4()}'

        builder = self.dataset_builder(
            package_id=self.package_id,
            dataset_name=dataset_name,
            sample_data=csv,
            data_preview_type='STATIC'
        ).with_external_s3_storage(
            bucket_name="test-bucket",
            aws_account_id=self.aws_account_id,
            prefix="test"
        )

        dataset = self.client.register_dataset(builder)

        csv = io.BytesIO(
            b'different,stuff\n'
            b'more,file'
        )
        csv.name = 'new_test.csv'

        dataset = self.client.edit_dataset(
            dataset.dataset_id,
            sample_data=csv,
        )

        with dataset.sample_data.file() as f:
            assert f.read() == (
                b'different,stuff\n'
                b'more,file'
            )

    def test_can_get_dataset_by_short_code(self):
        builder = self.builder.with_external_storage(
            location="jdbc://connectionstring:1232/my-db"
        )
        short_code = f'testGetByShortCode{str(uuid.uuid4())[:8]}'
        builder._data.update({'short_code': short_code})
        expected = self.client.register_dataset(builder)

        dataset_by_short_code = self.client.get_dataset(
            dataset_short_code=short_code
        )
        self.assertEqual(expected.dataset_id, dataset_by_short_code.dataset_id)

    def test_get_dataset_by_short_code_returns_404_if_organisation_does_not_match(self):
        self.builder.with_external_storage(
            location="jdbc://connectionstring:1232/my-db"
        )

        with pytest.raises(CatalogueEntityNotFoundException):
            self.client.get_dataset(
                dataset_short_code='testdatasetfunctions', organisation_short_code='abc'
            )

    def test_can_get_dataset_by_id_or_name(self):
        builder = self.builder.with_external_storage(
            location="jdbc://connectionstring:1232/my-db"
        )
        package = self.client.get_package(id=self.package_id)
        expected = self.client.register_dataset(builder)
        actual = self.client.get_dataset(expected.dataset_id)

        self.assertEqual(expected.dataset_id, actual.dataset_id)

        # By id
        dataset_by_id = self.client.get_dataset(id=expected.dataset_id)
        self.assertEqual(expected.dataset_id, dataset_by_id.dataset_id)

        # By name and package id
        dataset_by_name_and_package_id = self.client.get_dataset(name=expected.name, package_id=package.id)
        self.assertEqual(expected.dataset_id, dataset_by_name_and_package_id.dataset_id)

        # By name and package name
        dataset_by_name_and_package_name = self.client.get_dataset(name=expected.name, package_name=package.name)
        self.assertEqual(expected.dataset_id, dataset_by_name_and_package_name.dataset_id)

        # By name and package name and package id
        dataset_by_name_and_package_name_and_id = self.client.get_dataset(name=expected.name,
                                                                          package_id=package.id,
                                                                          package_name=package.name)
        self.assertEqual(expected.dataset_id, dataset_by_name_and_package_name_and_id.dataset_id)

        # By bad dataset name, valid package name
        with self.assertRaises(Exception):
            dataset_by_baddataset_name = self.client.get_dataset(
                name="bad name",
                package_id=package.package_id,
                package_name=package.name)

        # By dataset name, invalid package name
        with self.assertRaises(Exception):
            dataset_by_badpackage_name = self.client.get_dataset(
                name=expected.name,
                package_name="bad name")

        # No package deets
        with self.assertRaises(Exception):
            dataset_by_name_no_package = self.client.get_dataset(
                name="bad name")

        # No dataset deets
        with self.assertRaises(Exception):
            dataset_by_package_name_no_dataset = self.client.get_dataset(
                package_name="bad")


    def test_cannot_get_dataset_by_name_if_package_id_and_package_name_mismatch(self):
        builder = self.builder.with_external_storage(
            location="jdbc://connectionstring:1232/my-db"
        )
        package = self.client.get_package(id=self.package_id)
        dataset = self.client.register_dataset(builder)

        with self.assertRaises(CatalogueEntityNotFoundException):
            self.client.get_dataset(name=dataset.name, package_id=package.id, package_name="unknown")
            self.client.get_dataset(name=dataset.name, package_id="unknown", package_name=package.name)

    def test_retrieve_keys_for_unknown_dataset_raises_error(self):
        with self.assertRaises(CatalogueEntityNotFoundException):
            self.client.get_s3_access_keys_for_dataset("unknown")

    def test_can_retrieve_keys_for_single_dataset(self):
        dataset = self.create_datalake_dataset()
        keys = self.client.get_s3_access_keys_for_dataset(dataset.dataset_id)

        self.assertIsNotNone(keys.access_key_id)
        self.assertIsNotNone(keys.session_token)
        self.assertIsNotNone(keys.secret_access_key)

    def test_can_retrieve_keys_for_multiple_datasets(self):
        dataset1 = self.register_s3_dataset(
            package_id=self.package_id, dataset_name="dataset1", bucket_name="my-happy-bucket-1"
        )
        dataset2 = self.register_s3_dataset(
            package_id=self.package_id, dataset_name="dataset2", bucket_name="my-happy-bucket-2"
        )

        keys = self.client.get_s3_access_keys_for_dataset(
            dataset1.dataset_id,
            dataset2.dataset_id
        )

        self.assertIsNotNone(keys.access_key_id)
        self.assertIsNotNone(keys.session_token)
        self.assertIsNotNone(keys.secret_access_key)

    def test_can_not_create_dataset_without_location(self):
        with self.assertRaises(Exception):
            self.client.register_dataset(self.builder)

    def test_can_create_dataset_with_other_location(self):
        builder = self.builder.with_external_storage(
            location="jdbc://connectionstring:1232/my-db"
        )
        dataset = self.client.register_dataset(builder)

        self.assertIsNotNone(dataset)
        self.assertEqual(dataset.description, self.builder.payload["description"])
        self.assertEqual(dataset.location.type, "Other")

    def test_can_create_dataset_with_short_code(self):

        dataset_name = f'datapreview-test-{uuid.uuid4()}'
        short_code = f'someRandomShortCode{str(uuid.uuid4())[:8]}'
        builder = self.dataset_builder(
            package_id=self.package_id,
            dataset_name=dataset_name,
            short_code=short_code,
        ).with_external_storage(
            location='jdbc://connectionstring:1232/my-db'
        )
        dataset = self.client.register_dataset(builder)

        self.assertIsNotNone(dataset)
        self.assertEqual(dataset.short_code, builder._data['short_code'])

    def test_can_create_dataset_with_external_bucket(self):
        dataset = self.register_s3_dataset(self.package_id, "test_dataset", "my-happy-external-bucket")

        self.assertIsNotNone(dataset)
        self.assertEqual(dataset.location.type, "S3")
        self.assertEqual(dataset.location.bucket, "my-happy-external-bucket")

    def test_can_edit_dataset_with_same_values(self):
        dataset = self.create_datalake_dataset()

        updated = self.client.edit_dataset(
            dataset.dataset_id,
            name=dataset.name,
            description=dataset.description,
            content_type=dataset.content_type,
            data_format=dataset.data_format
        )

        self.assertEqual(dataset.dataset_id, updated.dataset_id)
        self.assertEqual(dataset.package_id, updated.package_id)
        self.assertEqual(dataset.name, updated.name)
        self.assertEqual(dataset.location, updated.location)
        self.assertEqual(dataset.created_at, updated.created_at)
        # updated has changed
        self.assertNotEqual(dataset.updated_at, updated.updated_at)

    def test_can_edit_and_change_values(self):
        dataset = self.create_datalake_dataset()
        # change location to other
        builder = builders.DatasetLocationBuilder().with_external_storage("changing-location")

        updated = self.client.edit_dataset(
            dataset.dataset_id,
            location_builder=builder,
            description="new desc",
            content_type="Structured",
            keywords=["test", "2"],
            load_type="Full Load"
        )

        self.assertEqual(updated.dataset_id, dataset.dataset_id)
        self.assertEqual(updated.package_id, dataset.package_id)
        self.assertEqual(updated.name, dataset.name)
        self.assertEqual(updated.description, "new desc")
        self.assertEqual(updated.content_type, "Structured")
        self.assertEqual(updated.keywords, ["test", "2"])
        self.assertEqual(updated.location.type, "Other")
        self.assertEqual(updated.load_type, "Full Load")

    def test_can_create_dataset_with_load_type(self):
        dataset = self.client.register_dataset(builders.DatasetBuilder(
            package_id=self.package_id,
            name="dataset_with_load_type",
            description="a testing dataset",
            content_type="Structured",
            data_format="CSV",
            publishing_frequency="Daily",
            taxonomy=[],
            load_type="Incremental Load",
            data_preview_type="NONE"
        ).with_external_storage("test")
                                               )

        self.assertEqual(dataset.load_type, "Incremental Load")

    def test_can_delete_dataset(self):
        dataset = self.create_datalake_dataset()
        self.client.delete_dataset(dataset.dataset_id)

        with self.assertRaises(CatalogueEntityNotFoundException):
            self.client.get_dataset(dataset.dataset_id)

    def test_delete_unknown_dataset_raises_error(self):
        with self.assertRaises(CatalogueEntityNotFoundException):
            self.client.delete_dataset("unknown")

    def test_register_dataset_in_unknown_package_raises_error(self):
        builder = builders.DatasetBuilder(
            package_id="unknown",
            name="test",
            description="a testing dataset",
            content_type="Structured",
            data_format="CSV",
            publishing_frequency="Daily",
            taxonomy=[],
            data_preview_type="NONE"
        )
        builder = builder.with_external_storage("s3://my-happy-bucket")

        with self.assertRaises(CatalogueEntityNotFoundException):
            self.client.register_dataset(builder)

    def test_indirect_get_dataset_deprecation(self):
        builder = self.builder.with_external_storage(
            location="jdbc://connectionstring:1232/my-db"
        )
        expected = self.client.register_dataset(builder)

        def indirect_call():
            return self.client.get_dataset(expected.dataset_id)

        with warnings.catch_warnings(record=True) as ws:
            warnings.simplefilter("always")
            actual = indirect_call()
            found_deprecation = False
            for w in ws:
                if str(w.message).startswith("This method is deprecated and is scheduled for removal"):
                    found_deprecation = True

            assert found_deprecation is False

    def test_direct_get_dataset_deprecation(self):
        builder = self.builder.with_external_storage(
            location="jdbc://connectionstring:1232/my-db"
        )
        expected = self.client.register_dataset(builder)

        with warnings.catch_warnings(record=True) as ws:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            actual = self.client.get_dataset(expected.dataset_id)

            found_deprecation = False
            for w in ws:
                if str(w.message).startswith("This method is deprecated and is scheduled for removal"):
                    found_deprecation = True

            assert found_deprecation is True




@pytest.mark.integration
class DatasetDatafilesTestCase(SdkIntegrationTestCase):

    def setUp(self):
        super().setUp()

    def test_get_dataset_datafiles_raises_exception_if_dataset_does_not_exists(self):
        with self.assertRaises(Exception):
            self.client.get_datafiles("unknown")

    def test_get_dataset_datafiles_returns_empty_when_no_datafiles(self):
        package_id = self.create_package(
            name="test_get_dataset_datafiles_returns_empty_when_no_datafiles"
        )
        dataset = self.client.register_dataset(
            self.dataset_builder(
                package_id,
                "test_get_dataset_datafiles_returns_empty_when_no_datafiles"
            ).with_external_storage(location="jdbc://connectionstring:1232/my-db")
        )
        datafiles = self.client.get_datafiles(dataset.dataset_id)
        self.assertEqual(datafiles, [])

    def test_get_dataset_datafiles_returns_datafiles_for_dataset(self):
        files = [{'path': "/path/to/file/A", 'size': 99999}, {'path': "/path/to/file/B", 'size': 88888}]
        package_id = self.create_package(
            name="test_get_dataset_datafiles_returns_datafiles_for_dataset"
        )
        dataset = self.client.register_dataset(
            self.dataset_builder(
                package_id,
                "test_get_dataset_datafiles_returns_datafiles_for_dataset"
            ).with_external_storage(location="jdbc://connectionstring:1232/my-db")
        )

        for i in range(1, 4):
            self.client.register_datafile_metadata(
                dataset.dataset_id,
                "datafile %s" % i,
                files,
                data_as_of="2018-10-1%s" % i
            )

        datafiles = self.client.get_datafiles(dataset.dataset_id)
        self.assertEqual(len(datafiles), 3)

        datafiles_paged = self.client.get_datafiles(dataset.dataset_id, count=2)
        self.assertEqual(len(datafiles_paged), 2)

        # Other Lookup scenarios
        datafiles_search_by_as_of_date = self.client.get_datafiles(dataset.dataset_id, as_of_date_start='2018-10-12')
        self.assertEqual(len(datafiles_search_by_as_of_date), 2)
        self.assertTrue(all(df.name in ["datafile 2", "datafile 3"] for df in datafiles_search_by_as_of_date))

        datafiles_search_by_as_of_date = self.client.get_datafiles(dataset.dataset_id, as_of_date_end='2018-10-12')
        self.assertEqual(len(datafiles_search_by_as_of_date), 2)
        self.assertTrue(all(df.name in ["datafile 1", "datafile 2"] for df in datafiles_search_by_as_of_date))

        datafiles_search_by_as_of_date = self.client.get_datafiles(dataset.dataset_id, as_of_date_start='2018-10-10',
                                                                   as_of_date_end='2018-10-11')
        self.assertEqual(len(datafiles_search_by_as_of_date), 1)
        self.assertTrue(all(df.name == "datafile 1" for df in datafiles_search_by_as_of_date))

        datafiles_search_by_as_of_date = self.client.get_datafiles(dataset.dataset_id, name_contains='datafile 2',
                                                                   as_of_date_start='2018-10-10',
                                                                   as_of_date_end='2018-10-13')
        self.assertEqual(len(datafiles_search_by_as_of_date), 1)
        self.assertTrue(all(df.name == "datafile 2" for df in datafiles_search_by_as_of_date))

    def test_get_dataset_datafiles_raises_exception_for_invalid_as_of_date_params(self):
        package_id = self.create_package(
            name="test_get_dataset_datafiles_raises_exception_for_invalid_as_of_date_params"
        )
        dataset = self.client.register_dataset(
            self.dataset_builder(
                package_id,
                "test_get_dataset_datafiles_raises_exception_for_invalid_as_of_date_params"
            ).with_external_storage(location="jdbc://connectionstring:1232/my-db")
        )

        with self.assertRaises(InvalidPayloadException):
            self.client.get_datafiles(dataset.dataset_id, as_of_date_end='blah blah')
            self.client.get_datafiles(dataset.dataset_id, as_of_date_start='blah blah')
            self.client.get_datafiles(dataset.dataset_id, as_of_date_start='11/12/2017', as_of_date_end='15/12/2017')

    def test_get_dataset_datafiles_raises_error_for_invalid_count(self):
        self.assert_page_count_is_valid_for_paginated_resource_actions(
            lambda c: self.client.get_datafiles("some_dataset", count=c))

    def test_get_latest_datafile_raises_exception_if_dataset_does_not_exists(self):
        with self.assertRaises(Exception):
            self.client.get_latest_datafile("unknown")

    def test_get_latest_datafile_raises_exception_if_dataset_has_no_datafiles(self):
        package_id = self.create_package(
            name="test_get_latest_datafile_raises_exception_if_dataset_has_no_datafiles"
        )
        dataset = self.client.register_dataset(
            self.dataset_builder(
                package_id,
                "test_get_latest_datafile_raises_exception_if_dataset_has_no_datafiles"
            ).with_external_storage(location="jdbc://connectionstring:1232/my-db")
        )

        files = [{'path': "/path/to/file/A", 'size': 99999}, {'path': "/path/to/file/B", 'size': 88888}]
        for i in range(4, 0, -1):
            self.client.register_datafile_metadata(
                dataset.dataset_id,
                "datafile %s" % i,
                files,
                data_as_of="2018-10-1%s" % i
            )

        latest_datafile = self.client.get_latest_datafile(dataset.dataset_id)

        self.assertEqual(latest_datafile.name, 'datafile 4')

    def test_get_latest_datafile_returns_latest_datafile(self):
        package_id = self.create_package(
            name="test_get_latest_datafile_returns_latest_datafile"
        )
        dataset = self.client.register_dataset(
            self.dataset_builder(
                package_id,
                "test_get_latest_datafile_returns_latest_datafile"
            ).with_external_storage(location="jdbc://connectionstring:1232/my-db")
        )

        with self.assertRaises(Exception):
            self.client.get_latest_datafile(dataset.dataset_id)


@pytest.mark.integration
class DatasetSchemasTestCase(SdkIntegrationTestCase):

    def setUp(self):
        super().setUp()

        dataset = self.register_s3_dataset(
            package_id=self.create_package("test_dataset_schema_functions"),
            dataset_name="test_dataset_schema_functions",
            bucket_name="my-happy-bucket"
        )
        self.dataset_id = dataset.dataset_id

    def create_schema_payload(self, version, valid_as_of, **kwargs):
        payload = {
            'version': version,
            'valid_as_of': valid_as_of,
            'fields': [
                {
                    'name': 'field1',
                    'type': 'Int',
                    'nullable': True
                },
            ]
        }

        payload.update(**kwargs)
        return payload

    def test_cannot_register_dictionary_for_missing_or_unknown_dataset(self):
        with self.assertRaises(CatalogueEntityNotFoundException):
            self.client.register_dictionary(
                'unknown', version='1a', valid_as_of='2018-10-31', fields=[
                    {
                        'name': 'field2',
                        'nullable': False,
                        'type': 'Int',
                        'metadata': {
                            'random': 'keys'
                        }
                    },
                ])

    def test_cannot_register_dictionary_with_invalid_payload(self):
        my_schema_fields = [
            {
                'name': 'field1',
                'type': 'Int',
                'nullable': True
            },
        ]
        # fields cannot be empty or contain invalid field definitions
        with self.assertRaises(InvalidPayloadException):
            self.client.register_dictionary(self.dataset_id, version='1a', valid_as_of='2018-10-31', fields=None)
        with self.assertRaises(InvalidPayloadException):
            self.client.register_dictionary(self.dataset_id, version='1a', valid_as_of='2018-10-31',
                                        fields=[{'random': 'keys'}])

        # valid_as_of should be date in ISO format
        with self.assertRaises(InvalidPayloadException):
            self.client.register_dictionary(self.dataset_id, version='1a', valid_as_of='31/10/2018',
                                        fields=my_schema_fields)
        with self.assertRaises(InvalidPayloadException):
            self.client.register_dictionary(self.dataset_id, version='1a', valid_as_of='halloween', fields=my_schema_fields)

        # partitions if provided can be empty, but must not contain invalid key value pairs
        self.client.register_dictionary(self.dataset_id, version='1a', valid_as_of='2018-10-31',
                                    fields=my_schema_fields, partitions=[])
        with self.assertRaises(InvalidPayloadException):
            self.client.register_dictionary(self.dataset_id, version='1a', valid_as_of='2018-10-31',
                                        fields=my_schema_fields, partitions=[{'random': 'keys'}])

    def test_can_register_dictionary(self):
        my_schema_fields = [
            {
                'name': 'field1',
                'type': 'Int',
                'nullable': True
            },
            {
                'name': 'field2',
                'type': 'Int',
                'nullable': False,
                'metadata': {
                    'random': 'keys'
                }
            },
        ]
        my_schema_partitions = [
            {
                'name': 'Who goes there?',
                'type': 'Phantom'
            }
        ]
        params = {
            'version': '1a',
            'valid_as_of': '2018-10-31',
            'fields': my_schema_fields,
            'partitions': my_schema_partitions,
            'description': 'My Funky Schema',
        }

        schema = self.client.register_dictionary(self.dataset_id, **params)
        self.assertIsNotNone(schema)
        self.assertEqual(schema.version, params['version'])
        self.assertEqual(schema.valid_as_of, params['valid_as_of'])
        self.assertEqual(len(schema.fields), 2)
        self.assertTrue(all([f['name'] in ['field1', 'field2'] for f in schema.fields]))
        self.assertEqual(len(schema.partitions), 1)

    def test_cannot_get_schema_for_missing_or_unknown_dataset(self):
        with self.assertRaises(CatalogueEntityNotFoundException):
            self.client.get_dictionary(None)
        with self.assertRaises(CatalogueEntityNotFoundException):
            self.client.get_dictionary('unknown')

    def test_cannot_get_schema_for_dataset_with_no_schemas(self):
        with self.assertRaises(CatalogueEntityNotFoundException):
            self.client.get_dictionary(self.dataset_id)

    def test_can_get_schema_by_version(self):
        payload = self.create_schema_payload('1a', '2018-10-31')
        self.client.register_dictionary(self.dataset_id, **payload)
        schema = self.client.get_dictionary(self.dataset_id, payload['version'])
        self.assertIsNotNone(schema)
        self.assertEqual(schema.version, payload['version'])
        assert schema.fields

    def test_can_get_schema_without_version_returns_the_latest(self):
        payload_a = self.create_schema_payload('1a', '2018-10-31')
        payload_b = self.create_schema_payload('1b', '2018-11-05')

        self.client.register_dictionary(self.dataset_id, **payload_a)
        self.client.register_dictionary(self.dataset_id, **payload_b)

        schema = self.client.get_dictionary(self.dataset_id)
        self.assertIsNotNone(schema)
        self.assertEqual(schema.version, payload_b['version'])

    def test_cannot_get_dictionaries_for_missing_or_unknown_dataset(self):
        with self.assertRaises(CatalogueEntityNotFoundException):
            self.client.get_dictionaries(None)
        with self.assertRaises(CatalogueEntityNotFoundException):
            self.client.get_dictionaries('unknown')

    def test_get_dictionaries_returns_empty_for_dataset_with_no_schemas(self):
        self.assertEqual(self.client.get_dictionaries(self.dataset_id), [])

    def test_can_get_dictionaries_for_dataset_and_schemas_are_sorted_by_valid_as_of_date(self):
        payload_a = self.create_schema_payload('1a', '2018-10-31')
        payload_b = self.create_schema_payload('1b', '2018-11-05')
        payload_c = self.create_schema_payload('1c', '2018-11-02')

        self.client.register_dictionary(self.dataset_id, **payload_a)
        self.client.register_dictionary(self.dataset_id, **payload_b)
        self.client.register_dictionary(self.dataset_id, **payload_c)

        all_schemas = self.client.get_dictionaries(self.dataset_id)
        self.assertEqual(len(all_schemas), 3)
        self.assertEqual(all_schemas[0].version, payload_b['version'])

        fewer_schemas = self.client.get_dictionaries(self.dataset_id, count=2)
        self.assertEqual(len(fewer_schemas), 2)
        self.assertEqual(fewer_schemas[0].version, payload_b['version'])

    def test_cannot_delete_dictionary_for_missing_or_unknown_dataset(self):
        with self.assertRaises(CatalogueEntityNotFoundException):
            self.client.delete_dictionary(None, '1a')

        with self.assertRaises(CatalogueEntityNotFoundException):
            self.client.delete_dictionary('unknown', '1a')

    def test_cannot_delete_dictionary_if_missing_or_unknown_version(self):
        with self.assertRaises(CatalogueEntityNotFoundException):
            self.client.delete_dictionary(self.dataset_id, None)
        with self.assertRaises(CatalogueEntityNotFoundException):
            self.client.delete_dictionary(self.dataset_id, 'unknown')

    def test_can_delete_dictionary_by_version(self):
        # Create schema first
        payload = self.create_schema_payload('1a', '2018-10-31')
        self.client.register_dictionary(self.dataset_id, **payload)
        self.assertIsNotNone(self.client.get_dictionary(self.dataset_id, payload['version']))
        # Now Delete
        self.client.delete_dictionary(self.dataset_id, payload['version'])
        with self.assertRaises(CatalogueEntityNotFoundException):
            self.client.get_dictionary(self.dataset_id, payload['version'])

    def test_cannot_edit_dictionary_for_missing_or_unknown_dataset(self):
        with self.assertRaises(CatalogueEntityNotFoundException):
            self.client.edit_dictionary(None, '1a')
        with self.assertRaises(CatalogueEntityNotFoundException):
            self.client.edit_dictionary('unknown', '1a')

    def test_cannot_edit_dictionary_if_missing_or_unknown_version(self):
        with self.assertRaises(CatalogueEntityNotFoundException):
            self.client.edit_dictionary(self.dataset_id, None)
        with self.assertRaises(CatalogueEntityNotFoundException):
            self.client.edit_dictionary(self.dataset_id, 'unknown')

    def test_can_edit_dictionary_by_version(self):
        # Create schema first
        payload = self.create_schema_payload('1a', '2018-10-31')
        self.client.register_dictionary(self.dataset_id, **payload)
        self.assertIsNotNone(self.client.get_dictionary(self.dataset_id, payload['version']))
        # Now Update valid as of
        result = self.client.edit_dictionary(self.dataset_id, payload['version'], valid_as_of='2018-11-05')

        self.assertEqual(result.valid_as_of, '2018-11-05')
        # Can update version too if available
        result = self.client.edit_dictionary(self.dataset_id, payload['version'], new_version='1b')
        self.assertEqual(result.version, '1b')
        # version now updated
        with self.assertRaises(CatalogueEntityNotFoundException):
            self.client.get_dictionary(self.dataset_id, payload['version'])

