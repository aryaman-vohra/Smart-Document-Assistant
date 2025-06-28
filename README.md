🧠 Smart Document Assistant
Transform your documents into interactive learning tools using Gemini-powered AI.




🚀 Features
📄 Document Upload: Supports .pdf and .txt (up to 10MB)

🧠 Auto Summary: Generates a 150-word concise summary

💬 Ask Anything Mode: Natural language Q&A over your document

🎯 Challenge Mode: Test your understanding with AI-generated quizzes

🔁 Conversation Memory: Maintains session history

📚 Cited Responses: All answers include document-based references

🛠️ Quick Start
✅ Prerequisites
Python 3.8+

Gemini API Key (from Google AI Studio)

📦 Installation
git clone https://github.com/<your-username>/smart-document-assistant.git
cd smart-document-assistant
pip install -r requirements.txt
🔐 Setup API Key
cp .env.example .env
# Open `.env` and add your Gemini API key
GEMINI_API_KEY=your-key-here
▶️ Run the App
streamlit run app.py
Open in browser: http://localhost:8501

🧩 Architecture Overview
Core Modules
Module	Responsibilities
DocumentProcessor	Parses and cleans PDF/TXT files
AIAssistant	Handles summarization, Q&A, session memory
QuestionGenerator	Creates challenge questions & evaluates answers

📈 Data Flow
Upload → Text Extraction → Summary Generation
                ↓
Ask Anything → Contextual Gemini Response
                ↓
Challenge Me → Question Generation → User Answer → Evaluation
⚙️ Configuration
Customize behavior via config/settings.py:

model: Gemini model name

temperature: Controls creativity (default: 0.7)

chunk_size: Document chunking for large inputs

max_tokens: Limit API output size

🔐 Security & Privacy
Documents are processed locally and not stored

API requests are made securely to Google AI endpoints

No data is persisted between sessions

⚡ Optimization Techniques-

Chunked document processing

Token-efficient prompt design

Cached components (@st.cache_resource)

Minimal latency with Gemini streaming

🧪 Error Handling

✅ File size and type validation

✅ Graceful fallback for API errors

✅ Empty input checks with clear messages

🛠️ Troubleshooting
Issue	Solution
🔑 API Key Error	Ensure GEMINI_API_KEY is set in .env
📄 Upload Fails	Check file size (≤10MB), use PDF or TXT
🐢 Slow Response	Large docs take longer—reduce file size

🔮 Future Enhancements-

🗃️ Multi-document support

✍️ Editable questions before evaluation

📤 Export summary/QA results

📊 Performance analytics

🌐 Multilingual support