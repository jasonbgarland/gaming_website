"""
Seed script: ensure the default test user exists in the database.

Safe to run multiple times — skips insertion if the user already exists.

Credentials:
    username : tester
    email    : tester@test.com
    password : test1234
"""

import logging
import os
import sys

from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# db/ is on the path when run from /app (set in Dockerfile)
from db.models.user import User  # noqa: E0401

logging.basicConfig(level=logging.INFO, format="%(levelname)s [seed] %(message)s")
logger = logging.getLogger("seed")

TEST_USER = {
    "username": "tester",
    "email": "tester@test.com",
    "password": "test1234",
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def seed(database_url: str) -> None:
    """Insert the test user if it doesn't already exist."""
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(bind=engine)

    with SessionLocal() as db:
        existing = db.query(User).filter(User.username == TEST_USER["username"]).first()
        if existing:
            logger.info(
                "Test user '%s' already exists — skipping.", TEST_USER["username"]
            )
            return

        hashed = pwd_context.hash(TEST_USER["password"])
        user = User(
            username=TEST_USER["username"],
            email=TEST_USER["email"],
            hashed_password=hashed,
            is_active=1,
        )
        db.add(user)
        db.commit()
        logger.info(
            "Test user '%s' (%s) created.", TEST_USER["username"], TEST_USER["email"]
        )


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if not url:
        logger.error("DATABASE_URL environment variable is not set.")
        sys.exit(1)
    seed(url)
