"""
Seed initial data from docs/initial/anchor_chat_summary.md
"""

from sqlalchemy.orm import Session
from models import Project, Ritual, RitualStep
from core.database import get_db_session
import logging

logger = logging.getLogger(__name__)


def seed_initial_projects(db: Session):
    """Seed projects from anchor chat summary"""
    
    # Check if projects already exist
    existing_count = db.query(Project).count()
    if existing_count > 0:
        logger.info(f"Projects already seeded ({existing_count} existing projects)")
        return

    # Projects from docs/initial/anchor_chat_summary.md
    initial_projects = [
        {
            "title": "MCP connection to assistant",
            "status": "completed",
            "priority": "high",
            "category": "Technical",
            "is_completed": True,
            "is_high_priority": True,
            "description": "Connect MCP (Model Context Protocol) to the assistant for enhanced functionality"
        },
        {
            "title": "Assistant v0 (rituals, sprints, logging)",
            "status": "active", 
            "priority": "high",
            "category": "Personal Development",
            "is_high_priority": True,
            "description": "Core assistant functionality with ritual tracking, sprint management, and logging"
        },
        {
            "title": "Improve Reminder Attention-Grabbing",
            "status": "active",
            "priority": "medium", 
            "category": "UX",
            "description": "Make reminders more noticeable and effective"
        },
        {
            "title": "Inbox Zero (daily)",
            "status": "active",
            "priority": "medium",
            "category": "Productivity",
            "description": "Daily task to maintain inbox zero"
        },
        {
            "title": "Advertisements for Chi Life", 
            "status": "active",
            "priority": "medium",
            "category": "Chi Life",
            "description": "Create advertising materials for Chi Life business"
        },
        {
            "title": "Flyers, cards, etc. for Chi Life",
            "status": "active",
            "priority": "medium", 
            "category": "Chi Life",
            "description": "Physical marketing materials for Chi Life business"
        },
        {
            "title": "CJ Clarke for City Council",
            "status": "active",
            "priority": "medium",
            "category": "Community",
            "description": "Support CJ Clarke's city council campaign"
        },
        {
            "title": "NBA Connect for Greg Foster",
            "status": "active",
            "priority": "medium",
            "category": "Client Work", 
            "description": "NBA connection project for Greg Foster"
        },
        {
            "title": "Discord+ with Mark and James",
            "status": "active",
            "priority": "medium",
            "category": "Technical",
            "description": "Enhanced Discord functionality with Mark and James"
        },
        {
            "title": "Build the Personal Assistant app",
            "status": "active",
            "priority": "high", 
            "category": "Technical",
            "is_high_priority": True,
            "description": "Complete personal assistant application with full functionality"
        }
    ]

    # Add projects to database
    for project_data in initial_projects:
        project = Project(**project_data)
        db.add(project)

    db.commit()
    logger.info(f"Seeded {len(initial_projects)} initial projects")


def seed_initial_rituals(db: Session):
    """Seed rituals from anchor chat summary"""
    
    # Check if rituals already exist
    existing_count = db.query(Ritual).count()
    if existing_count > 0:
        logger.info(f"Rituals already seeded ({existing_count} existing rituals)")
        return

    # Morning ritual
    morning_ritual = Ritual(
        name="morning",
        title="Morning Ritual", 
        description="Morning routine to start the day with focus and energy",
        estimated_duration_minutes=20
    )
    db.add(morning_ritual)
    db.flush()  # Get the ID

    # Morning ritual steps
    morning_steps = [
        {"step_text": "Cold shower", "order": 1, "estimated_minutes": 5},
        {"step_text": "Put on Limitless AI pendant", "order": 2, "estimated_minutes": 1},
        {"step_text": "Quick projects/meetings review", "order": 3, "estimated_minutes": 5},
        {"step_text": "Journaling (gratitude + focus + visualization/affirmation)", "order": 4, "estimated_minutes": 9}
    ]
    
    for step_data in morning_steps:
        step = RitualStep(ritual_id=morning_ritual.id, **step_data)
        db.add(step)

    # Evening ritual
    evening_ritual = Ritual(
        name="evening",
        title="Evening Ritual",
        description="Evening routine for reflection and preparation", 
        estimated_duration_minutes=15
    )
    db.add(evening_ritual)
    db.flush()  # Get the ID

    # Evening ritual steps
    evening_steps = [
        {"step_text": "Charge all devices (including pendant)", "order": 1, "estimated_minutes": 2},
        {"step_text": "Retro journaling (3 wins + 1 lesson + tomorrow's focus)", "order": 2, "estimated_minutes": 10},
        {"step_text": "Looking ahead: pick tomorrow's focus", "order": 3, "estimated_minutes": 3}
    ]
    
    for step_data in evening_steps:
        step = RitualStep(ritual_id=evening_ritual.id, **step_data)
        db.add(step)

    db.commit()
    logger.info("Seeded morning and evening rituals with steps")


def seed_all_data():
    """Seed all initial data"""
    try:
        db = get_db_session()
        seed_initial_projects(db)
        seed_initial_rituals(db)
        logger.info("All initial data seeded successfully")
    except Exception as e:
        logger.error(f"Error seeding data: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_all_data()