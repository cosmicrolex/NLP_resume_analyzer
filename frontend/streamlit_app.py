import streamlit as st
import requests
import os
from io import BytesIO
import json


# Configure Streamlit page
st.set_page_config(
    page_title="AI Job Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize sidebar state
def init_sidebar_state():
    if 'sidebar_state' not in st.session_state:
        st.session_state.sidebar_state = 'expanded'

def toggle_sidebar():
    if st.session_state.sidebar_state == 'expanded':
        st.session_state.sidebar_state = 'collapsed'
    else:
        st.session_state.sidebar_state = 'expanded'

# Theme toggle functionality
def init_theme():
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False

def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode

# Custom CSS for enhanced UI with working dark/light mode
def load_css():
    # Determine theme based on session state
    is_dark = st.session_state.get('dark_mode', False)
    
    # Set CSS variables based on theme
    if is_dark:
        theme_vars = """
        --primary-color: #6366f1;
        --primary-hover: #4f46e5;
        --success-color: #10b981;
        --error-color: #ef4444;
        --warning-color: #f59e0b;
        --text-primary: #f9fafb;
        --text-secondary: #d1d5db;
        --bg-primary: #111827;
        --bg-secondary: #1f2937;
        --border-color: #374151;
        --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.3), 0 1px 2px 0 rgba(0, 0, 0, 0.2);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -2px rgba(0, 0, 0, 0.2);
        """
    else:
        theme_vars = """
        --primary-color: #6366f1;
        --primary-hover: #4f46e5;
        --success-color: #10b981;
        --error-color: #ef4444;
        --warning-color: #f59e0b;
        --text-primary: #1f2937;
        --text-secondary: #6b7280;
        --bg-primary: #ffffff;
        --bg-secondary: #f9fafb;
        --border-color: #e5e7eb;
        --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        """
    
    st.markdown(f"""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Root variables for theming */
    :root {{
        {theme_vars}
    }}
    
    /* Global styles */
    .stApp {{
        font-family: 'Inter', sans-serif;
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }}
    
    /* Override Streamlit's default background */
    .main .block-container {{
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }}
    
    /* Header styling */
    .main-header {{
        background: linear-gradient(135deg, var(--primary-color), var(--primary-hover));
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        box-shadow: var(--shadow-lg);
        text-align: center;
    }}
    
    .main-header h1 {{
        color: white !important;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    
    .main-header p {{
        color: rgba(255,255,255,0.9) !important;
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        font-weight: 400;
    }}
    
    /* Theme toggle button styling */
    .theme-toggle-container {{
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 999;
    }}
    
    /* Sidebar toggle button styling */
    .sidebar-toggle-container {{
        position: fixed;
        top: 1rem;
        left: 1rem;
        z-index: 999;
    }}
    
    .stButton > button[data-testid="baseButton-secondary"] {{
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 50% !important;
        width: 50px !important;
        height: 50px !important;
        color: var(--text-primary) !important;
        font-size: 1.2rem !important;
        box-shadow: var(--shadow) !important;
        transition: all 0.3s ease !important;
        padding: 0 !important;
    }}
    
    .stButton > button[data-testid="baseButton-secondary"]:hover {{
        transform: scale(1.1) !important;
        box-shadow: var(--shadow-lg) !important;
        background: var(--bg-primary) !important;
    }}
    
    /* Card styling */
    .custom-card {{
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 1rem !important;
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
        box-shadow: var(--shadow) !important;
        transition: all 0.3s ease !important;
        color: var(--text-primary) !important;
    }}
    
    .custom-card:hover {{
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-lg) !important;
    }}
    
    /* Navigation styling */
    .nav-card {{
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 1rem !important;
        padding: 1rem !important;
        margin-bottom: 1rem !important;
        box-shadow: var(--shadow) !important;
        color: var(--text-primary) !important;
    }}
    
    /* Primary button styling */
    .stButton > button[data-testid="baseButton-primary"] {{
        background: linear-gradient(135deg, var(--primary-color), var(--primary-hover)) !important;
        color: white !important;
        border: none !important;
        border-radius: 0.75rem !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: var(--shadow) !important;
    }}
    
    .stButton > button[data-testid="baseButton-primary"]:hover {{
        transform: translateY(-1px) !important;
        box-shadow: var(--shadow-lg) !important;
    }}
    
    /* File uploader styling */
    .stFileUploader {{
        background: var(--bg-secondary) !important;
        border: 2px dashed var(--border-color) !important;
        border-radius: 1rem !important;
        padding: 2rem !important;
        text-align: center !important;
        transition: all 0.3s ease !important;
    }}
    
    .stFileUploader:hover {{
        border-color: var(--primary-color) !important;
        background: var(--bg-primary) !important;
    }}
    
    /* Text area styling */
    .stTextArea textarea {{
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 0.75rem !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
    }}
    
    /* Selectbox styling */
    .stSelectbox > div > div {{
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-primary) !important;
    }}
    
    /* Radio button styling */
    .stRadio > div {{
        background: var(--bg-secondary) !important;
        border-radius: 0.5rem !important;
        padding: 0.5rem !important;
    }}
    
    /* Metric styling */
    .metric-card {{
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 1rem !important;
        padding: 1.5rem !important;
        text-align: center !important;
        box-shadow: var(--shadow) !important;
        transition: all 0.3s ease !important;
    }}
    
    .metric-card:hover {{
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-lg) !important;
    }}
    
    .metric-value {{
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: var(--primary-color) !important;
        margin-bottom: 0.5rem !important;
    }}
    
    .metric-label {{
        font-size: 0.9rem !important;
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
    }}
    
    /* Success/Error styling */
    .stSuccess {{
        background: rgba(16, 185, 129, 0.1) !important;
        border: 1px solid var(--success-color) !important;
        border-radius: 0.75rem !important;
        color: var(--success-color) !important;
    }}
    
    .stError {{
        background: rgba(239, 68, 68, 0.1) !important;
        border: 1px solid var(--error-color) !important;
        border-radius: 0.75rem !important;
        color: var(--error-color) !important;
    }}
    
    .stInfo {{
        background: rgba(99, 102, 241, 0.1) !important;
        border: 1px solid var(--primary-color) !important;
        border-radius: 0.75rem !important;
        color: var(--primary-color) !important;
    }}
    
    .stWarning {{
        background: rgba(245, 158, 11, 0.1) !important;
        border: 1px solid var(--warning-color) !important;
        border-radius: 0.75rem !important;
        color: var(--warning-color) !important;
    }}
    
    /* Sidebar styling */
    .css-1d391kg, .css-1cypcdb {{
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--border-color) !important;
    }}
    
    /* Dataframe styling */
    .stDataFrame {{
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 0.5rem !important;
    }}
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {{
        background: var(--bg-secondary) !important;
        border-radius: 0.5rem !important;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        color: var(--text-secondary) !important;
        background: transparent !important;
    }}
    
    .stTabs [aria-selected="true"] {{
        color: var(--primary-color) !important;
        background: var(--bg-primary) !important;
    }}
    
    /* Responsive design */
    @media (max-width: 768px) {{
        .main-header h1 {{
            font-size: 2rem !important;
        }}
        
        .main-header p {{
            font-size: 1rem !important;
        }}
        
        .custom-card {{
            padding: 1rem !important;
            margin: 0.5rem 0 !important;
        }}
        
        .theme-toggle-container {{
            top: 0.5rem !important;
            right: 0.5rem !important;
        }}
        
        .stButton > button[data-testid="baseButton-secondary"] {{
            width: 45px !important;
            height: 45px !important;
        }}
    }}
    
    /* Hide Streamlit branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: var(--bg-secondary);
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: var(--border-color);
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: var(--text-secondary);
    }}
    </style>
    """, unsafe_allow_html=True)

# API Base URL - Use local backend when running in same container
# Check if we're running in production (Render) or locally
if os.getenv("RENDER"):
    # In production, both services run in the same container
    API_BASE_URL = "http://localhost:8000"
else:
    # For local development, try environment variable or default to localhost
    API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

# Fallback URLs to try if the primary URL fails
FALLBACK_URLS = [
    "https://ai-job-assistant.onrender.com",
    "https://nlp-ai-resume-analysis.onrender.com", 
    "https://ai-powered-job-assistant.onrender.com"
]

def display_detailed_error(error_info, context="API Request"):
    """Display detailed error information in an expandable format"""
    st.error(f"❌ {context} Failed")
    
    with st.expander("🔍 **Click to view detailed error information**", expanded=False):
        st.markdown("### 🚨 Error Details")
        
        # Basic error info
        if isinstance(error_info, dict):
            if "error_type" in error_info:
                st.markdown(f"**Error Type:** `{error_info['error_type']}`")
            if "error_message" in error_info:
                st.markdown(f"**Error Message:** {error_info['error_message']}")
            if "status_code" in error_info:
                st.markdown(f"**HTTP Status Code:** `{error_info['status_code']}`")
            if "endpoint" in error_info:
                st.markdown(f"**API Endpoint:** `{error_info['endpoint']}`")
        else:
            st.markdown(f"**Error Message:** {str(error_info)}")
        
        # Additional debugging info
        st.markdown("### 🔧 Debugging Information")
        st.markdown(f"**API Base URL:** `{API_BASE_URL}`")
        st.markdown(f"**Timestamp:** {st.session_state.get('last_error_time', 'Unknown')}")
        
        # Raw error details
        if isinstance(error_info, dict) and "raw_response" in error_info:
            st.markdown("### 📄 Raw Response")
            st.code(error_info["raw_response"], language="json")
        
        # Troubleshooting suggestions
        st.markdown("### 💡 Troubleshooting Suggestions")
        if isinstance(error_info, dict):
            if error_info.get("status_code") == 500:
                st.markdown("""
                - **Server Error**: The backend service encountered an internal error
                - Check if all required environment variables are set (GROQ_API_KEY, etc.)
                - Verify that the spaCy model is properly installed
                - Check backend logs for detailed error information
                """)
            elif error_info.get("status_code") == 404:
                st.markdown("""
                - **Endpoint Not Found**: The API endpoint may be incorrect
                - Verify the API base URL is correct
                - Check if the backend service is running
                """)
            elif error_info.get("status_code") == 422:
                st.markdown("""
                - **Validation Error**: The request data format is incorrect
                - Check if the uploaded file is a valid PDF
                - Verify all required fields are provided
                """)
            elif "Connection" in str(error_info.get("error_type", "")):
                st.markdown("""
                - **Connection Error**: Cannot reach the backend service
                - Check your internet connection
                - Verify the API base URL is correct and accessible
                - The backend service might be down or restarting
                """)
            elif "JSON" in str(error_info.get("error_type", "")):
                st.markdown("""
                - **JSON Parse Error**: The server response is not valid JSON
                - This usually indicates a server error or timeout
                - The backend might be returning HTML error pages instead of JSON
                - Check if the backend service is properly configured
                """)
        else:
            st.markdown("""
            - Check your internet connection
            - Verify the backend service is running
            - Try refreshing the page and attempting again
            - Contact support if the issue persists
            """)

def make_api_request(method, endpoint, files=None, data=None, timeout=30):
    """Make API request with comprehensive error handling"""
    import time
    
    # Store timestamp for debugging
    st.session_state.last_error_time = time.strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        url = f"{API_BASE_URL}{endpoint}"
        
        if method.upper() == "POST":
            response = requests.post(url, files=files, data=data, timeout=timeout)
        elif method.upper() == "GET":
            response = requests.get(url, timeout=timeout)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        # Check if response is successful
        if response.status_code == 200:
            try:
                return {"success": True, "data": response.json()}
            except json.JSONDecodeError as e:
                return {
                    "success": False,
                    "error_type": "JSON Decode Error",
                    "error_message": f"Server returned invalid JSON: {str(e)}",
                    "status_code": response.status_code,
                    "endpoint": endpoint,
                    "raw_response": response.text[:1000] + "..." if len(response.text) > 1000 else response.text
                }
        else:
            # Try to get error message from response
            try:
                error_data = response.json()
                error_message = error_data.get("error", f"HTTP {response.status_code} Error")
            except json.JSONDecodeError:
                error_message = f"HTTP {response.status_code}: {response.reason}"
            
            return {
                "success": False,
                "error_type": f"HTTP {response.status_code} Error",
                "error_message": error_message,
                "status_code": response.status_code,
                "endpoint": endpoint,
                "raw_response": response.text[:1000] + "..." if len(response.text) > 1000 else response.text
            }
    
    except requests.exceptions.ConnectionError as e:
        return {
            "success": False,
            "error_type": "Connection Error",
            "error_message": f"Cannot connect to backend service: {str(e)}",
            "endpoint": endpoint,
            "raw_response": str(e)
        }
    
    except requests.exceptions.Timeout as e:
        return {
            "success": False,
            "error_type": "Timeout Error",
            "error_message": f"Request timed out after {timeout} seconds: {str(e)}",
            "endpoint": endpoint,
            "raw_response": str(e)
        }
    
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error_type": "Request Error",
            "error_message": f"Request failed: {str(e)}",
            "endpoint": endpoint,
            "raw_response": str(e)
        }
    
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error_type": "JSON Decode Error",
            "error_message": f"Failed to parse response as JSON: {str(e)}",
            "endpoint": endpoint,
            "raw_response": "Invalid JSON response"
        }
    
    except Exception as e:
        return {
            "success": False,
            "error_type": "Unexpected Error",
            "error_message": f"An unexpected error occurred: {str(e)}",
            "endpoint": endpoint,
            "raw_response": str(e)
        }

