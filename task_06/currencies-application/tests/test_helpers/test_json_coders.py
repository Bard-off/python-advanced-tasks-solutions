import pytest

from helpers.json_coders import json_encode_default


def test_json_encode_default_raises_for_unknown():
    with pytest.raises(TypeError, match="not serializable"):
        json_encode_default(object())
