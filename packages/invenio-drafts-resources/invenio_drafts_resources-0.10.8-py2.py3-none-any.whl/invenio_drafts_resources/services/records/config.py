# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""RecordDraft Service API config."""

from invenio_records_resources.services import RecordServiceConfig

from .components import DraftMetadataComponent, PIDComponent
from .permissions import RecordDraftPermissionPolicy
from .schema import ParentSchema, RecordSchema
from .search_params import AllVersionsParam


class RecordDraftServiceConfig(RecordServiceConfig):
    """Draft Service configuration."""

    # Service configuration
    permission_policy_cls = RecordDraftPermissionPolicy

    # WHY: We want to force user input choice here.
    draft_cls = None

    schema = RecordSchema

    schema_parent = ParentSchema

    components = [
        DraftMetadataComponent,
        PIDComponent,
    ]

    search_params_interpreters_cls = [
        AllVersionsParam
    ] + RecordServiceConfig.search_params_interpreters_cls
