# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Files field tests."""


from io import BytesIO

from invenio_files_rest.models import Bucket, FileInstance, Location, ObjectVersion
from invenio_records.systemfields import ModelField
from invenio_records_resources.records.systemfields.files import FilesField

from invenio_records_marc21.records import Marc21Record as BaseMarc21Record
from invenio_records_marc21.records import RecordFile, models


class Record(BaseMarc21Record):
    """Test record class."""

    files = FilesField(store=True, file_cls=RecordFile)
    bucket_id = ModelField()
    bucket = ModelField(dump=False)


def test_class_attribute_access():
    """Test that field files returned."""
    assert isinstance(Record.files, FilesField)


def test_record_files_create(testapp, db):
    """Test record files bucket create."""
    record = Record.create({})
    assert record.bucket_id
    assert record.bucket
    assert record.files.enabled is True
    assert record.files.default_preview is None
    assert record.files.order == []
    assert len(record.files) == 0
    assert set(record.files) == set()

    assert record["files"]
    assert record["files"]["enabled"] is True
    assert "default_preview" not in record["files"]
    assert "order" not in record["files"]
    assert record["files"]["entries"] == {}


def test_record_file_update(testapp, db):
    """Test record files bucket update."""

    record = Record.create({})
    record.files["test.pdf"] = {"description": "A test file."}
    rf = record.files["test.pdf"]
    assert rf.key == "test.pdf"
    assert rf.object_version is None
    assert rf.object_version_id is None
    assert rf.record_id is not None
    assert rf.record_id == record.id
    assert rf.metadata == {"description": "A test file."}
    assert rf["metadata"] == {"description": "A test file."}
    db.session.commit()

    assert models.RecordFile.query.count() == 1
    assert ObjectVersion.query.count() == 0

    # Update
    record.files["test.pdf"] = {"description": "Update the file description"}
    rf = record.files["test.pdf"]
    assert rf.key == "test.pdf"
    assert rf.object_version is None
    assert rf.object_version_id is None
    assert rf.record_id is not None
    assert rf.record_id == record.id
    assert rf.metadata == {"description": "Update the file description"}
    assert rf["metadata"] == {"description": "Update the file description"}

    dummy_file = BytesIO(b"testfilestream")
    record.files["test.pdf"] = dummy_file
    rf = record.files["test.pdf"]
    assert rf.key == "test.pdf"
    assert rf.object_version
    assert rf.object_version_id
    assert rf.object_version.key == rf.key == "test.pdf"
    assert rf.object_version.file
    assert rf.metadata == {"description": "Update the file description"}
    assert rf["metadata"] == {"description": "Update the file description"}
    db.session.commit()

    assert FileInstance.query.count() == 1
    assert ObjectVersion.query.count() == 1

    # Delete the file
    del record.files["test.pdf"]
    record.commit()
    db.session.commit()

    assert models.RecordFile.query.count() == 0
    assert FileInstance.query.count() == 1
    assert ObjectVersion.query.count() == 2
    assert Bucket.query.count() == 1
    assert len(record.files) == 0
    assert "test.pdf" not in record.files
    assert record["files"]["entries"] == {}
    assert record["files"]["meta"] == {}


def test_record_files_delete(testapp, db):
    """Test record files bucket delete."""
    record = Record.create({})
    bucket_id = record.bucket_id
    db.session.commit()
    assert Bucket.query.count() == 1
    assert Bucket.query.get(bucket_id)

    record.delete()
    db.session.commit()

    assert Bucket.query.count() == 1


def test_record_files_clear(testapp, db):
    """Test clearing record files."""
    record = Record.create({})

    record.files["f1.pdf"] = (BytesIO(b"testfilestream"), {"description": "Test file"})
    record.files["f2.pdf"] = BytesIO(b"testfilestream")
    record.files["f3.pdf"] = {"description": "Metadata only"}
    record.commit()
    db.session.commit()

    assert models.RecordFile.query.count() == 3
    assert FileInstance.query.count() == 2
    assert ObjectVersion.query.count() == 2
    assert Bucket.query.count() == 1
    assert len(record.files) == 3

    # Delete all files soft
    record.files.clear()
    record.commit()
    db.session.commit()

    assert models.RecordFile.query.count() == 0
    assert FileInstance.query.count() == 2
    assert ObjectVersion.query.count() == 4
    assert Bucket.query.count() == 1
    assert len(record.files) == 0
    assert "f1.pdf" not in record.files
    assert "f2.pdf" not in record.files
    assert "f3.pdf" not in record.files
    assert record["files"]["entries"] == {}
    assert record["files"]["meta"] == {}


def test_record_files_store(testapp, db):
    """Test JSON stored for files."""
    record = Record.create({})

    record.files["f1.pdf"] = (BytesIO(b"testfilestream"), {"description": "Test file"})
    record.files["f2.pdf"] = BytesIO(b"testfilestream")
    record.files["f3.pdf"] = {"description": "Test my self again"}

    rf1 = record.files["f1.pdf"]
    rf2 = record.files["f2.pdf"]
    record.commit()
    assert record["files"]["meta"] == {
        "f1.pdf": {"description": "Test file"},
        "f2.pdf": None,
        "f3.pdf": {"description": "Test my self again"},
    }
    assert record["files"]["entries"] == {
        rf.key: {
            "bucket_id": str(record.bucket_id),
            "checksum": rf.file.checksum,
            "file_id": str(rf.file.file_id),
            "key": rf.key,
            "mimetype": rf.file.mimetype,
            "size": rf.file.size,
            "storage_class": rf.file.storage_class,
            "uri": rf.file.uri,
            "version_id": str(rf.object_version_id),
        }
        for rf in (rf1, rf2)
    }
