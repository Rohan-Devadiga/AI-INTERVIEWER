# AI Interviewer
### A Virtual Interview Practice Partner

---

## Overview
**AI Interviewer** is a voice-based interview simulation system designed to help students and job seekers practice real interviews.  
It offers an interactive and adaptive experience, allowing users to build confidence and improve both communication and technical skills through realistic practice sessions.

---

## Features

### Voice-Based Interaction
- The AI conducts the interview entirely through speech.  
- **Text-to-Speech (TTS):** The AI interviewer asks questions naturally.  
- **Speech-to-Text (STT):** The user's verbal responses are converted into text for processing.  

### Adaptive Questioning
- Questions are generated dynamically based on previous answers.  
- The system stores interview history and adapts future questions accordingly, creating a realistic and context-aware interview flow.  

### Technical Round
- After general questions, the AI conducts a **technical coding round**.  
- Users can write and submit code directly in the interface or terminal.  
- Code is analyzed for:
  - Syntax errors  
  - Optimization opportunities  
  - Better or alternative approaches  

### Simple Execution
- The project can be easily run using a single Python script (`demo.py`).  
- No complex setup or configurations are required — simply install dependencies and start the demo.  

---

## Installation and Setup

Follow the steps below to set up and run the project on your local machine.

### 1. Clone the Repository
<```bash
git clone (https://github.com/Rohan-Devadiga/AI-INTERVIEWER.git)<br>
cd ai-interviewer 

### 2. Create a Virtual Environment (Recommended)
python -m venv venv

### 3. Activate the Virtual Environment
On Windows:<br>
venv\Scripts\activate

On macOS/Linux:<br>
source venv/bin/activate

### 4. Install Dependencies
pip install -r requirements.txt

### 5. Add Your API Key<br>

Before running the project, you must add your own API key.<br>
Create a file named .env in the root directory and add the following line:<br>
KEY="GEMINI_API_KEY"<br>
STTKEY="DEEPGRAM_API_KEY"

### 6. Run the Demo
python demo.py
