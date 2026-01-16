import streamlit as st
import sys
from pathlib import Path
from agents import Runner
from dotenv import load_dotenv

load_dotenv(override=True)

# =========================
# Importer l'agent depuis agent_rag.py
# =========================

sys.path.insert(0, str(Path(__file__).parent / "scripts"))
from scripts.agent_rag import agent 

# =========================
# Configuration Streamlit
# =========================

st.set_page_config(
    page_title="Andrea Agent",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.title("💼 Mon Profil Professionnel")
st.markdown("Posez-moi des questions sur mon profil, mes projets ou mes expériences !")

# =========================
# Historique de conversation
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []

# Afficher l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =========================
# Entrée utilisateur
# =========================

if user_input := st.chat_input("Posez votre question..."):
    # Ajouter le message utilisateur à l'historique
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Générer la réponse de l'agent
    with st.chat_message("assistant"):
        with st.spinner("Andrea réfléchit..."):
            result = Runner.run_sync(agent, user_input)
            response = result.final_output

        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
    
