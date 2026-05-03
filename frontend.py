import streamlit as st
import requests
import time

# --- THEME & UI CONFIG ---
st.set_page_config(page_title="Project AI Portal", page_icon="🛡️", layout="wide")

# Professional Midnight Theme CSS
st.markdown("""
    <style>
    /* Main Background */
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] { background-color: #161B22 !important; border-right: 1px solid #30363D; }
    
    /* Chat Bubbles Customization */
    [data-testid="stChatMessage"] { 
        background-color: #1C2128; 
        border: 1px solid #30363D; 
        border-radius: 12px; 
        padding: 15px;
        margin-bottom: 10px;
    }
    
    /* Header Polish */
    .main-title { color: #58A6FF; font-weight: 800; font-size: 2.5rem; text-align: center; margin-bottom: 0px; }
    .subtitle { text-align: center; color: #8B949E; margin-bottom: 40px; }
    
    /* Hide Default Streamlit Menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- SESSION HANDLING ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- LOGIN VIEW ---
def login_view():
    st.markdown("<h1 class='main-title'>SECURE ACCESS</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Academic Intelligence Management System</p>", unsafe_allow_html=True)
    
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        with st.form("login_form"):
            user = st.text_input("Administrator ID")
            pwd = st.text_input("Security Key", type="password")
            if st.form_submit_button("AUTHENTICATE", use_container_width=True):
                if user == "admin" and pwd == "12345":
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Credential mismatch. Access logged.")

# --- CHAT VIEW ---
def chat_view():
    # Sidebar Metadata
    with st.sidebar:
        st.markdown("### 🛡️ SYSTEM STATUS")
        st.success("Core Engine: Online")
        st.divider()
        st.markdown("### 📊 PROJECT INFO")
        st.caption("**Student:** [Your Name]")
        st.caption("**Focus:** RAG Implementation")
        st.caption("**University:** Istanbul Computer Science")
        st.divider()
        if st.button("TERMINATE SESSION", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.messages = []
            st.rerun()

    st.markdown("<h1 class='main-title'>PROJECT INTELLIGENCE</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Llama-3.3 Optimized RAG Pipeline</p>", unsafe_allow_html=True)

    # Message History Container
    chat_container = st.container()
    with chat_container:
        for m in st.session_state.messages:
            with st.chat_message(m["role"]):
                st.markdown(m["content"])

    # Input Logic
    if prompt := st.chat_input("Input research query..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            with st.spinner("Analyzing Vector Space..."):
                try:
                    res = requests.post("http://127.0.0.1:8000/ask", json={"query": prompt}, timeout=20)
                    if res.status_code == 200:
                        full_response = res.json().get("response")
                        # High-quality streaming effect
                        typed = ""
                        for char in full_response:
                            typed += char
                            placeholder.markdown(typed + "█")
                            time.sleep(0.003)
                        placeholder.markdown(full_response)
                        st.session_state.messages.append({"role": "assistant", "content": full_response})
                except:
                    st.error("CRITICAL: Backend offline. Check FastAPI terminal.")

# --- ROUTER ---
if not st.session_state.logged_in:
    login_view()
else:
    chat_view()