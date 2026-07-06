# ruff: noqa
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

import datetime
from zoneinfo import ZoneInfo
import os
import google.auth

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.adk.tools import ToolContext
from google.genai import types

try:
    _, project_id = google.auth.default()
except Exception:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "mock-project-id")

os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"


def save_user_profile(
    goals: list[str],
    daily_schedule_time: str,
    tool_context: ToolContext
) -> dict:
    """Saves the user's learning goals and preferred daily delivery time.

    Args:
        goals: A list of strings representing the user's learning goals.
        daily_schedule_time: A string representing the preferred delivery time (e.g. '09:00 AM').

    Returns:
        A dictionary with a success status and confirmation message.
    """
    tool_context.state["goals"] = goals
    tool_context.state["daily_schedule_time"] = daily_schedule_time
    return {
        "status": "success",
        "message": f"Goals successfully updated to: {goals}. Daily delivery scheduled at: {daily_schedule_time}."
    }


def get_user_profile(tool_context: ToolContext) -> dict:
    """Retrieves the user's saved goals, schedule, and quiz history.

    Returns:
        A dictionary containing goals, daily delivery time, and quiz history.
    """
    goals = tool_context.state.get("goals", [])
    daily_schedule_time = tool_context.state.get("daily_schedule_time", "Not scheduled")
    quiz_history = tool_context.state.get("quiz_history", [])
    return {
        "goals": goals,
        "daily_schedule_time": daily_schedule_time,
        "quiz_history": quiz_history
    }


def search_simulated_kb(topic: str) -> dict:
    """Simulates searching an offline database/knowledge base for reference materials on a topic.

    Args:
        topic: The learning topic to search for.

    Returns:
        A dictionary with search status and either content or not found message.
    """
    kb = {
        "quantum computing": "Quantum computing uses qubit superposition and entanglement to perform calculations exponentially faster than classical computers for certain problems. Key concepts: superposition, entanglement, interference.",
        "machine learning": "Machine learning is a field of AI that trains algorithms to find patterns in data and make predictions. Key concepts: supervised learning, unsupervised learning, neural networks, gradient descent.",
        "photography": "Photography basics revolve around the exposure triangle: aperture (controlling depth of field), shutter speed (controlling motion blur), and ISO (controlling light sensitivity).",
        "cooking": "Cooking fundamentals involve heat transfer, seasoning (salt, acid, fat, heat), knife safety and cuts, and understanding flavor profiles."
    }
    normalized_topic = topic.lower()
    for key, val in kb.items():
        if key in normalized_topic:
            return {"status": "found", "content": val}
    return {
        "status": "not_found",
        "message": "Topic not found in local index. Proceeding with general knowledge generation."
    }


def log_quiz_result(
    score: int,
    total: int,
    topic: str,
    tool_context: ToolContext
) -> dict:
    """Records the user's score on a topic quiz.

    Args:
        score: The number of correct answers.
        total: The total number of questions in the quiz.
        topic: The topic of the quiz.

    Returns:
        A dictionary with a success status and confirmation message.
    """
    if "quiz_history" not in tool_context.state:
        tool_context.state["quiz_history"] = []
    
    entry = {
        "topic": topic,
        "score": score,
        "total": total,
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    tool_context.state["quiz_history"].append(entry)
    return {
        "status": "success",
        "message": f"Successfully logged score of {score}/{total} for '{topic}'."
    }


root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction="""You are the Micro-Learning Concierge, a highly personalized, friendly educational assistant.
Your objectives:
1. Help users set their learning goals and preferred daily schedule. Save this information using the `save_user_profile` tool.
2. Deliver today's custom 5-minute lesson.
   - First, check if the topic matches any simulated reference material using the `search_simulated_kb` tool.
   - Curate a highly engaging, custom lesson that can be read in 5 minutes (strictly between 400 and 600 words).
   - Format the lesson clearly with Markdown headings, bullet points, and key takeaways.
3. Immediately follow the lesson with a 3-question multiple-choice quiz (labeled Question 1, 2, and 3).
4. Evaluate the user's quiz answers, provide clear explanations, and log their scores using the `log_quiz_result` tool.
5. Provide a summary of the user's learning goals, schedule, and quiz performance when asked, using the `get_user_profile` tool.""",
    tools=[save_user_profile, get_user_profile, search_simulated_kb, log_quiz_result],
)

app = App(
    root_agent=root_agent,
    name="app",
)
