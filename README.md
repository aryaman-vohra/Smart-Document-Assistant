# 🧠 Smart Document Assistant  
**Transform your documents into interactive learning tools.**  

---

## 🚀 Features

- 📄 **Document Upload**: Supports `.pdf` and `.txt` files (max 10MB)  
- 🧠 **Auto Summary**: Generates a concise 150-word summary  
- 💬 **Ask Anything Mode**: Natural language Q&A over your document  
- 🎯 **Challenge Mode**: AI-generated comprehension quizzes  
- 🧠 **Session Memory**: Maintains conversational context  
- 📚 **Cited Answers**: Every response includes document references  

---

## 🛠️ Quick Start

### ✅ Prerequisites
- Python **3.8+**
- **Gemini API Key** from [Google AI Studio](https://makersuite.google.com/app)

### 📦 Installation

git clone https://github.com/<your-username>/smart-document-assistant.git
cd smart-document-assistant
pip install -r requirements.txt

### 📦 Setup API Key
cp .env.example .env
# Edit .env and add:
GEMINI_API_KEY=your-key-here
▶️ Run the App
streamlit run app.py
📍 Access at: http://localhost:8501

### 🧩 Architecture Overview
Module	Responsibilities
DocumentProcessor	Parses & cleans PDF/TXT files
AIAssistant	Summarizes content, answers questions, remembers context
QuestionGenerator	Creates quizzes & evaluates user responses

### 📈 Data Flow


Upload ➝ Text Extraction ➝ Summary Generation
                         ➝
   Ask Anything ➝ Contextual Gemini Response
                         ➝
      Challenge Me ➝ AI Questions ➝ Your Answers ➝ Evaluation

### ⚙️ Configuration
Edit config/settings.py to customize:

model: Gemini model name

temperature: Creativity level (default: 0.7)

chunk_size: Document chunk size (for splitting long text)

max_tokens: Max tokens in API response

### 🔐 Security & Privacy
🛡️ Local document processing (no permanent storage)

🔒 Secure API calls to Gemini (Google AI)

❌ No session data is persisted

### ⚡ Performance Optimization
📦 Chunked Processing: Handles large documents

🎯 Prompt Engineering: Efficient input design

🧠 Streamlit Caching: Fast reloads with @st.cache_resource

⚡ Streaming API: Fast Gemini responses

### 🧪 Error Handling
✅ File validation: size and type

✅ API fallback with friendly messages

✅ Input checks with visual feedback

### 🛠️ Troubleshooting
Issue	Solution
🔑 API Key Error	Make sure GEMINI_API_KEY is set in .env
📄 Upload Fails	File must be .pdf or .txt, ≤10MB size
🐢 Slow Response	Use smaller or more focused documents

### 🔮 Future Enhancements

🗂️ Multi-document support

✍️ Editable quiz questions before evaluation

📤 Export summaries / QA results

📊 Analytics dashboard

🌐 Multilingual document support



