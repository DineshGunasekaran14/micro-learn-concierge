import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from app.agent import save_user_profile, get_user_profile, search_simulated_kb, log_quiz_result

app = FastAPI(title="Micro-Learning Concierge Demo")

# Global in-memory session state for demo purposes
session_state = {
    "goals": ["Quantum Computing"],
    "daily_schedule_time": "09:00 AM",
    "quiz_history": [
        {"topic": "Quantum Computing Basics", "score": 3, "total": 3, "date": "2026-07-06 12:00:00"}
    ]
}


class MockToolContext:
    def __init__(self, state):
        self.state = state


class GoalsRequest(BaseModel):
    goals: list[str]
    time: str


class QuizSubmitRequest(BaseModel):
    topic: str
    score: int
    total: int


@app.get("/api/profile")
def api_get_profile():
    ctx = MockToolContext(session_state)
    return get_user_profile(ctx)


@app.post("/api/profile")
def api_save_profile(req: GoalsRequest):
    ctx = MockToolContext(session_state)
    return save_user_profile(req.goals, req.time, ctx)


@app.post("/api/quiz")
def api_submit_quiz(req: QuizSubmitRequest):
    ctx = MockToolContext(session_state)
    return log_quiz_result(req.score, req.total, req.topic, ctx)


@app.get("/api/lesson/{topic}")
def api_get_lesson(topic: str):
    # Retrieve simulated resource content
    kb_result = search_simulated_kb(topic)
    
    # Custom interactive lessons and quizzes based on topic
    if "quantum" in topic.lower():
        title = "Quantum Computing: Introduction to Qubits"
        content = """
        <p>In classical computing, the basic unit of information is the <strong>bit</strong>, which represents either a <code>0</code> or a <code>1</code>. In quantum computing, the fundamental unit is the <strong>qubit</strong> (quantum bit).</p>
        
        <h3>1. Superposition</h3>
        <p>Unlike classical bits, qubits can exist in a state of <strong>superposition</strong>. This means a qubit can represent a <code>0</code>, a <code>1</code>, or any quantum proportion of both simultaneously. Imagine a spinning coin—while it is spinning, it is not just heads or tails, but a blur of both states at once.</p>
        
        <h3>2. Entanglement</h3>
        <p><strong>Entanglement</strong> is a link between qubits where the state of one qubit instantaneously determines the state of another, regardless of the physical distance between them. Einstein famously referred to this connection as <em>"spooky action at a distance."</em></p>
        
        <h3>3. Quantum Interference</h3>
        <p>Quantum algorithms use <strong>interference</strong> to amplify path combinations that lead to the correct answer, while causing incorrect paths to cancel each other out. This permits solving complex problems in minutes that would take classical supercomputers millennia.</p>
        """
        quiz = [
            {
                "question": "What property allows a qubit to represent 0 and 1 simultaneously?",
                "options": ["A) Entanglement", "B) Superposition", "C) Decoherence"],
                "correct": 1,
                "explanation": "Superposition is the quantum property that allows qubits to exist in multiple states at once."
            },
            {
                "question": "What phrase did Einstein use to describe quantum entanglement?",
                "options": ["A) Spooky action at a distance", "B) Quantum anomaly", "C) Relativistic entanglement"],
                "correct": 0,
                "explanation": "Einstein called entanglement 'spooky action at a distance' because of its non-local correlation properties."
            },
            {
                "question": "Which mechanism amplifies correct results and cancels out wrong paths?",
                "options": ["A) Quantum Tunneling", "B) Thermalization", "C) Quantum Interference"],
                "correct": 2,
                "explanation": "Quantum interference is used to bias the measurement probability toward the correct solution."
            }
        ]
    elif "machine" in topic.lower() or "ml" in topic.lower():
        title = "Machine Learning: Core Paradigms"
        content = """
        <p><strong>Machine Learning (ML)</strong> is the field of computer science that gives computers the ability to learn without being explicitly programmed. It operates by building models from input data to make predictions.</p>
        
        <h3>1. Supervised Learning</h3>
        <p>In <strong>supervised learning</strong>, the model is trained on labeled data—meaning each training example is paired with its correct output. Examples include predicting house prices based on size, or classifying emails as spam or not spam.</p>
        
        <h3>2. Unsupervised Learning</h3>
        <p>In <strong>unsupervised learning</strong>, the system looks for hidden structures in unlabeled data. The algorithm groups data points together based on similarities without human assistance. This is called <strong>clustering</strong>.</p>
        
        <h3>3. Reinforcement Learning</h3>
        <p><strong>Reinforcement learning</strong> involves an agent that learns to make decisions by performing actions in an environment to maximize some notion of cumulative reward. The agent receives feedback in the form of rewards or penalties.</p>
        """
        quiz = [
            {
                "question": "What type of learning uses labeled input-output pairs?",
                "options": ["A) Unsupervised Learning", "B) Labeled Clustering", "C) Supervised Learning"],
                "correct": 2,
                "explanation": "Supervised learning relies on explicit labels to train model weights."
            },
            {
                "question": "Grouping customer segments based on buying patterns without labels is an example of:",
                "options": ["A) Clustering (Unsupervised)", "B) Regression (Supervised)", "C) Reward Maximization"],
                "correct": 0,
                "explanation": "Clustering is the primary method of grouping unlabeled datasets in unsupervised learning."
            },
            {
                "question": "What paradigm teaches an agent using a system of rewards and penalties?",
                "options": ["A) Gradient Descent", "B) Reinforcement Learning", "C) Dimensionality Reduction"],
                "correct": 1,
                "explanation": "Reinforcement learning optimizes behaviors by interacting with an environment to maximize cumulative rewards."
            }
        ]
    elif "photography" in topic.lower():
        title = "Photography: The Exposure Triangle"
        content = """
        <p>Creating a properly exposed photograph requires balancing three distinct camera variables known as the <strong>Exposure Triangle</strong>: Aperture, Shutter Speed, and ISO.</p>
        
        <h3>1. Aperture</h3>
        <p><strong>Aperture</strong> is the physical opening in the lens that lets light reach the sensor. It is measured in f-stops (e.g., f/2.8, f/16). A wide aperture (low f-number) creates a shallow depth of field, blurring the background (the 'bokeh' effect).</p>
        
        <h3>2. Shutter Speed</h3>
        <p><strong>Shutter Speed</strong> is the duration of time the camera shutter remains open. Fast shutter speeds (e.g., 1/1000s) freeze motion, while slow speeds (e.g., 1/2s) introduce motion blur, often used for silky waterfall effects.</p>
        
        <h3>3. ISO</h3>
        <p><strong>ISO</strong> measures the sensor's sensitivity to light. A lower ISO (e.g., 100) produces clean, sharp images. Raising the ISO (e.g., 6400) amplifies light sensitivity for dark environments but introduces digital noise (grain).</p>
        """
        quiz = [
            {
                "question": "Which f-stop opening will yield the shallowest depth of field (blurry background)?",
                "options": ["A) f/1.8", "B) f/8", "C) f/22"],
                "correct": 0,
                "explanation": "A lower f-number corresponds to a wider lens opening, producing a shallower depth of field."
            },
            {
                "question": "What is the primary visual byproduct of using a very high ISO value?",
                "options": ["A) Lens flare", "B) Digital noise (grain)", "C) Motion blur"],
                "correct": 1,
                "explanation": "High ISO amplifies the sensor signal, which introduces grain or digital noise."
            },
            {
                "question": "To freeze a fast-moving bird in mid-flight, you should prioritize:",
                "options": ["A) A slow shutter speed", "B) A high f-stop number", "C) A fast shutter speed"],
                "correct": 2,
                "explanation": "Fast shutter speeds (like 1/1000s or faster) freeze rapid action without blur."
            }
        ]
    else:
        title = f"Daily Lesson: {topic.title()}"
        content = f"""
        <p>Welcome to your customized lesson on <strong>{topic}</strong>. Based on your learning goal, here is a quick 5-minute reference outline:</p>
        <ul>
            <li><strong>Core Concept:</strong> Understanding the fundamental primitives and structure of {topic}.</li>
            <li><strong>Key Applications:</strong> Real-world scenarios, challenges, and implementation paradigms.</li>
            <li><strong>Next Steps:</strong> Further reading, practice exercises, and testing comprehension.</li>
        </ul>
        <p><em>Note: This lesson was dynamically formulated based on general knowledge outlines for the topic '{topic}'.</em></p>
        """
        quiz = [
            {
                "question": f"What is the primary focus of studying {topic}?",
                "options": ["A) Practical application", "B) Memorizing syntax", "C) Theoretical analysis"],
                "correct": 0,
                "explanation": "Active, practical application is the most effective way to retain new concepts."
            },
            {
                "question": "What is the recommended daily study length for maximum retention?",
                "options": ["A) 5 minutes", "B) 4 hours", "C) 8 hours"],
                "correct": 0,
                "explanation": "Bite-sized, daily 5-minute study sessions optimize recall and prevent cognitive fatigue."
            },
            {
                "question": "How should you verify you have mastered a topic?",
                "options": ["A) Reading the text twice", "B) Taking interactive quizzes", "C) Watching a video"],
                "correct": 1,
                "explanation": "Interactive testing active-recalls concepts, validating real understanding."
            }
        ]
        
    return {
        "title": title,
        "content": content,
        "kb_summary": kb_result.get("content", "General outline used."),
        "quiz": quiz
    }


