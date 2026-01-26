# Ignite 🚀

**Ignite** is a developer tool that automates the setup of a new development machine. Instead of visiting 20 different websites to download Chrome, VS Code, Docker, and Slack, Ignite lets you select your stack, click one button, and watch as it provisions your machine automatically.

It supports **macOS (Homebrew)**, **Windows (Winget)**, and **Linux (APT)**, making it a truly cross-platform solution.

## 💡 Why I Built This

I recently acquired a new MacBook and was excited to start coding, but the setup process was a nightmare. I spent hours hopping from site to site, downloading `.dmg` files, dragging icons to folders, and dealing with permission issues.

As someone new to the macOS ecosystem at the time, I also struggled with **Homebrew**—running terminal commands I didn't fully understand and dealing with "command not found" errors.

I saw a similar concept on Twitter once, but it was limited to just a simple script. I decided to take it a notch higher. I wanted a tool that:
1.  **Has a beautiful GUI:** No more scary terminal commands for beginners.
2.  **Is Cross-Platform:** Works whether you are on a Mac, a Windows gaming rig, or a Linux server.
3.  **Is Real-Time:** Shows exactly what is happening (downloading, installing, verifying) with live feedback.

Ignite is the result—a bridge between complex package managers and a simple, user-friendly experience.

## ✨ Features

* **Cross-Platform Support:** Auto-detects your OS and uses the native package manager:
    * 🍏 **macOS:** Homebrew (Install & verify)
    * 🪟 **Windows:** Winget
    * 🐧 **Linux:** APT (Debian/Ubuntu)
* **Smart App Resolution:** Automatically finds the correct package ID (e.g., converts "Chrome" -> `google-chrome` or `google-chrome-stable` depending on the OS).
* **Custom Requests:** Install any app supported by your package manager, even if it's not in the preset list.
* **Real-Time Progress:** Uses **Redis** and **Polling** to provide a live "installation console" in the UI.
* **Self-Healing:** Detects if an app is "phantom installed" (broken links) and attempts to force-repair it.

## 🛠️ Tech Stack

* **Frontend:** React (Vite), Tailwind CSS, Lucide Icons, Sonner (Toasts).
* **Backend:** Python (FastAPI).
* **Database:** Redis (for stateless job tracking and real-time status updates).
* **System:** Subprocess & Threading (for non-blocking background installations).

## 🚀 Getting Started

### Prerequisites
* **Python 3.8+**
* **Node.js 16+**
* **Redis** (Must be running locally)

### 1. Frontend Setup

The frontend is the visual dashboard.

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Build the UI
npm run build

```

### 2. Backend Setup
The backend handles the actual installation commands and renders the frontend build.

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install requirements.txt

# Start Redis (In a separate terminal)
redis-server

# Start the API Server
# Note: On Linux, you might need 'sudo' to allow installations
uvicorn backend.main:app --reload

```

Open `http://localhost:8000` (or your local port) to see Ignite in action.

## 📸 How It Works

1. **Selection:** You pick apps from the grid or type a custom name (e.g., "blender").
2. **Payload:** The frontend sends a list `["google-chrome", "blender"]` to the `/install` endpoint.
3. **Queue:** The Backend accepts the request, creates a job ID, and pushes the initial state to **Redis**.
4. **Worker:** A background thread picks up the job. It determines your OS (Mac/Win/Lin) and runs the specific CLI commands (`brew install`, `winget install`, etc.).
5. **Polling:** The Frontend polls the `/progress` endpoint every 1 second.
6. **Updates:** As the backend installs each app, it updates Redis. The Frontend sees this and turns the specific app icon **Green** (Success) or **Red** (Error with reason).

## ⚠️ Notes

* **macOS Users:** If an app installs but doesn't appear in Spotlight immediately, give it a moment for indexing. Check `~/Applications` if not found in the main folder.
* **Linux Users:** Running the backend with `sudo` is recommended so `apt` doesn't pause waiting for a password.

## 📄 License

MIT License. Free to use and modify!

```
