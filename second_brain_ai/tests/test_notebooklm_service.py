import pytest
import asyncio

from services.notebooklm_service import NotebookLMService


@pytest.mark.asyncio
async def test_generate_summary_success():

    service = NotebookLMService()

    response = await service.generate_summary("This is a test document.")

    assert response["status"] == "success"
    assert "summary" in response["data"]
    assert "timestamp" in response


@pytest.mark.asyncio
async def test_extract_insights_success():

    service = NotebookLMService()

    response = await service.extract_insights("Research paper content")

    assert response["status"] == "success"
    assert "insights" in response["data"]
    assert isinstance(response["data"]["insights"], list)