def test_backend_connection():
    """Test backend connection and display status"""
    st.markdown("### 🔗 Backend Connection Status")
    
    global API_BASE_URL
    
    with st.spinner("Testing backend connection..."):
        # Try current API_BASE_URL first
        result = make_api_request("GET", "/health")
        
        if result["success"]:
            st.success(f"✅ Backend connection successful!")
            st.info(f"**Connected to:** `{API_BASE_URL}`")
            health_data = result["data"]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Status", health_data.get("status", "Unknown"))
            with col2:
                st.metric("Version", health_data.get("version", "Unknown"))
            with col3:
                endpoints = health_data.get("endpoints", [])
                st.metric("Endpoints", len(endpoints))
            
            with st.expander("Available Endpoints"):
                for endpoint in endpoints:
                    st.code(endpoint)
        else:
            st.error(f"❌ Backend connection failed for: `{API_BASE_URL}`")
            
            # Try alternative URLs
            st.markdown("### 🔄 Trying Alternative URLs...")
            
            working_url = None
            for url in FALLBACK_URLS:
                if url == API_BASE_URL:
                    continue  # Skip the one we already tried
                
                st.info(f"Testing: `{url}`")
                
                # Temporarily change API_BASE_URL for testing
                original_url = API_BASE_URL
                API_BASE_URL = url
                
                test_result = make_api_request("GET", "/health")
                
                if test_result["success"]:
                    st.success(f"✅ Found working URL: `{url}`")
                    working_url = url
                    health_data = test_result["data"]
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Status", health_data.get("status", "Unknown"))
                    with col2:
                        st.metric("Version", health_data.get("version", "Unknown"))
                    with col3:
                        endpoints = health_data.get("endpoints", [])
                        st.metric("Endpoints", len(endpoints))
                    
                    with st.expander("Available Endpoints"):
                        for endpoint in endpoints:
                            st.code(endpoint)
                    break
                else:
                    st.error(f"❌ Failed: `{url}`")
                    # Restore original URL for next iteration
                    API_BASE_URL = original_url
            
            if not working_url:
                # Restore original URL if no working URL found
                API_BASE_URL = original_url
                st.error("❌ No working backend URL found!")
                
                st.markdown("### 🔍 Debugging Information")
                st.markdown("**Tested URLs:**")
                for url in FALLBACK_URLS:
                    st.code(url)
                
                st.markdown("### 💡 Possible Solutions")
                st.markdown("""
                1. **Check Render Dashboard**: Verify your service is running
                2. **Check Service Name**: Ensure the URL matches your Render service name
                3. **Check Deployment Status**: Service might be starting up or crashed
                4. **Check Logs**: Look at Render logs for startup errors
                5. **Try Manual URL**: Visit the URL directly in your browser
                """)
            else:
                st.info(f"**Updated API Base URL to:** `{working_url}`")



