# 🤖 RADEEC RAG Chatbot

## 📌 Overview
RADEEC RAG Chatbot is an AI-powered customer support assistant built using Retrieval-Augmented Generation (RAG).

The chatbot combines semantic search with Large Language Models (LLMs) to provide accurate and context-aware answers to customer questions about:

- Water consumption
- Billing information
- Frequently Asked Questions (FAQ)

This project demonstrates how AI can automate customer service and improve user experience using modern NLP technologies.

---

## 🎯 Objectives

The main objectives of this project are:

- Automate responses to customer questions
- Retrieve relevant information using semantic search
- Provide accurate answers using AI
- Connect AI with structured database (SQLite)
- Build an intelligent chatbot using RAG architecture
- Demonstrate real-world AI application

---

## 🚀 Features

- 🔍 Retrieval-Augmented Generation (RAG)
- 🧠 Semantic search using embeddings
- 🤖 Response generation using LLM (LLaMA 3 via Groq API)
- 💬 Interactive chatbot interface
- 🗄️ SQLite database integration
- 📊 Customer consumption information retrieval
- 💳 Billing query support
- 📚 FAQ knowledge base
- ⚡ Fast similarity search using FAISS
- 🔐 Secure API key storage using .env file

---

## 🛠️ Technologies Used

### Programming Language
- Python

### AI & NLP
- LangChain
- Sentence Transformers
- LLaMA 3 (Groq API)

### Database
- SQLite
- FAISS (Vector Database)

### Interface
- Streamlit

### Environment Management
- dotenv

---

## 🧠 How RAG Works

RAG (Retrieval-Augmented Generation) combines information retrieval with text generation:

1. User asks a question
2. The question is converted into embeddings
3. Similar information is retrieved from knowledge base
4. Context is sent to the LLM
5. LLM generates accurate answer
6. Answer is displayed in chatbot interface

---

## 📂 Project Structure

```
RADEEC_CHATBOT_PROJECT/
│
├── chatbot.py           # Main chatbot application
├── database.py          # Database connection and queries
├── data_data.txt        # Knowledge base text file
├── requirements.txt     # Project dependencies
├── README.md            # Documentation
```

---

## ▶️ Installation

### 1. Clone repository

```bash
git clone https://github.com/Souadzriouil/RADEEC_CHATBOT_PROJECT.git
cd RADEEC_CHATBOT_PROJECT
```

### 2. Create virtual environment (optional)

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create .env file

Create a file named `.env` in the project folder:

```env
GROQ_API_KEY=your_api_key_here
```

### 5. Run application

```bash
streamlit run chatbot.py
```

### 6. Open in browser

```
http://localhost:8501
```

---

## 💬 Example Questions

The chatbot can answer questions such as:

- What is my water consumption?
- What is the amount of my bill?
- How can I pay my bill?
- What services does RADEEC provide?
- Frequently asked questions

---

## 📸 Demo

### Chatbot Interface

<img width="1566" height="688" alt="Interface_principale" src="https://github.com/user-attachments/assets/8976601b-7eff-4793-b5dd-6274caed6c32" />


### Water Consumption Example

<img width="1326" height="784" alt="Consommation_eau" src="https://github.com/user-attachments/assets/7e7ef0d0-e825-498b-a5b5-89641c28eb26" />


### Billing Example

<img width="1353" height="784" alt="Consultation facture" src="https://github.com/user-attachments/assets/94098eef-dec7-4978-8370-9588e18abf41" />

---

## 🔒 Security

- API keys are stored in `.env`
- `.env` file is not shared publicly
- Sensitive information is protected
- Database is stored locally

---

## 📈 Future Improvements

- Add multilingual support (Arabic / French / English)
- Improve user interface design
- Add voice chatbot
- Deploy online (Streamlit Cloud)
- Connect to real company database
- Add authentication system

---

## 💡 Use Case

This chatbot can be used by:

- Water companies
- Electricity providers
- Customer service centers
- Government services
- Support teams

Benefits:

- 24/7 customer support
- Faster response time
- Reduced workload for employees
- Better user experience

---

## 👩‍💻 Author

**Souad Zriouil**  
AI Engineer | Data Scientist | Machine Learning | NLP | LLM  

[![GitHub](https://img.shields.io/badge/GitHub-Souadzriouil-black?logo=github)](https://github.com/Souadzriouil)

---

## ⭐ Support

If you like this project:

- ⭐ Star the repository
- Share on LinkedIn
- Add to your portfolio

---

## 📄 License

This project is for educational and research purposes.
