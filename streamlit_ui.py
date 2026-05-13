import streamlit as st
from pathlib import Path
import os

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="File Manager",
    page_icon="🗂️",
    layout="wide",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Sora:wght@300;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Sora', sans-serif;
}

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
    min-height: 100vh;
}

/* Main title */
h1 {
    font-family: 'Sora', sans-serif;
    font-weight: 800;
    color: #e0e0ff;
    letter-spacing: -1px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.04);
    border-right: 1px solid rgba(255,255,255,0.08);
}
section[data-testid="stSidebar"] .stRadio label {
    color: #b0b8d8;
    font-family: 'Sora', sans-serif;
    font-size: 0.95rem;
}

/* Cards */
.card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 16px;
    backdrop-filter: blur(10px);
}

.card-title {
    font-family: 'Sora', sans-serif;
    font-weight: 600;
    font-size: 1.1rem;
    color: #a0aeff;
    margin-bottom: 8px;
}

/* File list items */
.file-item {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    padding: 6px 12px;
    border-radius: 8px;
    color: #c8d0f0;
    background: rgba(255,255,255,0.03);
    border-left: 3px solid #4f63ff;
    margin-bottom: 4px;
}
.folder-item {
    border-left-color: #f0a500;
}

/* Alerts */
.success-box {
    background: rgba(0,200,120,0.12);
    border: 1px solid rgba(0,200,120,0.3);
    border-radius: 10px;
    padding: 12px 18px;
    color: #00e890;
    font-size: 0.9rem;
    margin-top: 10px;
}
.error-box {
    background: rgba(255,80,80,0.1);
    border: 1px solid rgba(255,80,80,0.3);
    border-radius: 10px;
    padding: 12px 18px;
    color: #ff6b6b;
    font-size: 0.9rem;
    margin-top: 10px;
}
.info-box {
    background: rgba(80,120,255,0.1);
    border: 1px solid rgba(80,120,255,0.3);
    border-radius: 10px;
    padding: 12px 18px;
    color: #7fa0ff;
    font-size: 0.9rem;
    margin-top: 10px;
    font-family: 'JetBrains Mono', monospace;
    white-space: pre-wrap;
}