def main():
    # Initialize theme and sidebar state
    init_theme()
    init_sidebar_state()
    load_css()
    
    # Theme toggle button in fixed position
    st.markdown('<div class="theme-toggle-container">', unsafe_allow_html=True)
    theme_icon = "🌙" if not st.session_state.dark_mode else "☀️"
    if st.button(theme_icon, key="theme_toggle", help="Toggle dark/light mode", type="secondary"):
        toggle_theme()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Sidebar toggle button - only show when sidebar is collapsed
    if st.session_state.sidebar_state == 'collapsed':
        st.markdown('<div class="sidebar-toggle-container">', unsafe_allow_html=True)
        if st.button("📋", key="sidebar_toggle", help="Show sidebar", type="secondary"):
            st.session_state.sidebar_state = 'expanded'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 AI-Powered Job Assistant</h1>
        <p>Intelligent resume analysis and job matching powered by machine learning and Groq LLM</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown('<div class="nav-card">', unsafe_allow_html=True)
        st.markdown("### 🧭 Navigation")
        option = st.selectbox(
            "Choose Analysis Type:",
            ["📄 Resume Analysis", "💼 Job Description Analysis", "🎯 Resume-Job Matching"],
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Feature highlights
        st.markdown('<div class="nav-card">', unsafe_allow_html=True)
        st.markdown("### ✨ Features")
        st.markdown("""
        - **AI-Powered Analysis** using TF-IDF
        - **Smart Keyword Extraction**
        - **Similarity Scoring**
        - **PDF Text Extraction**
        - **Real-time Processing**
        - **LLM Strengths/Weaknesses Analysis**
        - **LLM Job Fit Assessment**
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Theme status
        st.markdown('<div class="nav-card">', unsafe_allow_html=True)
        theme_status = "🌙 Dark Mode" if st.session_state.dark_mode else "☀️ Light Mode"
        st.markdown(f"**Current Theme:** {theme_status}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Backend connection test
        st.markdown('<div class="nav-card">', unsafe_allow_html=True)
        st.markdown("### 🔧 System Status")
        if st.button("🔍 Test Backend Connection", use_container_width=True):
            test_backend_connection()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Route to appropriate page
    if option == "📄 Resume Analysis":
        resume_analysis_page()
    elif option == "💼 Job Description Analysis":
        job_description_analysis_page()
    elif option == "🎯 Resume-Job Matching":
        matching_page()

def resume_analysis_page():
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("## 📄 Resume Analysis")
    st.markdown("Upload your resume in PDF format to extract key skills and analyze strengths/weaknesses using Groq's LLM and TF-IDF algorithms.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "📎 Choose your resume (PDF format)",
            type="pdf",
            help="Upload your resume in PDF format for AI-powered analysis"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("### 📊 What you'll get:")
        st.markdown("""
        - **Top Keywords** extracted from your resume
        - **TF-IDF Scores** for each term
        - **Skills Analysis** and importance ranking
        - **Text Preview** of extracted content
        - **Strengths & Weaknesses** via LLM
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    if uploaded_file is not None:
        col1, col2 = st.columns(2)
        with col2:
            if st.button("🚀 Analyze Resume", type="primary", use_container_width=True):
                with st.spinner("🔍 Analyzing your resume with AI..."):
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    result = make_api_request("POST", "/analyze-resume/", files=files)
                    
                    if result["success"]:
                        data = result["data"]
                        st.success("✅ Resume analyzed successfully!")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                            st.markdown("### 📊 Key Skills & Keywords")
                            if "tfidf_analysis" in data and data["tfidf_analysis"]:
                                keywords_df = []
                                for keyword in data["tfidf_analysis"]:
                                    keywords_df.append({
                                        "🔑 Keyword": keyword["term"],
                                        "📈 TF-IDF Score": f"{keyword['score']:.4f}"
                                    })
                                st.dataframe(keywords_df, use_container_width=True, hide_index=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                            st.markdown("### 📝 Extracted Text Preview")
                            extracted_text = data.get("extracted_text", "")
                            preview_text = extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text
                            st.text_area("Extracted Text Preview", preview_text, height=300, label_visibility="collapsed")
                            st.markdown('</div>', unsafe_allow_html=True)
                        
                        # LLM Strengths and Weaknesses
                        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                        st.markdown("### 💪 Strengths & Weaknesses (Groq LLM)")
                        if "llm_strengths_weaknesses" in data and data["llm_strengths_weaknesses"]:
                            try:
                                sw = data["llm_strengths_weaknesses"]
                                if isinstance(sw, str):
                                    sw = json.loads(sw)

                                if isinstance(sw, dict):
                                    st.markdown("**Strengths:**")
                                    for s in sw.get("strengths", []):
                                        st.markdown(f"- {s}")
                                    st.markdown("**Weaknesses:**")
                                    for w in sw.get("weaknesses", []):
                                        st.markdown(f"- {w}")

                                    if "raw_response" in sw:
                                        with st.expander("🔍 Raw AI Response"):
                                            st.text(sw["raw_response"])
                                else:
                                    st.write(sw)
                            except (json.JSONDecodeError, TypeError) as e:
                                st.error(f"Error parsing LLM response: {str(e)}")
                                st.write(data["llm_strengths_weaknesses"])
                        else:
                            st.warning("⚠️ No LLM analysis available. Check GROQ_API_KEY.")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    else:
                        display_detailed_error(result, "Resume Analysis")  

def job_description_analysis_page():
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("## 💼 Job Description Analysis")
    st.markdown("Analyze job requirements and extract key skills using AI-powered text processing.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input method selection
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        input_method = st.radio(
            "Choose input method:",
            ["📝 Text Input", "📄 PDF Upload"],
            horizontal=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    job_description = ""
    uploaded_jd_file = None
    
    if input_method == "📝 Text Input":
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        job_description = st.text_area(
            "📋 Job Description",
            height=200,
            placeholder="Paste the complete job description here...",
            help="Copy and paste the job description text for analysis"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif input_method == "📄 PDF Upload":
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        uploaded_jd_file = st.file_uploader(
            "📎 Upload Job Description PDF",
            type="pdf",
            help="Upload job description in PDF format",
            key="jd_pdf_uploader"
        )
        if uploaded_jd_file is not None:
            st.success(f"✅ File uploaded: {uploaded_jd_file.name}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Analysis button and logic
    can_analyze = (input_method == "📝 Text Input" and job_description.strip()) or \
                  (input_method == "📄 PDF Upload" and uploaded_jd_file is not None)
    
    if can_analyze:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔍 Analyze Job Description", type="primary", use_container_width=True):
                with st.spinner("🤖 AI is analyzing the job description..."):
                    try:
                        if input_method == "📝 Text Input":
                            data = {"job_description": job_description}
                            response = requests.post(f"{API_BASE_URL}/analyze-job-description/", data=data)
                        else:
                            files = {"file": (uploaded_jd_file.name, uploaded_jd_file.getvalue(), "application/pdf")}
                            response = requests.post(f"{API_BASE_URL}/analyze-job-description-pdf/", files=files)
                        
                        if response.status_code == 200:
                            result = response.json()
                            
                            st.success("✅ Job description analyzed successfully!")
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                                st.markdown("### 🎯 Key Requirements")
                                if "tfidf_analysis" in result and "top_keywords" in result["tfidf_analysis"]:
                                    keywords_df = []
                                    for keyword in result["tfidf_analysis"]["top_keywords"]:
                                        keywords_df.append({
                                            "💼 Requirement": keyword["term"],
                                            "⭐ Importance": f"{keyword['score']:.4f}"
                                        })
                                    st.dataframe(keywords_df, use_container_width=True, hide_index=True)
                                st.markdown('</div>', unsafe_allow_html=True)
                            
                            with col2:
                                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                                st.markdown("### 📈 Analysis Summary")
                                
                                # Metrics
                                total_keywords = len(result['tfidf_analysis']['top_keywords'])
                                st.markdown(f"""
                                <div class="metric-card">
                                    <div class="metric-value">{total_keywords}</div>
                                    <div class="metric-label">Keywords Analyzed</div>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Preview
                                preview_text = (job_description if input_method == "📝 Text Input" 
                                              else result.get("extracted_text", ""))[:300]
                                st.text_area("Job Description Preview", 
                                           preview_text + "..." if len(preview_text) == 300 else preview_text,
                                           height=150, label_visibility="collapsed")
                                st.markdown('</div>', unsafe_allow_html=True)
                        
                        else:
                            st.error(f"❌ Error: {response.json().get('error', 'Unknown error')}")
                            
                    except Exception as e:
                        st.error(f"❌ Connection error: {str(e)}")
                        

def matching_page():
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("## 🎯 Resume-Job Matching")
    st.markdown("Upload your resume and job description to get AI-powered compatibility analysis with detailed similarity scoring and Groq LLM fit assessment.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("### 📄 Upload Resume")
        uploaded_file = st.file_uploader(
            "Choose your resume (PDF)",
            type="pdf",
            help="Upload your resume in PDF format",
            key="resume_uploader"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("### 💼 Job Description")
        
        jd_input_method = st.radio(
            "Input method:",
            ["📝 Text", "📄 PDF"],
            horizontal=True,
            key="matching_jd_method"
        )
        
        job_description = ""
        uploaded_jd_file = None
        
        if jd_input_method == "📝 Text":
            job_description = st.text_area(
                "Paste job description",
                height=150,
                placeholder="Paste the job description here...",
                key="matching_jd_text"
            )
        else:
            uploaded_jd_file = st.file_uploader(
                "Upload job description PDF",
                type="pdf",
                key="matching_jd_pdf"
            )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Check if both inputs are provided
    resume_ready = uploaded_file is not None
    jd_ready = (jd_input_method == "📝 Text" and job_description.strip()) or \
              (jd_input_method == "📄 PDF" and uploaded_jd_file is not None)
    
    if resume_ready and jd_ready:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Analyze Compatibility", type="primary", use_container_width=True):
                with st.spinner("🤖 AI is analyzing compatibility..."):
                    try:
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                        
                        if jd_input_method == "📝 Text":
                            data = {"job_description": job_description}
                            response = requests.post(f"{API_BASE_URL}/match-resume-job/", files=files, data=data)
                        else:
                            files["jd_file"] = (uploaded_jd_file.name, uploaded_jd_file.getvalue(), "application/pdf")
                            response = requests.post(f"{API_BASE_URL}/match-resume-job-pdf/", files=files)
                        
                        if response.status_code == 200:
                            result = response.json()
                            analysis = result.get("analysis", {})
                            
                            st.success("✅ Compatibility analysis completed!")
                            
                            # Similarity Score Display
                            if "similarity_analysis" in analysis:
                                similarity = analysis["similarity_analysis"]
                                
                                col1, col2, col3 = st.columns(3)
                                
                                with col1:
                                    score = similarity.get("similarity_score", 0)
                                    st.markdown(f"""
                                    <div class="metric-card">
                                        <div class="metric-value">{score:.1%}</div>
                                        <div class="metric-label">Similarity Score</div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                
                                with col2:
                                    quality = similarity.get("match_quality", "Unknown")
                                    quality_color = {"Excellent Match": "#10b981", "Good Match": "#3b82f6", 
                                                   "Fair Match": "#f59e0b", "Poor Match": "#ef4444"}.get(quality, "#6b7280")
                                    st.markdown(f"""
                                    <div class="metric-card">
                                        <div class="metric-value" style="color: {quality_color};">{quality}</div>
                                        <div class="metric-label">Match Quality</div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                
                                with col3:
                                    common_count = len(similarity.get("common_keywords", []))
                                    st.markdown(f"""
                                    <div class="metric-card">
                                        <div class="metric-value">{common_count}</div>
                                        <div class="metric-label">Common Keywords</div>
                                    </div>
                                    """, unsafe_allow_html=True)
                            
                            # Detailed Analysis Tabs
                            tab1, tab2, tab3, tab4 = st.tabs(["🎯 Common Keywords", "📄 Resume Analysis", "💼 Job Analysis", "🤝 Fit Assessment"])
                            
                            with tab1:
                                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                                if "similarity_analysis" in analysis and "common_keywords" in analysis["similarity_analysis"]:
                                    common_keywords = analysis["similarity_analysis"]["common_keywords"]
                                    if common_keywords:
                                        keywords_df = []
                                        for kw in common_keywords:
                                            keywords_df.append({
                                                "🔑 Term": kw["term"],
                                                "📄 Resume Score": f"{kw['resume_score']:.4f}",
                                                "💼 Job Score": f"{kw['job_desc_score']:.4f}",
                                                "⭐ Combined": f"{kw['combined_importance']:.4f}"
                                            })
                                        st.dataframe(keywords_df, use_container_width=True, hide_index=True)
                                    else:
                                        st.warning("⚠️ No common keywords found between resume and job description")
                                st.markdown('</div>', unsafe_allow_html=True)
                            
                            with tab2:
                                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                                st.markdown("### 📄 Resume Key Skills")
                                if "resume_analysis" in analysis:
                                    resume_keywords = analysis["resume_analysis"].get("top_keywords", [])
                                    if resume_keywords:
                                        for i, kw in enumerate(resume_keywords[:10], 1):
                                            st.markdown(f"**{i}.** {kw['term']} - *Score: {kw['score']:.4f}*")
                                st.markdown('</div>', unsafe_allow_html=True)
                            
                            with tab3:
                                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                                st.markdown("### 💼 Job Requirements")
                                if "job_description_analysis" in analysis:
                                    job_keywords = analysis["job_description_analysis"].get("top_keywords", [])
                                    if job_keywords:
                                        for i, kw in enumerate(job_keywords[:10], 1):
                                            st.markdown(f"**{i}.** {kw['term']} - *Score: {kw['score']:.4f}*")
                                st.markdown('</div>', unsafe_allow_html=True)
                            
                            with tab4:
                                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                                st.markdown("### 🤝 Groq LLM Fit Assessment")
                                if "llm_fit_assessment" in result and result["llm_fit_assessment"]:
                                    try:
                                        fit = result["llm_fit_assessment"]
                                        # Check if it's already a dictionary or needs JSON parsing
                                        if isinstance(fit, str):
                                            fit = json.loads(fit)

                                        if isinstance(fit, dict):
                                            st.markdown(f"**Overall Fit:** {fit.get('fit_percentage', 'N/A')}%")
                                            st.markdown("**Reasons for Fit:**")
                                            for r in fit.get("reasons", []):
                                                st.markdown(f"- {r}")
                                            st.markdown("**Suggestions for Improvement:**")
                                            for s in fit.get("suggestions", []):
                                                st.markdown(f"- {s}")

                                            # Show raw response if available for debugging
                                            if "raw_response" in fit:
                                                with st.expander("🔍 Raw AI Response"):
                                                    st.text(fit["raw_response"])
                                        else:
                                            st.write(fit)  # Fallback display
                                    except (json.JSONDecodeError, TypeError) as e:
                                        st.error(f"Error parsing LLM response: {str(e)}")
                                        st.write(result["llm_fit_assessment"])  # Fallback raw display
                                else:
                                    st.warning("⚠️ No LLM fit assessment available. Check GROQ_API_KEY.")
                                st.markdown('</div>', unsafe_allow_html=True)
                        
                        else:
                            st.error(f"❌ Error: {response.json().get('error', 'Unknown error')}")
                            
                    except Exception as e:
                        st.error(f"❌ Connection error: {str(e)}")
    
    else:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        if not resume_ready:
            st.info("📄 Please upload your resume to continue")
        elif not jd_ready:
            st.info("💼 Please provide a job description to continue")
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()