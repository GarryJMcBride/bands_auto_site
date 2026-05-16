# import pytest
# from unittest.mock import AsyncMock, patch

# @pytest.mark.asyncio
# async def test_update_database_saves_submission():
#     mock_payload = QuoteSubmission(
#         name="John Doe",
#         email="john@example.com",
#         message="Test quote request"
#     )
#     mock_submission_id = 42

#     with patch("yourmodule.save_submission", new_callable=AsyncMock) as mock_save:
#         mock_save.return_value = mock_submission_id

#         await update_database(mock_payload)

#         mock_save.assert_called_once_with(mock_payload)


# @pytest.mark.asyncio
# async def test_update_database_logs_on_failure(caplog):
#     mock_payload = QuoteSubmission(
#         name="John Doe",
#         email="john@example.com",
#         message="Test quote request"
#     )

#     with patch("yourmodule.save_submission", new_callable=AsyncMock) as mock_save:
#         mock_save.side_effect = asyncpg.PostgresError("Connection refused")

#         # Should not raise — exception propagates to FastAPI's handler
#         with pytest.raises(asyncpg.PostgresError):
#             await update_database(mock_payload)