import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer, util
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import sqlite3
import os
import re
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()  
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# FONCTIONS BASE DE DONNÉES 

def connect_db():
    """Connexion à la base de données SQLite"""
    conn = sqlite3.connect('radeec.db')
    return conn

def check_account_and_get_consumption(numero_de_compte, mois=None, annee=None):
    """
    Récupère la consommation pour un compte et un mois spécifique
    
    Args:
        numero_de_compte: Numéro du compte client
        mois: Mois en français (ex: 'novembre', 'octobre') ou None pour le dernier
        annee: Année (ex: 2024) ou None pour l'année courante
    
    Returns:
        dict avec les infos de consommation ou None si non trouvé
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        # Vérifier si le compte existe
        cursor.execute("SELECT COUNT(*) FROM clients WHERE numero_compte=?", (numero_de_compte,))
        if cursor.fetchone()[0] == 0:
            conn.close()
            return None
        
        # Dictionnaire pour normaliser les mois (sans accent et avec accent)
        mois_normalisation = {
            'janvier': 'Janvier', 'fevrier': 'Février', 'février': 'Février',
            'mars': 'Mars', 'avril': 'Avril', 'mai': 'Mai', 'juin': 'Juin',
            'juillet': 'Juillet', 'aout': 'Août', 'août': 'Août',
            'septembre': 'Septembre', 'octobre': 'Octobre',
            'novembre': 'Novembre', 'decembre': 'Décembre', 'décembre': 'Décembre'
        }
        
        # Normaliser le mois si fourni
        if mois:
            mois_normalise = mois_normalisation.get(mois.lower(), mois.capitalize())
        else:
            mois_normalise = None
        
        # Construire la requête selon les paramètres
        if mois_normalise and annee:
            # Recherche pour un mois et une année spécifiques
            cursor.execute("""
                SELECT consommation_m3, date_releve, mois 
                FROM consommations 
                WHERE numero_compte=? AND LOWER(mois)=? AND strftime('%Y', date_releve)=?
                ORDER BY date_releve DESC
                LIMIT 1
            """, (numero_de_compte, mois_normalise.lower(), str(annee)))
        elif mois_normalise:
            # Recherche pour un mois spécifique (année courante)
            annee_courante = str(datetime.now().year)
            cursor.execute("""
                SELECT consommation_m3, date_releve, mois 
                FROM consommations 
                WHERE numero_compte=? AND LOWER(mois)=? AND strftime('%Y', date_releve)=?
                ORDER BY date_releve DESC
                LIMIT 1
            """, (numero_de_compte, mois_normalise.lower(), annee_courante))
        else:
            # Dernière consommation disponible
            cursor.execute("""
                SELECT consommation_m3, date_releve, mois 
                FROM consommations 
                WHERE numero_compte=?
                ORDER BY date_releve DESC
                LIMIT 1
            """, (numero_de_compte,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            # Extraire l'année de la date
            date_obj = datetime.strptime(result[1], '%Y-%m-%d')
            return {
                'consumption': result[0],
                'date_releve': result[1],
                'month': result[2],
                'year': date_obj.year
            }
        return None
        
    except Exception as e:
        conn.close()
        print(f"Erreur consommation: {e}")
        return None

def check_facture(numero_de_compte, mois=None, annee=None):
    """
    Vérifie les factures pour un compte et éventuellement un mois spécifique
    
    Args:
        numero_de_compte: Numéro du compte client
        mois: Mois en français (ex: 'novembre') ou None pour toutes
        annee: Année (ex: 2024) ou None pour l'année courante
    
    Returns:
        Liste de tuples (mois, annee, montant, statut, date_facture, numero_facture)
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        # Vérifier si le compte existe
        cursor.execute("SELECT COUNT(*) FROM clients WHERE numero_compte=?", (numero_de_compte,))
        if cursor.fetchone()[0] == 0:
            conn.close()
            return []
        
        # Dictionnaire pour convertir les mois
        mois_dict = {
            'janvier': 1, 'février': 2, 'mars': 3, 'avril': 4,
            'mai': 5, 'juin': 6, 'juillet': 7, 'août': 8,
            'septembre': 9, 'octobre': 10, 'novembre': 11, 'décembre': 12
        }
        mois_noms = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin',
                     'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']
        
        # Construire la requête selon les paramètres
        if mois and annee:
            # Recherche pour un mois et une année spécifiques
            mois_num = mois_dict.get(mois.lower())
            if not mois_num:
                conn.close()
                return []
            
            cursor.execute("""
                SELECT numero_facture, montant, date_facture, etat 
                FROM factures 
                WHERE numero_compte=? 
                AND strftime('%m', date_facture)=? 
                AND strftime('%Y', date_facture)=?
                ORDER BY date_facture DESC
            """, (numero_de_compte, f"{mois_num:02d}", str(annee)))
            
        elif mois:
            # Recherche pour un mois spécifique (année courante)
            mois_num = mois_dict.get(mois.lower())
            if not mois_num:
                conn.close()
                return []
            
            annee_courante = str(datetime.now().year)
            cursor.execute("""
                SELECT numero_facture, montant, date_facture, etat 
                FROM factures 
                WHERE numero_compte=? 
                AND strftime('%m', date_facture)=? 
                AND strftime('%Y', date_facture)=?
                ORDER BY date_facture DESC
            """, (numero_de_compte, f"{mois_num:02d}", annee_courante))
            
        else:
            # Toutes les factures
            cursor.execute("""
                SELECT numero_facture, montant, date_facture, etat 
                FROM factures 
                WHERE numero_compte=?
                ORDER BY date_facture DESC
            """, (numero_de_compte,))
        
        factures = cursor.fetchall()
        conn.close()
        
        # Reformater les résultats
        factures_formatees = []
        for f in factures:
            numero_facture = f[0]
            montant = f[1]
            date_facture = f[2]
            etat = f[3]
            
            # Extraire le mois et l'année de la date
            try:
                date_obj = datetime.strptime(date_facture, '%Y-%m-%d')
                mois_nom = mois_noms[date_obj.month - 1]
                annee_facture = date_obj.year
            except:
                mois_nom = "inconnu"
                annee_facture = datetime.now().year
            
            factures_formatees.append((
                mois_nom,
                annee_facture,
                montant,
                etat,
                date_facture,
                numero_facture
            ))
        
        return factures_formatees
        
    except Exception as e:
        conn.close()
        print(f"Erreur factures: {e}")
        return []

