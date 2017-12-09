import pytest

from playlog.lib.json import Encoder


def test_encoder():
    encoder = Encoder()
    with pytest.raises(TypeError):
        encoder.default(object())
