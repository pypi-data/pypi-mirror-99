# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Override of RecordResources."""

from .config import RecordResourceConfig, RecordVersionsResourceConfig
from .resource import RecordResource, RecordVersionsResource
from .schemas_links import RecordLinksSchema

__all__ = (
    "RecordLinksSchema",
    "RecordResource",
    "RecordResourceConfig",
    "RecordVersionsResource",
    "RecordVersionsResourceConfig",
)
