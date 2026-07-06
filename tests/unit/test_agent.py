# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from unittest.mock import MagicMock
import pytest
from app.agent import (
    save_user_profile,
    get_user_profile,
    search_simulated_kb,
    log_quiz_result,
    root_agent
)
from google.adk.tools import ToolContext


@pytest.fixture
def mock_tool_context():
    ctx = MagicMock(spec=ToolContext)
    ctx.state = {}
    return ctx


def test_save_user_profile(mock_tool_context):
    result = save_user_profile(
        goals=["Learn Python", "Learn ADK"],
        daily_schedule_time="10:00 AM",
        tool_context=mock_tool_context
    )
    assert result["status"] == "success"
    assert mock_tool_context.state["goals"] == ["Learn Python", "Learn ADK"]
    assert mock_tool_context.state["daily_schedule_time"] == "10:00 AM"


def test_get_user_profile(mock_tool_context):
    mock_tool_context.state["goals"] = ["Learn Python"]
    mock_tool_context.state["daily_schedule_time"] = "09:00 AM"
    mock_tool_context.state["quiz_history"] = [{"topic": "Python", "score": 3, "total": 3}]
    
    result = get_user_profile(tool_context=mock_tool_context)
    assert result["goals"] == ["Learn Python"]
    assert result["daily_schedule_time"] == "09:00 AM"
    assert len(result["quiz_history"]) == 1
    assert result["quiz_history"][0]["topic"] == "Python"


def test_search_simulated_kb():
    result_found = search_simulated_kb(topic="Quantum Computing")
    assert result_found["status"] == "found"
    assert "qubit" in result_found["content"]

    result_not_found = search_simulated_kb(topic="Advanced Gardening")
    assert result_not_found["status"] == "not_found"


def test_log_quiz_result(mock_tool_context):
    result = log_quiz_result(
        score=2,
        total=3,
        topic="Machine Learning",
        tool_context=mock_tool_context
    )
    assert result["status"] == "success"
    assert len(mock_tool_context.state["quiz_history"]) == 1
    assert mock_tool_context.state["quiz_history"][0]["topic"] == "Machine Learning"
    assert mock_tool_context.state["quiz_history"][0]["score"] == 2


def test_agent_configuration():
    assert root_agent.name == "root_agent"
    assert len(root_agent.tools) == 4
