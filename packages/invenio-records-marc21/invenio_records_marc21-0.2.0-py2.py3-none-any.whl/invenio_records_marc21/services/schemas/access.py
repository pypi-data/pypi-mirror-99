# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Marc21 record schemas."""

import arrow
from flask_babelex import lazy_gettext as _
from marshmallow import (
    Schema,
    ValidationError,
    fields,
    validate,
    validates,
    validates_schema,
)
from marshmallow_utils.fields import ISODateString, SanitizedUnicode

from .utils import validate_entry


class AccessConditionSchema(Schema):
    """Access condition schema.

    Conditions under which access to files are granted.
    """

    condition = fields.String()
    default_link_validity = fields.Integer()


class Agent(Schema):
    """An agent schema."""

    user = fields.Integer(required=True)


class AccessSchema(Schema):
    """Access schema."""

    metadata = fields.Bool(required=True)
    owned_by = fields.List(fields.Nested(Agent))
    access_right = SanitizedUnicode(required=True)
    embargo_date = ISODateString()
    access_condition = fields.Nested(AccessConditionSchema)

    @validates("embargo_date")
    def validate_embargo_date(self, value):
        """Validate that embargo date is in the future."""
        if arrow.get(value).date() <= arrow.utcnow().date():
            raise ValidationError(
                _("Embargo date must be in the future."), field_names=["embargo_date"]
            )

    @validates_schema
    def validate_access_right(self, data, **kwargs):
        """Validate that access right is one of the allowed ones."""
        validate_entry("access_right", data)
