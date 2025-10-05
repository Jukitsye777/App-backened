"""
Database Configuration - Supabase Connection
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Supabase credentials from environment
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_db():
    """
    Returns the Supabase client instance
    Use this in your routes to access the database
    """
    return supabase

# Test connection
def test_connection():
    """
    Test if database connection is working
    """
    try:
        result = supabase.table('projects').select("id").limit(1).execute()
        print("✅ Database connection successful!")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()