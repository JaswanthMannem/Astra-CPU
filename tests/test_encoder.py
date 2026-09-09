import pytest
from astra.logic.encoder import encoder

def test_encoder():
    assert encoder(1, 0, 0, 0) == (0, 0)
    assert encoder(0, 1, 0, 0) == (0, 1)
    assert encoder(0, 0, 1, 0) == (1, 0)
    assert encoder(0, 0, 0, 1) == (1, 1)

def test_encoder_invalid_input():
    with pytest.raises(ValueError):
        encoder(1, 1, 0, 0)
    with pytest.raises(ValueError):
        encoder(0, 1, 1, 0)
    with pytest.raises(ValueError):
        encoder(0, 0, 1, 1)
    with pytest.raises(ValueError):
        encoder(1, 1, 1, 1)