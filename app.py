import streamlit as st
from database import PromptDatabase
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="LLM Prompt Repository for Social Science",
    page_icon="🔬",
    layout="wide"
)

# ============================================
# CACHING EXAMPLES - This is the key difference!
# ============================================

@st.cache_resource
def get_database():
    """
    Cache the database connection
    This runs ONCE and is reused across all reruns
    Without this, you'd create a new DB connection every time!
    """
    print("🔴 CREATING DATABASE CONNECTION")  # You'll see this only ONCE
    return PromptDatabase()

@st.cache_data(ttl=60)  # Cache for 60 seconds
def load_all_prompts(_db):
    """
    Cache the prompts data
    This prevents re-querying the database on every interaction
    Note: _db with underscore tells Streamlit not to hash this parameter
    """
    print("🔴 LOADING PROMPTS FROM DATABASE")  # See how often this runs!
    return _db.get_all_prompts()

@st.cache_data(ttl=60)
def load_categories(_db):
    """Cache categories list"""
    print("🔴 LOADING CATEGORIES FROM DATABASE")
    return _db.get_categories()

@st.cache_data(ttl=10)
def search_prompts(_db, query):
    """Cache search results (shorter TTL since it changes more often)"""
    print(f"🔴 SEARCHING FOR: {query}")
    return _db.search_prompts(query)

# ============================================
# Initialize (using cached database)
# ============================================
db = get_database()

# Auto-seed database if empty
if db.get_prompt_count() == 0:
    from seed_data import seed_database
    seed_database()
    # Clear cache after seeding
    st.cache_data.clear()

