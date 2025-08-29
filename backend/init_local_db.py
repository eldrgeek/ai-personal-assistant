#!/usr/bin/env python3
"""
Initialize local database with seed data
Run this script before starting the local app to ensure persistent data
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🚀 Initializing local database...")
    
    try:
        # Import and run database initialization
        from core.database import init_db
        from utils.seed_data import seed_all_data
        import asyncio
        
        # Initialize database tables
        print("📊 Creating database tables...")
        asyncio.run(init_db())
        
        # Seed initial data
        print("🌱 Seeding initial data...")
        seed_all_data()
        
        print("✅ Local database initialized successfully!")
        print("📁 Database file location:", os.path.abspath("ai_assistant.db"))
        
        # Verify data was added
        from core.database import get_db_session
        from models import Project, Ritual
        
        db = get_db_session()
        project_count = db.query(Project).count()
        ritual_count = db.query(Ritual).count()
        db.close()
        
        print(f"📊 Data verification:")
        print(f"   - Projects: {project_count}")
        print(f"   - Rituals: {ritual_count}")
        
        if project_count > 0 and ritual_count > 0:
            print("🎉 Database is ready with persistent data!")
        else:
            print("⚠️  Database initialized but no data found")
            
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
