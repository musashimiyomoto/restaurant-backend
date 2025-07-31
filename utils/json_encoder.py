import json
from decimal import Decimal
from enum import Enum
from typing import Any


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o: Any):
        if isinstance(o, Enum):
            return o.value
        if isinstance(o, Decimal):
            return float(o)
        return super().default(o)
