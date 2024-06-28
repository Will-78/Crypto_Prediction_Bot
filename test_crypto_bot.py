import pytest
from unittest.mock import patch, AsyncMock
import asyncio

# Assuming the function is defined in a module named crypto_bot
from crypto_bot import retrieve_predictions

@pytest.mark.asyncio
@patch('builtins.input', return_value='BTC')
@patch('crypto_bot.fetch_currency', new_callable=AsyncMock)
@patch('crypto_bot.fetch_prediction', new_callable=AsyncMock)
async def test_no_crypto_id(mock_fetch_prediction, mock_fetch_currency, mock_input, capsys):
    # Setup mock for fetch_currency 
    mock_fetch_currency.return_value = None

    await retrieve_predictions()

    captured = capsys.readouterr()
    assert "There are no records of this crypto item in the database" in captured.out

@pytest.mark.asyncio
@patch('builtins.input', return_value='BTC')
@patch('crypto_bot.fetch_currency', new_callable=AsyncMock)
@patch('crypto_bot.fetch_prediction', new_callable=AsyncMock)
async def test_no_predictions(mock_fetch_prediction, mock_fetch_currency, mock_input, capsys):
    # mock values for making this prediction
    mock_fetch_currency.return_value = 'mocked_crypto_id'
    mock_fetch_prediction.return_value = ([], [])

    await retrieve_predictions()

    captured = capsys.readouterr()
    assert "Error fetching prior predictions for BTCUSDT" in captured.out
