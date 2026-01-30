# LLM Prompt Repository for Social Science Research

A web application for social scientists to share and discover LLM prompts for research purposes.

## Features

- 📚 Browse prompts by category or search
- ➕ Add new prompts (anonymous)
- 👍 Upvote useful prompts
- 🏷️ Filter by categories and tags
- 📋 Easy copy-to-clipboard functionality
- 🔍 Full-text search across all prompts

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

### Step 2: Initialize Database with Sample Data

```bash
# Run the seed script to populate the database with example prompts
python seed_data.py
```

This will create a `prompts.db` SQLite database and populate it with 10 example prompts.

### Step 3: Run the Application

```bash
# Start the Streamlit app
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

## Usage

### Browse Prompts
1. Go to "Browse Prompts" page
2. Use the search bar to find specific prompts
3. Filter by category using the dropdown
4. Click on any prompt to expand and view details
5. Click "Copy to Clipboard" to use the prompt

### Add New Prompt
1. Go to "Add New Prompt" page
2. Fill in the form:
   - **Title**: Descriptive name for your prompt
   - **Description**: What the prompt does
   - **Prompt Text**: The actual prompt (use [PLACEHOLDERS] for user inputs)
   - **Category**: Select from predefined categories
   - **Use Case**: Brief description of when to use it
   - **Tags**: Comma-separated keywords
3. Click "Submit Prompt"

### Upvote Prompts
- Click the "👍 Upvote" button on useful prompts
- Helps others discover valuable prompts

## Project Structure

```
llm-prompt-repository/
│
├── app.py                 # Main Streamlit application
├── database.py            # Database operations (SQLite)
├── seed_data.py           # Sample data loader
├── prompts.db             # SQLite database (created automatically)
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Database Schema

```sql
CREATE TABLE prompts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    prompt_text TEXT NOT NULL,
    category TEXT,
    tags TEXT,
    use_case TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    upvotes INTEGER DEFAULT 0
)
```

## Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **Database**: SQLite
- **Language**: Python 3.8+

## Example Prompts Included

The repository comes pre-populated with 10 example prompts covering:
- Sentiment Analysis
- Interview Transcript Coding
- Research Question Generation
- Literature Review Summarization
- Data Categorization
- Social Media Analysis
- Survey Question Improvement
- Hypothesis Generation
- Focus Group Discussion Guide
- Statistical Result Interpretation

## Future Enhancements

- User authentication and profiles
- Prompt versioning
- Advanced filtering and sorting
- Export prompts to various formats
- REST API for programmatic access
- Collaborative editing
- Prompt collections/bundles

## Notes

- All submissions are anonymous (no authentication required)
- Database resets if `prompts.db` is deleted
- Re-run `seed_data.py` to restore example prompts

## Troubleshooting

**Database already exists error:**
- The seed script checks for existing data
- Delete `prompts.db` and re-run `python seed_data.py` to reset

**Port already in use:**
```bash
# Run on a different port
streamlit run app.py --server.port 8502
```

**Module not found:**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

## License

This project is for educational and research purposes.
