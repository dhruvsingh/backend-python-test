# -*- coding: utf-8 -*-
"""utils for app."""


def clean_field(value):
    """Clean field to return str value or None."""
    if value.strip():
        return value

    return None