def get_client_info(numero_de_compte):
    """Récupère les informations complètes d'un client"""
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT numero_compte, nom, prenom, cin, adresse, telephone, email 
            FROM clients 
            WHERE numero_compte=?
        """, (numero_de_compte,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'numero_compte': result[0],
                'nom': result[1],
                'prenom': result[2],
                'cin': result[3],
                'adresse': result[4],
                'telephone': result[5],
                'email': result[6]
            }
        return None
        
    except Exception as e:
        conn.close()
        print(f"Erreur client: {e}")
        return None

def extraire_mois_annee(texte):
    """
    Extrait le mois et l'année d'un texte
    
    Returns:
        tuple (mois, annee) ou (None, None) si non trouvé
    """
    mois_dict = {
        'janvier': 'janvier', 'fevrier': 'février', 'février': 'février',
        'mars': 'mars', 'avril': 'avril', 'mai': 'mai', 'juin': 'juin',
        'juillet': 'juillet', 'aout': 'août', 'août': 'août',
        'septembre': 'septembre', 'octobre': 'octobre',
        'novembre': 'novembre', 'decembre': 'décembre', 'décembre': 'décembre'
    }
    
    texte_lower = texte.lower()
    
    # Chercher le mois
    mois_trouve = None
    for mois_key, mois_val in mois_dict.items():
        if mois_key in texte_lower:
            mois_trouve = mois_val
            break
    
    # Chercher l'année (4 chiffres)
    annee_match = re.search(r'\b(20\d{2})\b', texte)
    annee_trouvee = int(annee_match.group(1)) if annee_match else None
    
    return mois_trouve, annee_trouvee


# FONCTIONS IA ET RAG


@st.cache_resource
def initialize_llm():
    """Initialiser le modèle Llama via Groq"""
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.3,
        max_tokens=1024,
        groq_api_key=GROQ_API_KEY
    )
    return llm

@st.cache_resource
def initialize_vectorstore(file_path):
    """Charger et préparer le vectorstore pour RAG"""
    try:
        # Charger les données
        data = pd.read_csv(file_path)
        
        # Créer des documents combinant questions et réponses
        documents = []
        for _, row in data.iterrows():
            doc_text = f"Question: {row['Question']}\nRéponse: {row['Réponse']}"
            documents.append(doc_text)
        
        # Splitter les documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            length_function=len
        )
        splits = text_splitter.create_documents(documents)
        
        # Créer les embeddings avec un modèle multilingue
        embeddings = HuggingFaceEmbeddings(
            model_name="paraphrase-multilingual-MiniLM-L12-v2"
        )
        
        # Créer le vectorstore FAISS
        vectorstore = FAISS.from_documents(splits, embeddings)
        return vectorstore
    except Exception as e:
        st.error(f"Erreur lors du chargement du vectorstore: {str(e)}")
        return None

def rag_response(question, vectorstore, llm):
    """Fonction RAG pour générer une réponse avec Llama via Groq"""
    try:
        # Récupérer les documents pertinents
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        relevant_docs = retriever.invoke(question)
        
        # Construire le contexte
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        
        # Créer le prompt pour Llama
        prompt_template = ChatPromptTemplate.from_template(
            """Tu es un assistant virtuel professionnel pour RADEEC (Régie Autonome de Distribution d'Eau et d'Électricité).
            
