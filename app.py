import streamlit as st
from database import PromptDatabase
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="LLM Prompt Repository for Social Science",
    page_icon="🔬",
    layout="wide"
)

# Initialize database
db = PromptDatabase()

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
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("🔬 LLM Prompt Repository for Social Science Research")
st.markdown("""
Welcome to the prompt repository! Browse prompts shared by the community or add your own.
All prompts are designed to help social scientists leverage LLMs in their research.
""")

# Sidebar for navigation and filtering
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Browse Prompts", "Add New Prompt", "About"])

# Get statistics
total_prompts = db.get_prompt_count()
categories = db.get_categories()

st.sidebar.markdown("---")
st.sidebar.metric("Total Prompts", total_prompts)

# Browse Prompts Page
if page == "Browse Prompts":
    st.header("📚 Browse Prompts")
    
    # Search and filter options
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_query = st.text_input("🔍 Search prompts", placeholder="Enter keywords...")
    
    with col2:
        filter_category = st.selectbox("Filter by Category", ["All"] + categories)
    
    # Fetch prompts based on search/filter
    if search_query:
        prompts = db.search_prompts(search_query)
        st.info(f"Found {len(prompts)} prompt(s) matching '{search_query}'")
    elif filter_category != "All":
        prompts = db.filter_by_category(filter_category)
        st.info(f"Showing {len(prompts)} prompt(s) in category '{filter_category}'")
    else:
        prompts = db.get_all_prompts()
    
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
                        st.success("Upvoted!")
                        st.rerun()

# Add New Prompt Page
elif page == "Add New Prompt":
    st.header("➕ Add New Prompt")
    
    st.markdown("""
    Share your LLM prompt with the community! Your contribution helps other researchers.
    All submissions are anonymous.
    """)
    
    with st.form("add_prompt_form"):
        # Form fields
        title = st.text_input("Prompt Title*", placeholder="e.g., Sentiment Analysis for Interviews")
        
        description = st.text_area(
            "Description", 
            placeholder="Brief description of what this prompt does...",
            height=100
        )
        
        prompt_text = st.text_area(
            "Prompt Text*",
            placeholder="Enter your full prompt here. Use [PLACEHOLDERS] for parts the user should fill in.",
            height=300
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            category = st.selectbox(
                "Category",
                [""] + ["Qualitative Analysis", "Quantitative Analysis", "Research Design", 
                        "Literature Review", "Data Analysis", "Content Analysis", 
                        "Digital Methods", "Survey Design", "Mixed Methods", "Other"]
            )
        
        with col2:
            use_case = st.text_input(
                "Use Case",
                placeholder="e.g., Coding interview transcripts"
            )
        
        tags = st.text_input(
            "Tags (comma-separated)",
            placeholder="e.g., sentiment, survey, qualitative"
        )
        
        # Submit button
        submitted = st.form_submit_button("🚀 Submit Prompt")
        
        if submitted:
            # Validation
            if not title or not prompt_text:
                st.error("❌ Please fill in all required fields (marked with *)")
            else:
                # Add to database
                try:
                    prompt_id = db.add_prompt(
                        title=title,
                        description=description,
                        prompt_text=prompt_text,
                        category=category,
                        tags=tags,
                        use_case=use_case
                    )
                    st.success(f"✅ Prompt added successfully! (ID: {prompt_id})")
                    st.balloons()
                    
                    # Show what was added
                    with st.expander("View your submitted prompt"):
                        st.markdown(f"**Title:** {title}")
                        st.markdown(f"**Category:** {category}")
                        st.code(prompt_text, language="text")
                    
                except Exception as e:
                    st.error(f"❌ Error adding prompt: {str(e)}")

# About Page
elif page == "About":
    st.header("ℹ️ About This Repository")
    
    st.markdown("""
    ## Purpose
    
    This LLM Prompt Repository is designed specifically for **social scientists** who want to:
    - 📚 Discover effective prompts for common research tasks
    - 🤝 Share their own proven prompts with the community
    - ⚡ Accelerate their research by reusing tested prompts
    - 🎓 Learn best practices for using LLMs in social science research
    
    ## How to Use
    
    1. **Browse Prompts**: Explore prompts by category or search for specific use cases
    2. **Copy & Use**: Copy any prompt and paste it into your preferred LLM (ChatGPT, Claude, etc.)
    3. **Customize**: Replace placeholders with your own data
    4. **Share**: Add your own successful prompts to help others
    
    ## Categories
    
    Our prompts cover various research areas:
    - **Qualitative Analysis**: Interview coding, thematic analysis, content analysis
    - **Quantitative Analysis**: Statistical interpretation, data processing
    - **Research Design**: Hypothesis generation, survey design, methodology
    - **Literature Review**: Paper summarization, synthesis
    - **Data Analysis**: Categorization, sentiment analysis, coding
    - **Digital Methods**: Social media analysis, web scraping
    
    ## Privacy & Anonymity
    
    - All contributions are **anonymous**
    - No authentication required
    - Focus on collaborative knowledge sharing
    
    ## Technology
    
    Built with:
    - **Streamlit** (Python web framework)
    - **SQLite** (Database)
    - **Python** (Backend logic)
    
    ## Future Enhancements
    
    Potential features for future versions:
    - User accounts and authentication
    - Prompt versioning
    - Rating and review system
    - API access for programmatic use
    - Export functionality
    - Prompt templates and wizards
    
    ---
    
    **Note**: This is a demonstration project created for research purposes.
    All example prompts are for educational use.
    """)
    
    # Stats
    st.markdown("---")
    st.subheader("📊 Repository Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Prompts", total_prompts)
    
    with col2:
        st.metric("Categories", len(categories))
    
    with col3:
        if prompts := db.get_all_prompts():
            total_upvotes = sum(p['upvotes'] for p in prompts)
            st.metric("Total Upvotes", total_upvotes)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; font-size: 12px;'>
        LLM Prompt Repository for Social Science Research | Built with Streamlit
    </div>
""", unsafe_allow_html=True)
