#!/bin/bash

# Simple script to set up and run the LLM Prompt Repository

echo "======================================"
echo "LLM Prompt Repository - Setup & Run"
echo "======================================"
echo ""

# Check if database exists
if [ ! -f "prompts.db" ]; then
    echo "📦 Database not found. Initializing with sample data..."
    python seed_data.py
    echo ""
else
    echo "✅ Database found. Skipping seed data."
    echo ""
fi

# Run the Streamlit app
echo "🚀 Starting Streamlit app..."
echo "The app will open in your browser at http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server."
echo ""

streamlit run app.py