@app.get("/", response_class=HTMLResponse)
def get_dashboard():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Micro-Learning Concierge Dashboard</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;600;800&display=swap" rel="stylesheet">
        <style>
            :root {
                --bg-dark: #0f111a;
                --card-bg: rgba(22, 28, 45, 0.7);
                --card-border: rgba(255, 255, 255, 0.08);
                --accent-primary: #7c4dff;
                --accent-secondary: #00e5ff;
                --text-main: #f3f4f6;
                --text-muted: #9ca3af;
                --text-link: #818cf8;
                --success: #10b981;
                --error: #ef4444;
            }

            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }

            body {
                background-color: var(--bg-dark);
                background-image: 
                    radial-gradient(at 10% 20%, rgba(124, 77, 255, 0.15) 0px, transparent 50%),
                    radial-gradient(at 90% 80%, rgba(0, 229, 255, 0.1) 0px, transparent 50%);
                background-attachment: fixed;
                color: var(--text-main);
                font-family: 'Inter', sans-serif;
                min-height: 100vh;
                padding: 2rem;
            }

            header {
                max-width: 1200px;
                margin: 0 auto 2rem auto;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 1px solid var(--card-border);
                padding-bottom: 1.5rem;
            }

            h1 {
                font-family: 'Outfit', sans-serif;
                font-size: 2.2rem;
                font-weight: 800;
                background: linear-gradient(135deg, #ffffff 30%, var(--accent-secondary) 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }

            .badge {
                background: rgba(124, 77, 255, 0.2);
                border: 1px solid var(--accent-primary);
                color: var(--accent-secondary);
                padding: 0.4rem 0.8rem;
                border-radius: 20px;
                font-size: 0.8rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }

            .container {
                max-width: 1200px;
                margin: 0 auto;
                display: grid;
                grid-template-columns: 350px 1fr;
                gap: 2rem;
            }

            .card {
                background: var(--card-bg);
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                border: 1px solid var(--card-border);
                border-radius: 16px;
                padding: 1.5rem;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
                transition: transform 0.3s ease, border-color 0.3s ease;
            }

            .card:hover {
                border-color: rgba(124, 77, 255, 0.3);
            }

            h2 {
                font-family: 'Outfit', sans-serif;
                font-size: 1.4rem;
                margin-bottom: 1rem;
                color: #ffffff;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }

            .sidebar {
                display: flex;
                flex-direction: column;
                gap: 1.5rem;
            }

            label {
                display: block;
                font-size: 0.85rem;
                color: var(--text-muted);
                margin-bottom: 0.4rem;
                font-weight: 500;
            }

            input[type="text"], select {
                width: 100%;
                background: rgba(15, 17, 26, 0.6);
                border: 1px solid var(--card-border);
                border-radius: 8px;
                padding: 0.75rem;
                color: #ffffff;
                font-family: inherit;
                font-size: 0.95rem;
                margin-bottom: 1rem;
                outline: none;
                transition: border-color 0.2s ease;
            }

            input[type="text"]:focus, select:focus {
                border-color: var(--accent-primary);
            }

            button {
                width: 100%;
                background: linear-gradient(135deg, var(--accent-primary) 0%, #6200ea 100%);
                border: none;
                border-radius: 8px;
                padding: 0.8rem;
                color: #ffffff;
                font-weight: 600;
                font-family: inherit;
                font-size: 0.95rem;
                cursor: pointer;
                transition: opacity 0.2s ease, transform 0.1s ease;
            }

            button:hover {
                opacity: 0.9;
            }

            button:active {
                transform: scale(0.98);
            }

            .profile-stat {
                display: flex;
                justify-content: space-between;
                padding: 0.6rem 0;
                border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            }

            .profile-stat:last-child {
                border-bottom: none;
            }

            .profile-stat span:first-child {
                color: var(--text-muted);
            }

            .profile-stat span:last-child {
                font-weight: 600;
            }

            .lesson-content h3 {
                font-family: 'Outfit', sans-serif;
                margin-top: 1.5rem;
                margin-bottom: 0.5rem;
                color: var(--accent-secondary);
            }

            .lesson-content p {
                line-height: 1.6;
                color: var(--text-main);
                margin-bottom: 1rem;
            }

            .lesson-content code {
                background: rgba(255, 255, 255, 0.1);
                padding: 0.2rem 0.4rem;
                border-radius: 4px;
                font-family: monospace;
            }

            .quiz-container {
                margin-top: 2rem;
                border-top: 1px solid var(--card-border);
                padding-top: 1.5rem;
            }

            .quiz-question {
                margin-bottom: 1.5rem;
            }

            .quiz-question p {
                font-weight: 600;
                margin-bottom: 0.8rem;
            }

            .quiz-options {
                display: flex;
                flex-direction: column;
                gap: 0.6rem;
            }

            .option-btn {
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid var(--card-border);
                border-radius: 8px;
                padding: 0.75rem 1rem;
                text-align: left;
                color: var(--text-main);
                cursor: pointer;
                transition: all 0.2s ease;
                font-weight: 400;
            }

            .option-btn:hover {
                background: rgba(124, 77, 255, 0.15);
                border-color: var(--accent-primary);
            }

            .option-btn.selected {
                background: rgba(124, 77, 255, 0.3);
                border-color: var(--accent-primary);
                font-weight: 600;
            }

            .option-btn.correct {
                background: rgba(16, 185, 129, 0.2) !important;
                border-color: var(--success) !important;
                color: #ffffff;
            }

            .option-btn.incorrect {
                background: rgba(239, 68, 68, 0.2) !important;
                border-color: var(--error) !important;
                color: #ffffff;
            }

            .explanation {
                font-size: 0.85rem;
                color: var(--text-muted);
                margin-top: 0.5rem;
                padding: 0.5rem;
                border-left: 2px solid var(--accent-primary);
                display: none;
            }

            .score-banner {
                background: rgba(16, 185, 129, 0.1);
                border: 1px solid var(--success);
                border-radius: 8px;
                padding: 1rem;
                margin-top: 1.5rem;
                text-align: center;
                display: none;
            }

            .score-banner h4 {
                color: var(--success);
                font-size: 1.2rem;
                margin-bottom: 0.3rem;
            }

            .score-banner p {
                font-size: 0.9rem;
                color: var(--text-muted);
            }

            .history-list {
                list-style: none;
                max-height: 200px;
                overflow-y: auto;
                font-size: 0.85rem;
                display: flex;
                flex-direction: column;
                gap: 0.5rem;
                margin-top: 0.5rem;
            }

            .history-item {
                background: rgba(255, 255, 255, 0.02);
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-radius: 6px;
                padding: 0.5rem;
                display: flex;
                justify-content: space-between;
            }

            .history-item span:last-child {
                color: var(--accent-secondary);
                font-weight: 600;
            }

            .welcome-panel {
                text-align: center;
                padding: 4rem 2rem;
            }

            .welcome-panel h2 {
                font-size: 2rem;
                margin-bottom: 1rem;
                justify-content: center;
            }

            .welcome-panel p {
                color: var(--text-muted);
                max-width: 500px;
                margin: 0 auto 2rem auto;
                line-height: 1.5;
            }

            .tab-btn {
                background: transparent;
                border: 1px solid var(--accent-primary);
                color: var(--accent-primary);
                border-radius: 20px;
                padding: 0.4rem 1rem;
                width: auto;
                cursor: pointer;
                font-size: 0.85rem;
                font-weight: 500;
                transition: all 0.2s ease;
            }

            .tab-btn:hover {
                background: var(--accent-primary);
                color: #ffffff;
            }
        </style>
    </head>
    <body>
        <header>
            <div>
                <h1>Micro-Learning Concierge</h1>
                <p style="font-size: 0.9rem; color: var(--text-muted); margin-top: 0.2rem;">Custom 5-minute daily lessons</p>
            </div>
            <div style="display: flex; align-items: center; gap: 1rem;">
                <span class="badge">Local Sandbox Demo</span>
            </div>
        </header>

        <div class="container">
            <div class="sidebar">
                <!-- Configure Goals -->
                <div class="card">
                    <h2>🎯 Learning Config</h2>
                    <label for="goal-input">Learning Topic</label>
                    <select id="goal-input">
                        <option value="Quantum Computing">Quantum Computing</option>
                        <option value="Machine Learning">Machine Learning</option>
                        <option value="Photography">Photography</option>
                    </select>

                    <label for="schedule-input">Daily Delivery Schedule</label>
                    <select id="schedule-input">
                        <option value="08:00 AM">08:00 AM</option>
                        <option value="09:00 AM" selected>09:00 AM</option>
                        <option value="12:00 PM">12:00 PM</option>
                        <option value="06:00 PM">06:00 PM</option>
                    </select>

                    <button id="save-profile-btn" onclick="saveProfile()">Update Profile</button>
                </div>

                <!-- User Profile & Progress -->
                <div class="card">
                    <h2>👤 User Profile</h2>
                    <div class="profile-stat">
                        <span>Active Goal:</span>
                        <span id="active-goal-stat">-</span>
                    </div>
                    <div class="profile-stat">
                        <span>Daily Time:</span>
                        <span id="schedule-stat">-</span>
                    </div>
                    
                    <h3 style="font-size: 1rem; margin-top: 1.5rem; margin-bottom: 0.5rem; color: #ffffff;">📊 Quiz Performance</h3>
                    <ul class="history-list" id="history-list">
                        <!-- History items populated dynamically -->
                    </ul>
                </div>
            </div>

            <div class="main-content">
                <!-- Lesson Panel -->
                <div class="card" id="lesson-card" style="display: none;">
                    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--card-border); padding-bottom: 1rem; margin-bottom: 1.5rem;">
                        <h2 id="lesson-title" style="margin-bottom: 0;">Lesson</h2>
                        <span class="badge" style="background: rgba(0, 229, 255, 0.1); border-color: var(--accent-secondary); color: var(--accent-secondary);">⏱️ 5 min read</span>
                    </div>
                    
                    <div class="lesson-content" id="lesson-body">
                        <!-- Lesson HTML populated dynamically -->
                    </div>

                    <!-- Interactive Quiz -->
                    <div class="quiz-container" id="quiz-container">
                        <h2>📝 Knowledge Check</h2>
                        <div id="quiz-questions">
                            <!-- Questions populated dynamically -->
                        </div>
                        <button id="submit-quiz-btn" style="margin-top: 1rem;" onclick="gradeQuiz()">Submit Quiz answers</button>
                        
                        <div class="score-banner" id="score-banner">
                            <h4 id="score-text">You scored 3/3!</h4>
                            <p>Quiz results successfully logged to your profile history.</p>
                        </div>
                    </div>
                </div>

                <!-- Welcome Screen -->
                <div class="card welcome-panel" id="welcome-card">
                    <h2>Welcome to your Concierge!</h2>
                    <p>Select your learning goal and delivery schedule on the left panel, then request your daily customized lesson to begin.</p>
                    <button class="tab-btn" onclick="loadLesson()">Request Today's Lesson</button>
                </div>
            </div>
        </div>

        <script>
            let currentLessonData = null;
            let userAnswers = {};

            async function loadProfile() {
                const res = await fetch("/api/profile");
                const profile = await res.json();
                
                // Update stats
                document.getElementById("active-goal-stat").innerText = profile.goals.join(", ") || "None";
                document.getElementById("schedule-stat").innerText = profile.daily_schedule_time;
                
                // Update select dropdowns
                if (profile.goals.length > 0) {
                    document.getElementById("goal-input").value = profile.goals[0];
                }
                document.getElementById("schedule-input").value = profile.daily_schedule_time;

                // Update history
                const historyList = document.getElementById("history-list");
                historyList.innerHTML = "";
                if (profile.quiz_history.length === 0) {
                    historyList.innerHTML = '<li style="color: var(--text-muted);">No quizzes taken yet</li>';
                } else {
                    profile.quiz_history.forEach(item => {
                        const li = document.createElement("li");
                        li.className = "history-item";
                        li.innerHTML = `<span>${item.topic}</span><span>${item.score}/${item.total}</span>`;
                        historyList.appendChild(li);
                    });
                }
            }

            async function saveProfile() {
                const goal = document.getElementById("goal-input").value;
                const time = document.getElementById("schedule-input").value;
                
                const btn = document.getElementById("save-profile-btn");
                btn.innerText = "Saving...";
                btn.disabled = true;

                await fetch("/api/profile", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ goals: [goal], time: time })
                });

                await loadProfile();
                
                btn.innerText = "Update Profile";
                btn.disabled = false;
            }

            async function loadLesson() {
                const topic = document.getElementById("goal-input").value;
                
                document.getElementById("welcome-card").style.display = "none";
                const lessonCard = document.getElementById("lesson-card");
                lessonCard.style.display = "block";
                
                document.getElementById("lesson-title").innerText = "Loading Lesson...";
                document.getElementById("lesson-body").innerHTML = "<p>Curating your custom 5-minute lesson...</p>";
                document.getElementById("quiz-container").style.display = "none";

                const res = await fetch(`/api/lesson/${encodeURIComponent(topic)}`);
                currentLessonData = await res.json();
                userAnswers = {};

                // Render Lesson
                document.getElementById("lesson-title").innerText = currentLessonData.title;
                document.getElementById("lesson-body").innerHTML = currentLessonData.content;
                
                // Render Quiz
                const quizQuestions = document.getElementById("quiz-questions");
                quizQuestions.innerHTML = "";
                currentLessonData.quiz.forEach((q, qIndex) => {
                    const qDiv = document.createElement("div");
                    qDiv.className = "quiz-question";
                    qDiv.innerHTML = `<p>${qIndex + 1}. ${q.question}</p>`;
                    
                    const optsDiv = document.createElement("div");
                    optsDiv.className = "quiz-options";
                    
                    q.options.forEach((opt, optIndex) => {
                        const optBtn = document.createElement("button");
                        optBtn.className = "option-btn";
                        optBtn.id = `q-${qIndex}-opt-${optIndex}`;
                        optBtn.innerText = opt;
                        optBtn.onclick = () => selectOption(qIndex, optIndex);
                        optsDiv.appendChild(optBtn);
                    });
                    
                    const expDiv = document.createElement("div");
                    expDiv.className = "explanation";
                    expDiv.id = `explanation-${qIndex}`;
                    expDiv.innerText = q.explanation;
                    
                    qDiv.appendChild(optsDiv);
                    qDiv.appendChild(expDiv);
                    quizQuestions.appendChild(qDiv);
                });

                document.getElementById("submit-quiz-btn").style.display = "block";
                document.getElementById("submit-quiz-btn").disabled = false;
                document.getElementById("score-banner").style.display = "none";
                document.getElementById("quiz-container").style.display = "block";
            }

            function selectOption(qIndex, optIndex) {
                // Remove selected class from other options of this question
                const optionsCount = currentLessonData.quiz[qIndex].options.length;
                for (let i = 0; i < optionsCount; i++) {
                    const btn = document.getElementById(`q-${qIndex}-opt-${i}`);
                    if (btn) btn.classList.remove("selected");
                }
                
                // Add selected class to this option
                const selectedBtn = document.getElementById(`q-${qIndex}-opt-${optIndex}`);
                if (selectedBtn) selectedBtn.classList.add("selected");
                
                userAnswers[qIndex] = optIndex;
            }

            async function gradeQuiz() {
                // Check if all answered
                const totalQuestions = currentLessonData.quiz.length;
                for (let i = 0; i < totalQuestions; i++) {
                    if (userAnswers[i] === undefined) {
                        alert("Please answer all questions before submitting!");
                        return;
                    }
                }

                let score = 0;
                for (let i = 0; i < totalQuestions; i++) {
                    const correctIdx = currentLessonData.quiz[i].correct;
                    const selectedIdx = userAnswers[i];
                    
                    const explanation = document.getElementById(`explanation-${i}`);
                    explanation.style.display = "block";
                    
                    // Style options
                    for (let optIdx = 0; optIdx < currentLessonData.quiz[i].options.length; optIdx++) {
                        const btn = document.getElementById(`q-${i}-opt-${optIdx}`);
                        btn.disabled = true; // disable option click
                        
                        if (optIdx === correctIdx) {
                            btn.classList.add("correct");
                        } else if (optIdx === selectedIdx) {
                            btn.classList.add("incorrect");
                        }
                    }

                    if (selectedIdx === correctIdx) {
                        score++;
                    }
                }

                // Submit to backend API
                await fetch("/api/quiz", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        topic: currentLessonData.title,
                        score: score,
                        total: totalQuestions
                    })
                });

                // Update UI
                document.getElementById("submit-quiz-btn").style.display = "none";
                document.getElementById("score-text").innerText = `You scored ${score}/${totalQuestions}!`;
                document.getElementById("score-banner").style.display = "block";
                
                // Refresh profile stats/history
                await loadProfile();
            }

            // Initial load
            window.onload = loadProfile;
        </script>
    </body>
    </html>
    """


if __name__ == "__main__":
    uvicorn.run("demo_server:app", host="0.0.0.0", port=18081, reload=False)