Contexte pertinent extrait de la base de connaissances:
{context}

Question de l'utilisateur: {question}

Instructions importantes:
- Réponds en français de manière claire, professionnelle et amicale
- Utilise UNIQUEMENT le contexte fourni ci-dessus pour répondre
- Si le contexte ne contient pas l'information nécessaire, dis poliment que tu n'as pas cette information dans ta base de connaissances
- Sois concis mais informatif (maximum 3-4 phrases)
- N'invente jamais d'informations
- Utilise des emojis appropriés pour rendre la réponse plus conviviale

Réponse:"""
        )
        
        # Générer la réponse
        messages = prompt_template.format_messages(context=context, question=question)
        response = llm.invoke(messages)
        
        return response.content
    except Exception as e:
        return f"Désolé, une erreur s'est produite lors de la génération de la réponse: {str(e)}"

# Ensemble de questions de référence pour chaque intention
intention_questions = {
    "consommation": [
        "Quelle est ma consommation pour ce mois ?", 
        "Combien d'eau ai-je consommé ?", 
        "Je veux voir ma consommation d'eau.",
        "Ma consommation mensuelle",
        "consommation du mois",
        "consommation d'eau"
    ],
    "facture": [
        "Montrez-moi mes factures", 
        "Combien dois-je payer ?", 
        "Je veux vérifier ma facture pour un certain mois.",
        "Mes factures impayées",
        "facture du mois",
        "paiement facture",
        "combien je dois"
    ]
}

def detect_intention(question, intention_questions, model):
    """Fonction pour détecter l'intention avec embeddings"""
    max_score = 0
    detected_intention = None
    question_embedding = model.encode(question, convert_to_tensor=True)
    
    for intention, examples in intention_questions.items():
        example_embeddings = model.encode(examples, convert_to_tensor=True)
        cosine_scores = util.pytorch_cos_sim(question_embedding, example_embeddings).max().item()
        if cosine_scores > max_score and cosine_scores > 0.65:
            max_score = cosine_scores
            detected_intention = intention
    return detected_intention


# CONFIGURATION STREAMLIT

st.set_page_config(page_title="Assistant RADEEC", page_icon="💧", layout="wide")

