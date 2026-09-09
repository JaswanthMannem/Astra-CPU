import pytest
from astra.logic.decoder import decoder

def test_decoder():
    assert decoder(0, 0) == (1, 0, 0, 0)
    assert decoder(0, 1) == (0, 1, 0, 0)
    assert decoder(1, 0) == (0, 0, 1, 0)
    assert decoder(1, 1) == (0, 0, 0, 1)    

def test_decoder_invalid_input():
    with pytest.raises(ValueError):
        decoder(2, 0)
    with pytest.raises(ValueError):
        decoder(1, 2)