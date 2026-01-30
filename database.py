import sqlite3
from datetime import datetime
from typing import List, Dict, Optional

class PromptDatabase:
    def __init__(self, db_name="prompts.db"):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        """Create a database connection"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        return conn
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prompts (
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
        """)
        
        conn.commit()
        conn.close()
    
    def add_prompt(self, title: str, prompt_text: str, description: str = "",
                   category: str = "", tags: str = "", use_case: str = "") -> int:
        """Add a new prompt to the database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO prompts (title, description, prompt_text, category, tags, use_case)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, description, prompt_text, category, tags, use_case))
        
        prompt_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return prompt_id
    
    def get_all_prompts(self) -> List[Dict]:
        """Retrieve all prompts from the database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM prompts ORDER BY created_at DESC
        """)
        
        prompts = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return prompts
    
    def search_prompts(self, query: str) -> List[Dict]:
        """Search prompts by title, description, category, or tags"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        search_query = f"%{query}%"
        cursor.execute("""
            SELECT * FROM prompts 
            WHERE title LIKE ? 
               OR description LIKE ? 
               OR category LIKE ?
               OR tags LIKE ?
               OR use_case LIKE ?
            ORDER BY created_at DESC
        """, (search_query, search_query, search_query, search_query, search_query))
        
        prompts = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return prompts
    
    def get_prompt_by_id(self, prompt_id: int) -> Optional[Dict]:
        """Get a specific prompt by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM prompts WHERE id = ?", (prompt_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        return dict(row) if row else None
    
    def upvote_prompt(self, prompt_id: int):
        """Increment upvotes for a prompt"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE prompts 
            SET upvotes = upvotes + 1 
            WHERE id = ?
        """, (prompt_id,))
        
        conn.commit()
        conn.close()
    
    def get_categories(self) -> List[str]:
        """Get all unique categories"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT DISTINCT category FROM prompts WHERE category != ''")
        categories = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        
        return sorted(categories)
    
    def filter_by_category(self, category: str) -> List[Dict]:
        """Filter prompts by category"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM prompts 
            WHERE category = ?
            ORDER BY created_at DESC
        """, (category,))
        
        prompts = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return prompts
    
    def get_prompt_count(self) -> int:
        """Get total number of prompts"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM prompts")
        count = cursor.fetchone()[0]
        
        conn.close()
        
        return count
