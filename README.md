<div align="center">

# 🤖 RADEEC RAG Chatbot

### 🧠 AI-Powered Customer Support Assistant using Retrieval-Augmented Generation (RAG)

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/LangChain-121212?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/LLaMA%203-Groq-success?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/FAISS-Vector%20Search-blue?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Streamlit-Interactive-red?style=for-the-badge"/>
</p>

</div>

---

# 📌 Overview

RADEEC RAG Chatbot is an AI-powered customer support assistant built using **Retrieval-Augmented Generation (RAG)** architecture.

The chatbot combines:

- 🔍 Semantic search
- 🧠 Large Language Models (LLMs)
- 📚 Knowledge retrieval
- 💬 Interactive conversational AI

to provide accurate and context-aware responses to customer questions related to:

- Water consumption
- Billing information
- Frequently Asked Questions (FAQ)

This project demonstrates how modern NLP and Generative AI technologies can automate customer support and improve user experience.

---

# 🎯 Project Objectives

- Automate customer support interactions
- Retrieve relevant information using semantic search
- Generate intelligent AI responses
- Integrate AI with structured databases
- Build a real-world RAG pipeline
- Demonstrate practical LLM applications

---

# 🚀 Features

✅ Retrieval-Augmented Generation (RAG) architecture  
✅ Semantic search using embeddings  
✅ LLM response generation with LLaMA 3 (Groq API)  
✅ Interactive chatbot interface with Streamlit  
✅ SQLite database integration  
✅ Customer billing and consumption support  
✅ FAQ knowledge base retrieval  
✅ Fast vector similarity search using FAISS  
✅ Secure API key management using `.env`  

---

# 🛠️ Technologies Used

| Category | Technologies |
|---|---|
| Programming Language | Python |
| LLM Framework | LangChain |
| Embedding Model | Sentence Transformers |
| Large Language Model | LLaMA 3 (Groq API) |
| Vector Database | FAISS |
| Database | SQLite |
| Interface | Streamlit |
| Environment Management | python-dotenv |

---

# 🧠 How RAG Works

<div align="center">

```text
User Question
      ↓
Text Embedding
      ↓
Semantic Search (FAISS)
      ↓
Relevant Context Retrieval
      ↓
LLaMA 3 Response Generation
      ↓
Final AI Answer
```

</div>

---

# 📂 Project Structure

```bash
RADEEC_CHATBOT_PROJECT/
│
├── chatbot.py
├── database.py
├── data_data.txt
├── requirements.txt
├── README.md
└── .env
```

---

# 📸 Application Preview

## 💬 Main Chatbot Interface

<p align="center">
  <img width="1000" src="https://github.com/user-attachments/assets/8976601b-7eff-4793-b5dd-6274caed6c32"/>
</p>

---

## 💧 Water Consumption Example

<p align="center">
  <img width="900" src="https://github.com/user-attachments/assets/7e7ef0d0-e825-498b-a5b5-89641c28eb26"/>
</p>

---

## 💳 Billing Information Example

<p align="center">
  <img width="900" src="https://github.com/user-attachments/assets/94098eef-dec7-4978-8370-9588e18abf41"/>
</p>

---

# ⚙️ Installation

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/Souadzriouil/RADEEC_CHATBOT_PROJECT.git
cd RADEEC_CHATBOT_PROJECT
```

---

## 2️⃣ Create Virtual Environment (Optional)

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_api_key_here
```

---

## 5️⃣ Run the Application

```bash
streamlit run chatbot.py
```

---

# 🌐 Access the Application

Open your browser and navigate to:

```bash
http://localhost:8501
```

---

# 💬 Example Questions

The chatbot can answer questions such as:

- What is my water consumption?
- What is the amount of my bill?
- How can I pay my bill?
- What services does RADEEC provide?
- Frequently asked customer questions

---

# 🔒 Security

- API keys stored securely using `.env`
- Sensitive credentials excluded from GitHub
- Local database management
- Environment variable protection

---

# 📈 Future Improvements

- [ ] Multilingual support (Arabic / French / English)
- [ ] Voice-enabled chatbot
- [ ] Improved UI/UX design
- [ ] Online deployment with Streamlit Cloud
- [ ] Real company database integration
- [ ] Authentication system
- [ ] Chat history persistence
- [ ] PDF document ingestion

---

# 💡 Potential Use Cases

This chatbot architecture can be adapted for:

- Water utility companies
- Electricity providers
- Customer service centers
- Government services
- AI-powered support systems

### Benefits

✅ 24/7 customer support  
✅ Faster response times  
✅ Reduced operational workload  
✅ Improved customer experience  

---

# 👩‍💻 Author

<div align="center">

## Souad Zriouil

### AI Engineer | Data Scientist | Machine Learning | NLP | LLM

<p align="center">
  <a href="https://github.com/Souadzriouil">
    <img src="https://img.shields.io/badge/GitHub-Souadzriouil-181717?style=for-the-badge&logo=github"/>
  </a>

  <a href="https://www.linkedin.com/in/souad-zriouil-54b19b267">
    <img src="https://img.shields.io/badge/LinkedIn-Souad%20Zriouil-0077B5?style=for-the-badge&logo=linkedin"/>
  </a>
</p>

</div>

---

# ⭐ Support

If you find this project useful:

- ⭐ Star the repository
- 🔄 Share it on LinkedIn
- 📌 Add it to your portfolio

---

# 📄 License

This project is intended for educational and research purposes.
