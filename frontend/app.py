import streamlit as st
import requests
import json
import os

API_BASE = os.getenv("API_BASE", "http://localhost:8000/api/v1")

# ─────── Page Config ──────────────────────
st.set_page_config(
    page_title="IntelliDocs",
    page_icon="🧠",
    layout="wide"
)

# ─────── Header ──────────────────────
st.title("🧠 IntelliDocs")
st.caption("Universal Document Intelligence Platform")
st.divider()

# ─────── Sidebar - System Health ───────────────────
with st.sidebar:
    st.header("⚙️ System Status")
    
    try:
        health = requests.get(f"{API_BASE}/health/detailed", timeout=3)
        if health.status_code == 200:
            data = health.json()
            st.success("✅ API Online")
            
            cache = data["components"]["cache"]
            if cache["status"] == "connected":
                st.success("✅ Redis Connected")
                st.metric("Cache Queries", cache["total_cached_queries"])
                st.metric("Memory Used", cache["memory_used"])
            else:
                st.warning("⚠️ Redis Offline")
        else:
            st.error("❌ API Offline")
    except:
        st.error("❌ Cannot reach API")
        
    st.divider()
    st.header("📖 How To Use")
    st.markdown("""
    1. Upload a document
    2. System auto-detects domain
    3. Ask any question about it
    4. Get instant AI answers            
    """)
    
# ────── Main Layout - Two Columns ──────────
left, right = st.columns([1, 1])

# ─────── Left Column - Upload ──────────
with left:
    st.subheader("📄 Upload Document")
    
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["txt", "pdf"],
        help="Supports Legal, Medical, Corporate, and Code documents"
    )
    
    if uploaded_file is not None:
        if st.button("🚀 Process Document",use_container_width=True):
            with st.spinner("Processing document..."):
                try:
                    files = {"file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type
                    )}
                    response = requests.post(
                        f"{API_BASE}/upload",
                        files=files,
                        timeout=60
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        meta = result["metadata"]
                        
                        st.success("✅ Document processed!")
                        
                        # Show what was detected
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Domain", meta["domain"].upper())
                        col2.metric("Chunks", meta["num_chunks"])
                        col3.metric("Time", f"{meta['processing_time_seconds']}s")
                        
                        # Store domain in session for query tab
                        st.session_state["domain"] = meta["domain"]
                        st.session_state["filename"] = meta["filename"]
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                
# ────── Right Column - Query ───────────────
with right:
    st.subheader("💬 Ask A Question")
    
    # Domain Selector - auto-dilled after upload
    domain = st.selectbox(
        "Document Domain",
        ["corporate", "legal", "medical", "code"],
        index=["corporate", "legal", "medical", "code"].index(
            st.session_state.get("domain", "corporate")
        )
    )
    
    question = st.text_area(
        "Your Question",
        placeholder="Whats is the leave policy?\nWhat are the termination clauses?\nWhat was the sample size?",
        height=100
    )
    
    if st.button("🔍 get Answer", use_container_width=True):
        if not question.strip():
            st.warning("Please enter a question")
        else:
            with st.spinner("Thinking..."):
                try:
                    response = requests.post(
                        f"{API_BASE}/query",
                        json={
                            "question": question,
                            "domain": domain
                        },
                        timeout=60
                    )
                    
                    if response.status_code == 200:
                        result = response.json()["result"]
                        
                        # Cache hit badge
                        if result.get("cache_hit"):
                            st.success("⚡ Instant answer (from cache)")
                        else:
                            st.info("🔄️ Fresh answer generated")
                            
                        # The answer
                        st.markdown("### Answer")
                        st.markdown(result["answer"])
                        
                        # stats
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Domain", result["domain"].upper())
                        col2.metric("Sources Used", result["source_chunks"])
                        col3.metric("Response Time", f"{result['respoonse_time_seconds']}s")
                        
                    else:
                        st.error(f"Query failed: {response.json()['detail']}")
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    
# ────── Bottom - Query History ────────────────────
st.divider()
st.subheader("📊 Session History")

if "history" not in st.session_state:
    st.session_state["history"] = []
    
# Add latest query to history
if "result" in dir() and question:
    st.session_state["history"].append({
        "question": question,
        "domain": domain,
        "cache_hit": result.get("cache_hit", False)
    })
    
if st.session_state["history"]:
    for i, item in enumerate(reversed(st.session_state["history"][-5:])):
        with st.expander(f"Q: {item['question'][:60]}..."):
            st.write(f"**Domain:** {item['domain'].upper()}")
            st.write(f"**Cache Hit:** {'⚡ Yes' if item['cache_hit'] else '🔄️ No'}")
else:
    st.caption("No queries yet in this session")