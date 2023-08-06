# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 CERN.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Record, Draft and Parent Record API classes.

These classes belongs to the  data access layer and MUST ONLY be accessed from
within the service layer. It's wrong to use these classes in the presentation
layer.

A record and a draft share a single parent record. The parent record is used
to store properties common to all versions of a record (e.g. access control).

The draft and record share the same UUID, and thus both also share a single
persistent identifier. The parent record has its own UUID and own persistent
identifier.
"""

import uuid

from invenio_pidstore.models import PIDStatus
from invenio_pidstore.providers.recordid_v2 import RecordIdProviderV2
from invenio_records.systemfields import ModelField
from invenio_records_resources.records import Record as RecordBase
from invenio_records_resources.records.systemfields import PIDField, \
    PIDStatusCheckField
from sqlalchemy.orm.exc import NoResultFound

from .systemfields import ParentField, VersionsField


#
# Persistent identifier providers
#
class DraftRecordIdProviderV2(RecordIdProviderV2):
    """Draft PID provider."""

    default_status_with_obj = PIDStatus.NEW


#
# Record API classes
#
class ParentRecord(RecordBase):
    """Parent record API."""

    # Configuration
    model_cls = None

    pid = PIDField('id', provider=DraftRecordIdProviderV2, delete=True)


class Record(RecordBase):
    """Record API."""

    #
    # Configuration to be set by a subclass
    #

    #: The record's SQLAlchemy model class. Must be set by the subclass.
    model_cls = None
    #: The parent state's SQLAlchemy model class. Must be set by the subclass.
    versions_model_cls = None
    #: The parent record's API class. Must be set by the subclass.
    parent_record_cls = None

    #
    # System fields
    #
    #: The internal persistent identifier. Records and drafts share UUID.
    pid = PIDField('id', provider=DraftRecordIdProviderV2, delete=True)

    #: System field to check if a record has been published.
    is_published = PIDStatusCheckField(status=PIDStatus.REGISTERED)

    #: The parent record - the draft is responsible for creating the parent.
    parent = ParentField(
        ParentRecord, create=False, soft_delete=False, hard_delete=False)

    #: Version relationship
    versions = VersionsField(create=True, set_latest=True)

    @classmethod
    def get_records_by_parent(cls, parent):
        """Get all sibling records for the specified parent record."""
        versions = cls.model_cls.query.filter_by(parent_id=parent.id).all()
        return [
            cls(rec_model.data, model=rec_model)
            for rec_model in versions
        ]

    @classmethod
    def publish(cls, draft):
        """Publish a draft as a new record.

        If a record already exists, we simply get the record. If a draft has
        not yet been published, we create the record.

        The caller is responsible for registering the internal persistent
        identifiers (see ``register()``).
        """
        if draft.is_published:
            record = cls.get_record(draft.id)
        else:
            record = cls.create(
                {},
                # A draft and record share UUID, so we reuse the draft's id/pid
                id_=draft.id,
                pid=draft.pid,
                # Link the record with the parent record and set the versioning
                # relationship.
                parent=draft.parent,
                versions=draft.versions,
            )
            # Merge the PIDs into the current db session if not already in the
            # session.
            cls.pid.session_merge(record)
            cls.parent_record_cls.pid.session_merge(record.parent)
        return record

    def register(self):
        """Register the internal persistent identifiers."""
        if not self.parent.pid.is_registered():
            self.parent.pid.register()
            self.parent.commit()
        self.pid.register()


class Draft(Record):
    """Draft base API for metadata creation and manipulation."""

    #
    # Configuration to be set by a subclass
    #

    #: The record's SQLAlchemy model class. Must be set by the subclass.
    model_cls = None
    #: The parent state's SQLAlchemy model class. Must be set by the subclass.
    versions_model_cls = None
    #: The parent record's API class. Must be set by the subclass.
    parent_record_cls = None

    #
    # System fields
    #

    #: The internal persistent identifier. Records and drafts share UUID.
    pid = PIDField('id', provider=DraftRecordIdProviderV2, delete=False)

    #: The parent record - the draft is responsible for creating the parent.
    parent = ParentField(
        ParentRecord, create=True, soft_delete=False, hard_delete=True)

    #: Version relationship
    versions = VersionsField(create=True, set_next=True)

    #: The expiry date of the draft.
    expires_at = ModelField()

    #: Revision id of record from which this draft was created.
    fork_version_id = ModelField()

    @classmethod
    def new_version(cls, record):
        """Create a draft for a new version of a record.

        The caller is responsible for:
        1) checking if a draft for a new version already exists
        2) moving the record data into the draft data.
        """
        return cls.create(
            {},
            # We create a new id, because this is for a new version.
            id=uuid.uuid4(),
            # Links the draft with the same parent (i.e. a new version).
            parent=record.parent,
            versions=record.versions,
            # New drafts without a record (i.e. unpublished drafts) must set
            # the fork version id to None.
            fork_version_id=None,
        )

    @classmethod
    def edit(cls, record):
        """Create a draft for editing an existing version of a record."""
        try:
            # We soft-delete a draft once it has been published, in order to
            # keep the version_id counter around for optimistic concurrency
            # control (both for ES indexing and for REST API clients)
            draft = cls.get_record(record.id, with_deleted=True)
            if draft.is_deleted:
                draft.undelete()
                # Below line is needed to dump PID back into the draft.
                draft.pid = record.pid
                # Ensure record is link with the parent
                draft.parent = record.parent
                draft.versions = record.versions
                # Ensure we record the revision id we forked from
                draft.fork_version_id = record.revision_id
                # Note, other values like bucket_id values was kept in the
                # soft-deleted record, so we are not setting them again here.
        except NoResultFound:
            # If a draft was ever force deleted, then we will create the draft.
            # This is a very exceptional case as normally, when we edit a
            # record then the soft-deleted draft exists and we are in above
            # case.
            draft = cls.create(
                {},
                # A draft to edit a record must share the id and uuid.
                id_=record.id,
                pid=record.pid,
                # Link it with the same parent record
                parent=record.parent,
                versions=record.versions,
                # Record which record version we forked from.
                fork_version_id=record.revision_id,
            )
        return draft
