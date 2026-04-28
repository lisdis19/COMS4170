# 🏐 VolleyLearn

An interactive web app for learning volleyball — covering positions, plays, and formations through guided lessons and hands-on drag-and-drop challenges.

Built for **COMS 4170: User Interface Design** at Columbia University.

---

## What It Does

VolleyLearn walks users through two core learning experiences:

**Learn** — Step-by-step lessons on volleyball positions and roles. Each lesson lets users make a selection to reinforce what they just read before moving on.

**Build-a-Play** — Drag-and-drop court challenges where users place players into the correct zones. The app gives instant feedback on each placement and tracks performance across all challenges.

---

## Tech Stack

- **Backend:** Python / Flask
- **Frontend:** HTML, Jinja2 templates, JavaScript
- **Data:** JSON files for lessons and challenges (`data/content.json`, `data/challenges.json`)

---

## Project Structure

```
COMS4170/
├── app.py                  # Flask routes and session logic
├── data/
│   ├── content.json        # Lesson content and quiz data
│   └── challenges.json     # Build-a-Play challenge definitions
└── templates/
    ├── home.html
    ├── learn.html
    ├── play_intro.html
    ├── play.html
    └── play_result.html
```

---

## Running Locally

**1. Clone the repo**
```bash
git clone https://github.com/lisdis19/COMS4170.git
cd COMS4170
```

**2. Install dependencies**
```bash
pip install flask
```

**3. Start the app**
```bash
python app.py
```

**4. Open in your browser**
```
http://localhost:5000
```

---

## Routes

| Route | Description |
|---|---|
| `/` | Home / landing page |
| `/start` | Begins a new session, resets the log |
| `/learn/<n>` | Lesson page for lesson number `n` |
| `/play` | Build-a-Play intro screen |
| `/play/<n>` | Challenge number `n` |
| `/play/result` | Final results screen |
| `/api/log` | JSON dump of the current session log (for TA demo) |

---

## Course

**COMS 4170 — User Interface Design**  
Columbia University, Spring 2026
