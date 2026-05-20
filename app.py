import streamlit as st
from llm_chain import create_rag_chain

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Med AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# LOAD CHAIN
# =========================================================
@st.cache_resource
def load_chain():
    return create_rag_chain()

chain = load_chain()

# =========================================================
# SESSION STATE
# =========================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown("""
<style>

/* GLOBAL */
.stApp {
    background: #F4F7FE;
    font-family: 'Inter', sans-serif;
}

/* Hide Streamlit Branding */
#MainMenu, header, footer {
    visibility: hidden;
}

/* Main Layout */
.block-container {
    padding-top: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: white;
    border-right: 1px solid #EAEAEA;
}

.sidebar-title {
    font-size: 28px;
    font-weight: 800;
    margin-bottom: 30px;
    color: #111827;
}

.sidebar-item {
    padding: 14px 18px;
    border-radius: 14px;
    margin-bottom: 10px;
    font-weight: 500;
    transition: 0.3s;
    cursor: pointer;
}

.sidebar-item:hover {
    background: #EEF2FF;
    color: #4F46E5;
}

/* HERO */
.hero {
    padding: 40px;
    border-radius: 30px;
    background: linear-gradient(
        135deg,
        #7C3AED,
        #6366F1,
        #06B6D4
    );

    color: white;
    margin-bottom: 30px;

    box-shadow: 0 10px 40px rgba(99,102,241,0.25);
}

.hero h1 {
    font-size: 52px;
    font-weight: 800;
    margin-bottom: 10px;
}

.hero p {
    font-size: 20px;
    opacity: 0.95;
}

/* CARDS */
.card {
    background: white;
    padding: 25px;
    border-radius: 24px;
    border: 1px solid #ECECEC;

    box-shadow: 0 6px 25px rgba(0,0,0,0.04);

    transition: 0.3s;
}

.card:hover {
    transform: translateY(-5px);
}

.card-title {
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 14px;
    color: #111827;
}

.card-text {
    color: #6B7280;
    line-height: 1.7;
}

/* CHAT AREA */
.chat-box {
    background: white;
    border-radius: 30px;
    padding: 30px;
    margin-top: 30px;

    border: 1px solid #ECECEC;

    box-shadow: 0 8px 30px rgba(0,0,0,0.04);
}

/* USER MESSAGE */
.user-msg {
    background: linear-gradient(
        135deg,
        #6366F1,
        #8B5CF6
    );

    color: white;

    padding: 14px 18px;

    border-radius: 18px 18px 4px 18px;

    width: fit-content;
    max-width: 75%;

    margin-left: auto;
    margin-top: 15px;
    margin-bottom: 15px;

    box-shadow: 0 8px 25px rgba(99,102,241,0.22);
}

/* BOT MESSAGE */
.bot-msg {
    background: #F3F4F6;

    color: #111827;

    padding: 14px 18px;

    border-radius: 18px 18px 18px 4px;

    width: fit-content;
    max-width: 75%;

    margin-top: 15px;
    margin-bottom: 15px;
}

/* INPUT */
.stChatInput input {
    border-radius: 18px !important;
    border: 1px solid #E5E7EB !important;

    padding: 16px !important;

    background: white !important;
}

/* BUTTON */
.stButton button {

    background: linear-gradient(
        135deg,
        #8B5CF6,
        #6366F1
    );

    color: white;

    border: none;

    border-radius: 14px;

    padding: 12px 18px;

    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">✨ Med AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-item">🏠 Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-item">💬 New Chat</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-item">📄 Medical Docs</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-item">📊 Analytics</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-item">⚙ Settings</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    if st.button("🗑 Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

# =========================================================
# HERO SECTION
# =========================================================
st.markdown("""
<div class="hero">
    <h1>Welcome Back 👋</h1>
    <p>Ask medical questions from your documents intelligently</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# CARDS
# =========================================================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <div class="card-title">📄 Medical Documents</div>
        <div class="card-text">
            Search uploaded PDFs using semantic embeddings and intelligent retrieval.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <div class="card-title">🧠 AI Analysis</div>
        <div class="card-text">
            Generate contextual responses powered by Mistral AI and RAG pipelines.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <div class="card-title">⚡ Smart Retrieval</div>
        <div class="card-text">
            ChromaDB enables ultra-fast vector similarity search across documents.
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# CHAT SECTION
# =========================================================
st.markdown('<div class="chat-box">', unsafe_allow_html=True)

st.subheader("💬 Medical AI Assistant")

# DISPLAY CHAT
for msg in st.session_state.messages:

    if msg["role"] == "user":

        st.markdown(
            f'<div class="user-msg">{msg["content"]}</div>',
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f'<div class="bot-msg">{msg["content"]}</div>',
            unsafe_allow_html=True
        )

# INPUT
prompt = st.chat_input("Ask your medical question...")

if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.spinner("Thinking..."):

        try:
            response = chain.invoke(prompt)

        except Exception as e:
            response = f"Error: {str(e)}"

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)