/* Streamlit widgets override */
.stTextInput > label, .stSelectbox > label, .stTextArea > label, .stRadio > label {
    color: #9090c0 !important;
    font-family: 'Sora', sans-serif;
    font-size: 0.85rem;
}
.stButton > button {
    background: linear-gradient(90deg, #4f63ff, #7a4fff);
    color: white;
    border: none;
    border-radius: 10px;
    font-family: 'Sora', sans-serif;
    font-weight: 600;
    padding: 10px 28px;
    font-size: 0.9rem;
    transition: opacity 0.2s;
}
.stButton > button:hover {
    opacity: 0.85;
    color: white;
}
</style>
""", unsafe_allow_html=True)


# ─── Helper: List files & folders ────────────────────────────────────────────
def list_items():
    p = Path('.')
    return list(p.rglob('*'))

def render_file_list():
    items = list_items()
    if not items:
        st.markdown('<div class="info-box">📂 Directory is empty.</div>', unsafe_allow_html=True)
        return
    files = [i for i in items if i.is_file()]
    folders = [i for i in items if i.is_dir()]
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card-title">📄 Files</div>', unsafe_allow_html=True)
        for f in files:
            st.markdown(f'<div class="file-item">📄 {f}</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card-title">📁 Folders</div>', unsafe_allow_html=True)
        for f in folders:
            st.markdown(f'<div class="file-item folder-item">📁 {f}</div>', unsafe_allow_html=True)

def success(msg):
    st.markdown(f'<div class="success-box">✅ {msg}</div>', unsafe_allow_html=True)

def error(msg):
    st.markdown(f'<div class="error-box">❌ {msg}</div>', unsafe_allow_html=True)


# ─── Sidebar Navigation ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🗂️ File Manager")
    st.markdown("---")
    operation = st.radio(
        "Choose Operation",
        [
            "📋 Browse Files",
            "➕ Create File",
            "📖 Read File",
            "✏️ Update File",
            "🗑️ Delete File",
            "🔤 Rename File",
            "📁 Create Folder",
            "🗑️ Delete Folder",
        ]
    )
    st.markdown("---")
    st.markdown('<small style="color:#555">Built with Streamlit · Python</small>', unsafe_allow_html=True)


# ─── Main Area ────────────────────────────────────────────────────────────────
st.markdown("# 🗂️ File Manager")
st.markdown("---")

# ══ Browse ══
if operation == "📋 Browse Files":
    st.markdown("### Current Directory Contents")
    render_file_list()

# ══ Create File ══
elif operation == "➕ Create File":
    st.markdown("### ➕ Create a New File")
    render_file_list()
    st.markdown("---")
    with st.container():
        file_name = st.text_input("File name (e.g. notes.txt)")
        content = st.text_area("File content", height=160)
        if st.button("Create File"):
            if not file_name.strip():
                error("Please enter a file name.")
            else:
                p = Path(file_name.strip())
                if p.exists():
                    error(f"'{file_name}' already exists!")
                else:
                    try:
                        p.write_text(content)
                        success(f"File '{file_name}' created successfully!")
                    except Exception as e:
                        error(str(e))

# ══ Read File ══
elif operation == "📖 Read File":
    st.markdown("### 📖 Read a File")
    render_file_list()
    st.markdown("---")
    file_name = st.text_input("File name to read")
    if st.button("Read File"):
        if not file_name.strip():
            error("Please enter a file name.")
        else:
            p = Path(file_name.strip())
            if p.exists() and p.is_file():
                content = p.read_text()
                st.markdown(f'<div class="info-box">{content if content else "(empty file)"}</div>', unsafe_allow_html=True)
            else:
                error(f"File '{file_name}' not found.")

# ══ Update File ══
elif operation == "✏️ Update File":
    st.markdown("### ✏️ Update a File")
    render_file_list()
    st.markdown("---")
    file_name = st.text_input("File name to update")
    mode = st.radio("Update mode", ["Overwrite", "Append"])
    new_content = st.text_area("New content", height=140)
    if st.button("Update File"):
        if not file_name.strip():
            error("Please enter a file name.")
        else:
            p = Path(file_name.strip())
            if p.exists() and p.is_file():
                try:
                    write_mode = 'w' if mode == "Overwrite" else 'a'
                    with open(file_name.strip(), write_mode) as f:
                        f.write(new_content)
                    success(f"File '{file_name}' updated ({mode.lower()})!")
                except Exception as e:
                    error(str(e))
            else:
                error(f"File '{file_name}' does not exist.")

# ══ Delete File ══
elif operation == "🗑️ Delete File":
    st.markdown("### 🗑️ Delete a File")
    render_file_list()
    st.markdown("---")
    file_name = st.text_input("File name to delete")
    confirm = st.checkbox("I confirm I want to delete this file permanently")
    if st.button("Delete File"):
        if not file_name.strip():
            error("Please enter a file name.")
        elif not confirm:
            error("Please check the confirmation box first.")
        else:
            p = Path(file_name.strip())
            if p.exists() and p.is_file():
                try:
                    os.remove(p)
                    success(f"File '{file_name}' deleted.")
                except Exception as e:
                    error(str(e))
            else:
                error(f"File '{file_name}' not found.")

# ══ Rename File ══
elif operation == "🔤 Rename File":
    st.markdown("### 🔤 Rename a File")
    render_file_list()
    st.markdown("---")
    old_name = st.text_input("Current file name")
    new_name = st.text_input("New file name")
    if st.button("Rename File"):
        if not old_name.strip() or not new_name.strip():
            error("Please fill in both fields.")
        else:
            p = Path(old_name.strip())
            if p.exists():
                try:
                    p.rename(new_name.strip())
                    success(f"Renamed '{old_name}' → '{new_name}'")
                except Exception as e:
                    error(str(e))
            else:
                error(f"'{old_name}' not found.")

# ══ Create Folder ══
elif operation == "📁 Create Folder":
    st.markdown("### 📁 Create a Folder")
    render_file_list()
    st.markdown("---")
    folder_name = st.text_input("Folder name")
    if st.button("Create Folder"):
        if not folder_name.strip():
            error("Please enter a folder name.")
        else:
            p = Path(folder_name.strip())
            if p.exists():
                error(f"Folder '{folder_name}' already exists!")
            else:
                try:
                    p.mkdir(parents=True)
                    success(f"Folder '{folder_name}' created!")
                except Exception as e:
                    error(str(e))

# ══ Delete Folder ══
elif operation == "🗑️ Delete Folder":
    st.markdown("### 🗑️ Delete a Folder")
    render_file_list()
    st.markdown("---")
    folder_name = st.text_input("Folder name to delete")
    confirm = st.checkbox("I confirm I want to delete this folder")
    if st.button("Delete Folder"):
        if not folder_name.strip():
            error("Please enter a folder name.")
        elif not confirm:
            error("Please check the confirmation box first.")
        else:
            p = Path(folder_name.strip())
            if p.exists() and p.is_dir():
                try:
                    p.rmdir()
                    success(f"Folder '{folder_name}' deleted.")
                except OSError:
                    error(f"Folder '{folder_name}' is not empty. Remove its contents first.")
                except Exception as e:
                    error(str(e))
            else:
                error(f"Folder '{folder_name}' not found.")