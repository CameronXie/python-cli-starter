"""Output Formatter."""

import json
from typing import Any

from .options import OutputFormat


def format_list(data: list[Any], output_format: OutputFormat) -> str:
    """Format the given data into the specified output format."""
    if output_format == OutputFormat.JSON:
        return json.dumps(data)
    elif output_format == OutputFormat.CSV:
        return ",".join(data)
    else:
        raise ValueError("Invalid output format")