# Custom CSS for better styling
st.markdown("""
    <style>
    .prompt-card {
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin: 10px 0;
        background-color: #f9f9f9;
    }
    .prompt-title {
        font-size: 20px;
        font-weight: bold;
        color: #1f77b4;
    }
    .prompt-category {
        display: inline-block;
        padding: 5px 10px;
        background-color: #e1f5ff;
        border-radius: 5px;
        font-size: 12px;
        margin: 5px 5px 5px 0;
    }
    .prompt-tag {
        display: inline-block;
        padding: 3px 8px;
        background-color: #f0f0f0;
        border-radius: 3px;
        font-size: 11px;
        margin: 2px;
    }
    .stButton>button {
        width: 100%;
    }
    .debug-info {
        background-color: #fff3cd;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ffc107;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================
# DEBUG PANEL - Shows you the re-run behavior!
# ============================================
if 'run_count' not in st.session_state:
    st.session_state.run_count = 0

st.session_state.run_count += 1

with st.expander("🐛 DEBUG INFO - See How Streamlit Re-runs!", expanded=False):
    st.markdown(f"""
    <div class='debug-info'>
    <h4>Script Re-run Counter: {st.session_state.run_count}</h4>
    <p><strong>What this means:</strong> Every time you click a button, type in search, or interact with ANYTHING, 
    this entire Python script runs from top to bottom again!</p>
    
    <p><strong>Current time:</strong> {datetime.now().strftime('%H:%M:%S.%f')[:-3]}</p>
    
    <p><strong>Watch your terminal/console:</strong> You'll see 🔴 messages showing when cached functions actually execute vs when they use cached data.</p>
    
    <p><strong>Try this:</strong> Click around and watch this counter increase. Then check your terminal - 
    you'll notice the database queries (🔴 messages) DON'T run every time because of caching!</p>
    </div>
    """, unsafe_allow_html=True)

# Title and description
st.title("🔬 LLM Prompt Repository for Social Science Research")
st.markdown("""
Welcome to the prompt repository! Browse prompts shared by the community or add your own.
All prompts are designed to help social scientists leverage LLMs in their research.
""")

# Sidebar for navigation and filtering
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Browse Prompts", "Add New Prompt", "About", "🐛 Cache Demo"])

# Get statistics (using cached functions)
total_prompts = db.get_prompt_count()
categories = load_categories(db)

st.sidebar.markdown("---")
st.sidebar.metric("Total Prompts", total_prompts)
st.sidebar.metric("Script Re-runs", st.session_state.run_count)

# ============================================
# CACHE DEMO PAGE - New page to show caching!
# ============================================
if page == "🐛 Cache Demo":
    st.header("🐛 Understanding Streamlit's Re-run Behavior")
    
    st.markdown("""
    ## What Happens on Every Interaction?
    
    Streamlit re-runs the **ENTIRE** Python script from top to bottom when you:
    - Click a button
    - Type in a text input
    - Move a slider
    - Select from a dropdown
    - Literally ANY interaction!
    """)
    
    st.markdown("---")
    
    st.subheader("🧪 Experiment 1: See the Re-runs")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Click Me!"):
            st.success(f"Button clicked at {datetime.now().strftime('%H:%M:%S')}")
    
    with col2:
        st.info(f"This script has run {st.session_state.run_count} times since you opened the page!")
    
    st.markdown("---")
    
    st.subheader("🧪 Experiment 2: Caching vs No Caching")
    
    st.markdown("""
    **Open your terminal/console** where you ran `streamlit run app_optimized.py` and watch for 🔴 messages!
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**❌ WITHOUT Caching:**")
        if st.button("Load Prompts (No Cache)"):
            start = time.time()
            # Direct DB call - no cache
            prompts_no_cache = db.get_all_prompts()
            end = time.time()
            st.warning(f"Loaded {len(prompts_no_cache)} prompts in {(end-start)*1000:.2f}ms")
            st.caption("This hits the database EVERY time!")
    
    with col2:
        st.markdown("**✅ WITH Caching:**")
        if st.button("Load Prompts (Cached)"):
            start = time.time()
            # Cached call
            prompts_cached = load_all_prompts(db)
            end = time.time()
            st.success(f"Loaded {len(prompts_cached)} prompts in {(end-start)*1000:.2f}ms")
            st.caption("First time: hits DB. After that: uses cached data!")
    
    st.markdown("---")
    
    st.subheader("🧪 Experiment 3: Session State")
    
    st.markdown("""
    **Problem:** Normal variables reset on every re-run!  
    **Solution:** Use `st.session_state` to persist data across re-runs.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**❌ Normal Variable (Resets):**")
        
        # This counter ALWAYS shows 1 because the variable resets!
        normal_counter = 0
        
        if st.button("Increment Normal Counter"):
            normal_counter += 1
        
        st.error(f"Normal counter: {normal_counter}")
        st.caption("Always shows 0 because it resets on every re-run!")
    
    with col2:
        st.markdown("**✅ Session State (Persists):**")
        
        # Initialize session state counter
        if 'session_counter' not in st.session_state:
            st.session_state.session_counter = 0
        
        if st.button("Increment Session Counter"):
            st.session_state.session_counter += 1
        
        st.success(f"Session counter: {st.session_state.session_counter}")
        st.caption("Persists across re-runs!")
    
    st.markdown("---")
    
    st.subheader("📚 Key Takeaways")
    
    st.markdown("""
    1. **Re-runs are normal** in Streamlit - it's by design!
    2. **Use `@st.cache_data`** for data/computations that don't change often
    3. **Use `@st.cache_resource`** for connections (DB, models, etc.)
    4. **Use `st.session_state`** to persist values across re-runs
    5. **Check your terminal** to see when cached functions actually execute
    
    ### Caching Decorators:
    
    ```python
    @st.cache_data  # For data, DataFrames, lists, etc.
    def load_data():
        return expensive_computation()
    
    @st.cache_resource  # For connections, models, objects
    def get_database():
        return DatabaseConnection()
    
    # Session state for simple values
    if 'counter' not in st.session_state:
        st.session_state.counter = 0
    ```
    """)

# Browse Prompts Page
elif page == "Browse Prompts":
    st.header("📚 Browse Prompts")
    
    # Search and filter options
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_query = st.text_input("🔍 Search prompts", placeholder="Enter keywords...")
    
    with col2:
        filter_category = st.selectbox("Filter by Category", ["All"] + categories)
    
    # Fetch prompts based on search/filter (using cached functions where possible)
    if search_query:
        prompts = search_prompts(db, search_query)
        st.info(f"Found {len(prompts)} prompt(s) matching '{search_query}'")
    elif filter_category != "All":
        prompts = db.filter_by_category(filter_category)  # Could cache this too
        st.info(f"Showing {len(prompts)} prompt(s) in category '{filter_category}'")
    else:
        prompts = load_all_prompts(db)  # Using cached version!
    
    # Display prompts
    if not prompts:
        st.warning("No prompts found. Try a different search or add a new prompt!")
    else:
        for prompt in prompts:
            with st.expander(f"📝 {prompt['title']}", expanded=False):
                # Display metadata
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    if prompt['category']:
                        st.markdown(f"**Category:** {prompt['category']}")
                    if prompt['use_case']:
                        st.markdown(f"**Use Case:** {prompt['use_case']}")
                
                with col2:
                    st.markdown(f"**Upvotes:** 👍 {prompt['upvotes']}")
                
                with col3:
                    created = datetime.fromisoformat(prompt['created_at']).strftime("%Y-%m-%d")
                    st.markdown(f"**Added:** {created}")
                
                # Description
                if prompt['description']:
                    st.markdown(f"**Description:** {prompt['description']}")
                
                # Tags
                if prompt['tags']:
                    st.markdown("**Tags:**")
                    tags = prompt['tags'].split(',')
                    tag_html = " ".join([f"<span class='prompt-tag'>{tag.strip()}</span>" for tag in tags])
                    st.markdown(tag_html, unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Prompt text
                st.markdown("**Prompt:**")
                st.code(prompt['prompt_text'], language="text")
                
                # Action buttons
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    if st.button(f"📋 Copy to Clipboard", key=f"copy_{prompt['id']}"):
                        st.code(prompt['prompt_text'], language="text")
                        st.success("✅ Prompt displayed above - you can copy it from there!")
                
                with col2:
                    if st.button(f"👍 Upvote", key=f"upvote_{prompt['id']}"):
                        db.upvote_prompt(prompt['id'])
                        st.cache_data.clear()  # Clear cache so updated upvotes show
                        st.success("Upvoted!")
                        st.rerun()

# Add New Prompt Page (unchanged)
elif page == "Add New Prompt":
    st.header("➕ Add New Prompt")
    
    st.markdown("""
    Share your LLM prompt with the community! Your contribution helps other researchers.
    All submissions are anonymous.
    """)
    
    with st.form("add_prompt_form"):
        title = st.text_input("Prompt Title*", placeholder="e.g., Sentiment Analysis for Interviews")
        description = st.text_area("Description", placeholder="Brief description of what this prompt does...", height=100)
        prompt_text = st.text_area("Prompt Text*", placeholder="Enter your full prompt here. Use [PLACEHOLDERS] for parts the user should fill in.", height=300)
        
        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox("Category", [""] + ["Qualitative Analysis", "Quantitative Analysis", "Research Design", 
                        "Literature Review", "Data Analysis", "Content Analysis", "Digital Methods", "Survey Design", "Mixed Methods", "Other"])
        with col2:
            use_case = st.text_input("Use Case", placeholder="e.g., Coding interview transcripts")
        
        tags = st.text_input("Tags (comma-separated)", placeholder="e.g., sentiment, survey, qualitative")
        submitted = st.form_submit_button("🚀 Submit Prompt")
        
        if submitted:
            if not title or not prompt_text:
                st.error("❌ Please fill in all required fields (marked with *)")
            else:
                try:
                    prompt_id = db.add_prompt(title=title, description=description, prompt_text=prompt_text,
                                             category=category, tags=tags, use_case=use_case)
                    st.cache_data.clear()  # Clear cache so new prompt shows up
                    st.success(f"✅ Prompt added successfully! (ID: {prompt_id})")
                    st.balloons()
                    
                    with st.expander("View your submitted prompt"):
                        st.markdown(f"**Title:** {title}")
                        st.markdown(f"**Category:** {category}")
                        st.code(prompt_text, language="text")
                except Exception as e:
                    st.error(f"❌ Error adding prompt: {str(e)}")

# About Page (unchanged, truncated for brevity)
elif page == "About":
    st.header("ℹ️ About This Repository")
    st.markdown("""
    This repository demonstrates Streamlit's architecture with proper caching implementation.
    See the 🐛 Cache Demo page to understand how Streamlit re-runs work!
    """)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; font-size: 12px;'>
        LLM Prompt Repository | Built with Streamlit | Script runs: {st.session_state.run_count}
    </div>
""", unsafe_allow_html=True)