# Styling avec du markdown
st.markdown("""
<style>
body {
    background-color: #f4f4f9;
    font-family: 'Arial', sans-serif;
}
.header {
    background: linear-gradient(135deg, #003366 0%, #0066cc 100%);
    color: white;
    padding: 25px;
    text-align: center;
    border-radius: 10px;
    margin-bottom: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.title {
    font-size: 2.5em;
    margin-bottom: 5px;
    font-weight: bold;
}
.subtitle {
    font-size: 1.2em;
    opacity: 0.9;
}
.message {
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
    animation: fadeIn 0.5s;
}
.user-message {
    background-color: #e3f2fd;
    border-left: 5px solid #2196f3;
    margin-left: 20%;
}
.chatbot-message {
    background-color: #f1f8e9;
    border-left: 5px solid #8bc34a;
    margin-right: 20%;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
.stButton>button {
    background-color: #003366;
    color: white;
    border-radius: 5px;
    padding: 10px 20px;
    border: none;
    transition: all 0.3s;
}
.stButton>button:hover {
    background-color: #0066cc;
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)

# En-tête et message de bienvenue
st.markdown("""
<div class='header'>
    <div class='title'>💧 Chatbot RADEEC</div>
    <div class='subtitle'>Votre assistant virtuel au service de vos besoins en eau et électricité.</div>
</div>
""", unsafe_allow_html=True)


# INITIALISATION DES MODÈLES

@st.cache_resource
def load_models():
    """Charger tous les modèles nécessaires"""
    try:
        embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        llm = initialize_llm()
        vectorstore = initialize_vectorstore("data_data.txt")
        return embedding_model, llm, vectorstore
    except Exception as e:
        st.error(f"Erreur lors du chargement des modèles: {str(e)}")
        return None, None, None

# Charger les modèles
with st.spinner("⚙️ Chargement des modèles IA..."):
    embedding_model, llm, vectorstore = load_models()

if embedding_model is None or llm is None or vectorstore is None:
    st.error("❌ Erreur lors de l'initialisation. Veuillez vérifier vos fichiers et votre connexion.")
    st.stop()


# GESTION DE L'ÉTAT DE SESSION

if 'history' not in st.session_state:
    st.session_state.history = []

if 'waiting_for' not in st.session_state:
    st.session_state.waiting_for = None


# INTERFACE PRINCIPALE


with st.container():
    st.write("👋 Bonjour ! Je suis l’assistant RADEEC. Posez-moi vos questions pour obtenir de l’aide sur vos factures, votre consommation ou nos services.")
    
    input_text = st.text_input("💬 Posez votre question!", placeholder="Ex: Comment puis-je payer ma facture en ligne ?", key="main_input")
    
    # Gérer les flux de conversation nécessitant des informations supplémentaires
    if st.session_state.waiting_for:
        
        # FLUX CONSOMMATION
        if st.session_state.waiting_for == "consommation_account":
            st.info("ℹ️ Pour consulter votre consommation, veuillez fournir votre numéro de compte:")
            numero_de_compte = st.text_input("📋 Numéro de compte:", key="account_input", placeholder="Ex: 123456")
            
            col1, col2 = st.columns([1, 5])
            with col1:
                if st.button("✅ Continuer"):
                    if numero_de_compte:
                        # Vérifier si le compte existe
                        client_info = get_client_info(numero_de_compte)
                        if client_info:
                            st.session_state.temp_account = numero_de_compte
                            st.session_state.waiting_for = "consommation_mois"
                            st.rerun()
                        else:
                            response = "❌ Compte introuvable.\n\n💡 **Comptes de test:** 123456, 654321, 789012"
                            st.session_state.history.append({"role": "assistant", "content": response})
                            st.session_state.waiting_for = None
                            st.rerun()
                    else:
                        st.warning("⚠️ Veuillez entrer le numéro de compte.")
            with col2:
                if st.button("❌ Annuler"):
                    st.session_state.waiting_for = None
                    st.rerun()
        
        elif st.session_state.waiting_for == "consommation_mois":
            st.info("📅 Voulez-vous consulter la consommation d'un mois spécifique ?")
            
            col1, col2 = st.columns(2)
            with col1:
                mois = st.selectbox(
                    "Sélectionnez un mois (optionnel):",
                    ["Dernière consommation", "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
                     "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"],
                    key="mois_select"
                )
            with col2:
                annee = st.number_input("Année:", min_value=2020, max_value=2025, 
                                       value=datetime.now().year, key="annee_input")
            
            col_btn1, col_btn2 = st.columns([1, 5])
            with col_btn1:
                if st.button("✅ Consulter"):
                    numero_de_compte = st.session_state.temp_account
                    
                    # Déterminer les paramètres de recherche
                    mois_param = None if mois == "Dernière consommation" else mois.lower()
                    annee_param = annee if mois != "Dernière consommation" else None
                    
                    result = check_account_and_get_consumption(numero_de_compte, mois_param, annee_param)
                    
                    if result:
                        response = f"""✅ **Consommation trouvée:**
                        
💧 **Consommation:** {result['consumption']} m³
📅 **Période:** {result['month']} {result['year']}
📊 **Date de relevé:** {result['date_releve']}"""
                    else:
                        if mois_param:
                            response = f"❌ Aucune consommation trouvée pour {mois} {annee}.\n\n💡 Essayez un autre mois ou consultez la dernière consommation."
                        else:
                            response = "❌ Aucune donnée de consommation disponible."
                    
                    st.session_state.history.append({"role": "assistant", "content": response})
                    st.session_state.waiting_for = None
                    if 'temp_account' in st.session_state:
                        del st.session_state.temp_account
                    st.rerun()
            
            with col_btn2:
                if st.button("❌ Annuler"):
                    st.session_state.waiting_for = None
                    if 'temp_account' in st.session_state:
                        del st.session_state.temp_account
                    st.rerun()
        
        #  FLUX FACTURES 
        elif st.session_state.waiting_for == "facture_account":
            st.info("ℹ️ Pour consulter vos factures, veuillez fournir votre numéro de compte:")
            numero_de_compte = st.text_input("📋 Numéro de compte:", key="facture_account_input", placeholder="Ex: 123456")
            
            col1, col2 = st.columns([1, 5])
            with col1:
                if st.button("✅ Continuer"):
                    if numero_de_compte:
                        client_info = get_client_info(numero_de_compte)
                        if client_info:
                            st.session_state.temp_account = numero_de_compte
                            st.session_state.waiting_for = "facture_mois"
                            st.rerun()
                        else:
                            response = "❌ Compte introuvable.\n\n💡 **Comptes de test:** 123456, 654321, 789012"
                            st.session_state.history.append({"role": "assistant", "content": response})
                            st.session_state.waiting_for = None
                            st.rerun()
            with col2:
                if st.button("❌ Annuler"):
                    st.session_state.waiting_for = None
                    st.rerun()
        
        elif st.session_state.waiting_for == "facture_mois":
            st.info("📅 Voulez-vous filtrer par mois ?")
            
            col1, col2 = st.columns(2)
            with col1:
                mois = st.selectbox(
                    "Sélectionnez un mois (optionnel):",
                    ["Toutes les factures", "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
                     "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"],
                    key="mois_facture_select"
                )
            with col2:
                annee = st.number_input("Année:", min_value=2020, max_value=2025, 
                                       value=datetime.now().year, key="annee_facture_input")
            
            col_btn1, col_btn2 = st.columns([1, 5])
            with col_btn1:
                if st.button("✅ Consulter"):
                    numero_de_compte = st.session_state.temp_account
                    
                    # Déterminer les paramètres de recherche
                    mois_param = None if mois == "Toutes les factures" else mois.lower()
                    annee_param = annee if mois != "Toutes les factures" else None
                    
                    factures = check_facture(numero_de_compte, mois_param, annee_param)
                    
                    if factures:
                        if mois_param:
                            response = f"📄 **Facture(s) pour {mois} {annee}:**\n\n"
                        else:
                            response = "📄 **Toutes vos factures:**\n\n"
                        
                        for facture in factures:
                            mois_f, annee_f, montant, statut, date_facture, numero_facture = facture
                            statut_emoji = "✅" if statut.lower() == "payée" else "⏳"
                            response += f"{statut_emoji} **{mois_f.capitalize()} {annee_f}**\n"
                            response += f"   💰 Montant: {montant} MAD\n"
                            response += f"   📋 N° Facture: {numero_facture}\n"
                            response += f"   📊 Statut: {statut}\n"
                            response += f"   📅 Date: {date_facture}\n\n"
                        
                        st.session_state.history.append({"role": "assistant", "content": response})
                    else:
                        if mois_param:
                            response = f"❌ Aucune facture trouvée pour {mois} {annee}."
                        else:
                            response = "❌ Aucune facture trouvée pour ce compte."
                        st.session_state.history.append({"role": "assistant", "content": response})
                    
                    st.session_state.waiting_for = None
                    if 'temp_account' in st.session_state:
                        del st.session_state.temp_account
                    st.rerun()
            
            with col_btn2:
                if st.button("❌ Annuler"):
                    st.session_state.waiting_for = None
                    if 'temp_account' in st.session_state:
                        del st.session_state.temp_account
                    st.rerun()
    
    # Traitement de la question initiale
    elif input_text:
        submit_button = st.button("🚀 Envoyer")
        if submit_button:
            st.session_state.history.append({"role": "user", "content": input_text})
            
            # Détecter l'intention
            intention = detect_intention(input_text, intention_questions, embedding_model)
            
            if intention == "consommation":
                response = "💧 Pour consulter votre consommation, j'ai besoin de votre numéro de compte."
                st.session_state.history.append({"role": "assistant", "content": response})
                st.session_state.waiting_for = "consommation_account"
                st.rerun()
            
            elif intention == "facture":
                response = "💳 Pour consulter vos factures, j'ai besoin de votre numéro de compte."
                st.session_state.history.append({"role": "assistant", "content": response})
                st.session_state.waiting_for = "facture_account"
                st.rerun()
            
            else:
                # Utiliser RAG avec Llama via Groq pour les questions générales
                with st.spinner("🤖 Génération de la réponse avec Llama..."):
                    response = rag_response(input_text, vectorstore, llm)
                st.session_state.history.append({"role": "assistant", "content": response})
                st.rerun()
    
    # Afficher l'historique des conversations
    if st.session_state.history:
        st.markdown("---")
        st.markdown("### 💬 Historique de la conversation")
        for msg in st.session_state.history:
            if msg["role"] == "user":
                st.markdown(f"<div class='message user-message'>👤 **Vous:** {msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='message chatbot-message'>🤖 **Assistant:** {msg['content']}</div>", unsafe_allow_html=True)

# BARRE LATÉRALE

st.sidebar.title("💡 Aide & Ressources")
st.sidebar.markdown("### ❓ Questions fréquentes")

faq_questions = [
    "Comment puis-je consulter ma consommation d'eau ?",
    "Que faire en cas d'interruption de service ?",
    "Comment puis-je payer ma facture en ligne ?",
    "Comment souscrire à un nouveau service d'eau ?",
    "Comment signaler une fuite d'eau ?"
]

for i, question in enumerate(faq_questions):
    if st.sidebar.button(f"💡 {question}", key=f"faq_{i}"):
        st.session_state.history.append({"role": "user", "content": question})
        with st.spinner("🤖 Génération de la réponse..."):
            response = rag_response(question, vectorstore, llm)
        st.session_state.history.append({"role": "assistant", "content": response})
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### 📞 Contact et Support")
st.sidebar.markdown("""
🌐 **Site web :** [www.radeec.ma](https://www.radeec.ma)  
📧 **Email :** contact@radeec.ma  
📞 **Téléphone :** 0537-57-88-00  
🕓 **Horaires :** Lun - Ven : 8h30 - 16h30
""")


st.sidebar.markdown("---")

# Bouton pour effacer l'historique
if st.sidebar.button("🗑️ Effacer l'historique", type="secondary"):
    st.session_state.history = []
    st.session_state.waiting_for = None
    if 'temp_account' in st.session_state:
        del st.session_state.temp_account
    st.success("✅ Historique effacé!")
    st.rerun()

# Bouton pour recharger les modèles
if st.sidebar.button("🔄 Recharger les modèles", type="secondary"):
    st.cache_resource.clear()
    st.success("✅ Cache effacé! Rechargement...")
    st.rerun()

# Information sur le modèle
with st.sidebar.expander("ℹ️ À propos du chatbot"):
    st.markdown("""
    **Modèle:** Llama 3.3 70B  
    **Fournisseur:** Groq  
    **Technologie:** RAG (Retrieval-Augmented Generation)  
    **Embeddings:** Multilingual MiniLM  
    
    **Base de données:**
    - 3 clients de test
    - Données sur 6 mois (Juin-Novembre 2024)
    - Recherche par mois et année
    - Temps réel
    """)