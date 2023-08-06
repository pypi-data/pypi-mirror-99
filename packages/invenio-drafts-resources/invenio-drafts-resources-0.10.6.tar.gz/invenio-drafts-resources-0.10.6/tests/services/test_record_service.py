# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-Records-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Service tests.

Test to add:
- Read a tombstone page
- Read with missing permissions
- Read with missing pid
"""

import pytest
from invenio_pidstore.errors import PIDDoesNotExistError, PIDUnregistered
from invenio_pidstore.models import PIDStatus
from marshmallow.exceptions import ValidationError
from sqlalchemy.orm.exc import NoResultFound

#
# Operations tests
#


def test_create_draft(app, service, identity_simple, input_data):
    """Test draft creation of a non-existing record."""
    draft = service.create(identity_simple, input_data)
    draft_dict = draft.to_dict()

    assert draft.id

    for key, value in input_data.items():
        assert draft[key] == value

    # Check for pid and parent pid
    assert draft['id']
    assert draft['parent']['id']
    assert draft['is_published'] is False
    assert draft['versions']['is_latest_draft'] is True
    assert draft['versions']['is_latest'] is False
    assert 'errors' not in draft_dict


def test_create_empty_draft(app, service, identity_simple):
    """Test an empty draft can be created.

    Errors (missing required fields) are reported, but don't prevent creation.
    """
    input_data = {
        "metadata": {}
    }

    draft = service.create(identity_simple, input_data)
    draft_dict = draft.to_dict()

    assert draft['id']
    assert draft['is_published'] is False
    assert draft_dict['errors'][0]['field'] == 'metadata.title'


def test_read_draft(app, service, identity_simple, input_data):
    draft = service.create(identity_simple, input_data)
    assert draft.id

    draft_2 = service.read_draft(draft.id, identity_simple)
    assert draft.id == draft_2.id


def test_update_draft(app, service, identity_simple, input_data):
    draft = service.create(identity_simple, input_data)
    assert draft.id

    orig_title = input_data['metadata']['title']
    edited_title = "Edited title"
    input_data['metadata']['title'] = edited_title

    # Update draft content
    update_draft = service.update_draft(draft.id, identity_simple, input_data)
    assert update_draft["metadata"]['title'] == edited_title
    assert draft.id == update_draft.id

    # Check the updates where saved
    update_draft = service.read_draft(draft.id, identity_simple)
    assert draft.id == update_draft.id
    assert update_draft["metadata"]['title'] == edited_title


def test_update_draft_invalid_field(app, service, identity_simple, input_data):
    """Update with invalid field reports rather than raises errors."""
    draft = service.create(identity_simple, input_data)
    orig_title = input_data['metadata']['title']
    edited_title = 100
    input_data['metadata']['title'] = edited_title

    updated_draft = service.update_draft(draft.id, identity_simple, input_data)
    updated_draft_dict = updated_draft.to_dict()

    assert draft.id == updated_draft.id
    assert 'title' not in updated_draft["metadata"]
    assert updated_draft_dict['errors'][0]['field'] == 'metadata.title'


def test_delete_draft(app, service, identity_simple, input_data):
    draft = service.create(identity_simple, input_data)
    assert draft.id

    success = service.delete_draft(draft.id, identity_simple)
    assert success

    # Check draft deletion
    with pytest.raises(PIDDoesNotExistError):
        # NOTE: Draft and Record have the same `id`
        delete_draft = service.read_draft(draft.id, identity_simple)


def _create_and_publish(service, input_data, identity_simple):
    """Creates a draft and publishes it."""
    # Cannot create with record service due to the lack of versioning
    draft = service.create(identity_simple, input_data)

    record = service.publish(draft.id, identity_simple)

    assert record.id == draft.id
    assert record._record.revision_id == 1

    return record


def test_publish_draft(app, service, identity_simple, input_data):
    """Test draft publishing of a non-existing record.

    Note that the publish action requires a draft to be created first.
    """
    # Needs `app` context because of invenio_access/permissions.py#166
    record = _create_and_publish(service, input_data, identity_simple)
    assert record._record.pid.status == PIDStatus.REGISTERED
    assert record._record.parent.pid.status == PIDStatus.REGISTERED

    for key, value in input_data.items():
        assert record[key] == value

    # Check draft deletion
    with pytest.raises(NoResultFound):
        # NOTE: Draft and Record have the same `id`
        draft = service.read_draft(record.id, identity_simple)

    # Test record exists
    record = service.read(record.id, identity_simple)

    assert record.id
    assert record._record.pid.status == PIDStatus.REGISTERED
    assert record._record.parent.pid.status == PIDStatus.REGISTERED

    for key, value in input_data.items():
        assert record[key] == value


def test_fail_to_publish_invalid_draft(app, service, identity_simple):
    """Publishing an incomplete draft should fail.

    Note that the publish action requires a draft to be created first.
    """
    # Needs `app` context because of invenio_access/permissions.py#166
    input_data = {
        "metadata": {}
    }
    draft = service.create(identity_simple, input_data)

    with pytest.raises(ValidationError) as e:
        record = service.publish(draft.id, identity_simple)

    exception = e.value
    assert "metadata" not in exception.valid_data

    # Draft still there
    draft = service.read_draft(draft.id, identity_simple)
    assert draft
    assert draft._record.pid.status == PIDStatus.NEW
    assert draft._record.parent.pid.status == PIDStatus.NEW

    # Test no published record exists
    with pytest.raises(PIDUnregistered) as e:
        record = service.read(draft.id, identity_simple)


#
# Flow tests (Note that operations are tested above
# therefore these tests do not assert their output)
#

def test_create_publish_new_revision(app, service, identity_simple,
                                     input_data):
    """Test creating a new revision of a record.

    This tests the `edit` service method.
    """
    # Needs `app` context because of invenio_access/permissions.py#166
    record = _create_and_publish(service, input_data, identity_simple)
    recid = record.id

    # Create new draft of said record
    draft = service.edit(recid, identity_simple)
    assert draft.id == recid
    assert draft._record.fork_version_id == record._record.revision_id
    # create, soft-delete, undelete, update
    assert draft._record.revision_id == 5

    # Update the content
    orig_title = input_data['metadata']['title']
    edited_title = "Edited title"
    input_data['metadata']['title'] = edited_title

    update_draft = service.update_draft(draft.id, identity_simple, input_data)

    # Check the actual record was not modified
    record = service.read(recid, identity_simple)
    assert record["metadata"]['title'] == orig_title

    # Publish it to check the increment in version_id
    record = service.publish(recid, identity_simple)

    assert record.id == recid
    assert record._record.revision_id == 2
    assert record["metadata"]['title'] == edited_title

    # Check it was actually edited
    record = service.read(recid, identity_simple)
    assert record["metadata"]['title'] == edited_title


def test_mutiple_edit(app, service, identity_simple, input_data):
    """Test the revision_id when editing record multiple times..

    This tests the `edit` service method.
    """
    # Needs `app` context because of invenio_access/permissions.py#166
    record = _create_and_publish(service, input_data, identity_simple)
    recid = record.id

    # Create new draft of said record
    draft = service.edit(recid, identity_simple)
    assert draft.id == recid
    assert draft._record.fork_version_id == record._record.revision_id
    assert draft._record.revision_id == 5

    draft = service.edit(recid, identity_simple)
    assert draft.id == recid
    assert draft._record.fork_version_id == record._record.revision_id
    assert draft._record.revision_id == 5

    # Publish it to check the increment in version_id
    record = service.publish(recid, identity_simple)

    draft = service.edit(recid, identity_simple)
    assert draft.id == recid
    assert draft._record.fork_version_id == record._record.revision_id
    assert draft._record.revision_id == 8  # soft-delete, undelete, update


def test_create_publish_new_version(app, service, identity_simple,
                                    input_data):
    """Test creating a new version of a record.

    This tests the `new_version` service method.
    """
    record = _create_and_publish(service, input_data, identity_simple)
    recid = record.id

    # Create new version
    draft = service.new_version(recid, identity_simple)

    assert draft._record.revision_id == 2
    assert draft['id'] != record['id']
    assert draft._record.pid.status == PIDStatus.NEW
    assert draft._record.parent.pid.status == PIDStatus.REGISTERED

    # Publish it
    record_2 = service.publish(draft.id, identity_simple)

    assert record_2.id
    assert record_2._record.pid.status == PIDStatus.REGISTERED
    assert record_2._record.parent.pid.status == PIDStatus.REGISTERED
    assert record_2._record.revision_id == 1
    assert record_2['id'] != record['id']


def test_read_latest_version(app, service, identity_simple,
                             input_data):
    """Test read the latest version of a record.

    This tests the `read_latest` service method.
    """
    record = _create_and_publish(service, input_data, identity_simple)
    recid = record.id

    # Create new version
    draft = service.new_version(recid, identity_simple)
    # Publish it
    record_2 = service.publish(draft.id, identity_simple)
    recid_2 = record_2.id

    latest = service.read_latest(recid, identity_simple)
    assert latest['id'] == recid_2

    latest = service.read_latest(recid_2, identity_simple)
    assert latest['id'] == recid_2
