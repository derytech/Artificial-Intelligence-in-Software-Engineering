"""
SQLAlchemy ORM Database Management System
-----------------------------------------
This module provides an object-oriented interface for managing a user database
using SQLAlchemy ORM (v2.0 style) and PyMySQL driver.
"""

from typing import List, Optional
from sqlalchemy import String, create_engine, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

# ==========================================
# 1. Database Configuration & Setup
# ==========================================

# Connection URL format: dialect+driver://username:password@host:port/database_name
# Replace placeholders with your actual database credentials.
DATABASE_URL = "mysql+pymysql://db_user:db_password@localhost:3306/example_db"

# Create the database engine.
# echo=True logs SQL queries for debugging (set to False in production).
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)

# Create a configured session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ==========================================
# 2. ORM Declarative Base & Model Definition
# ==========================================

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy declarative ORM models."""
    pass


class User(Base):
    """
    User model representing the 'users' table in the database.
    Maps Python class attributes directly to database table columns.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"


def init_db() -> None:
    """Create all tables defined by models extending Base."""
    Base.metadata.create_all(bind=engine)


# ==========================================
# 3. CRUD Operations (Repository Pattern)
# ==========================================

def create_user(username: str, email: str) -> Optional[User]:
    """Create and insert a new user into the database."""
    if not username or not email:
        print("Error: Username and email are required.")
        return None

    with SessionLocal() as session:
        try:
            new_user = User(username=username, email=email)
            session.add(new_user)
            session.commit()
            # Refresh loads database-generated values (like auto-increment ID)
            session.refresh(new_user)
            print(f"User '{username}' created successfully with ID {new_user.id}.")
            return new_user
        except IntegrityError:
            session.rollback()
            print(f"Error: User with username '{username}' or email '{email}' already exists.")
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Database error occurred: {e}")
        return None


def get_user_by_username(username: str) -> Optional[User]:
    """Query a single user by their username using modern select() constructs."""
    with SessionLocal() as session:
        try:
            stmt = select(User).where(User.username == username)
            user = session.scalars(stmt).first()
            return user
        except SQLAlchemyError as e:
            print(f"Error fetching user '{username}': {e}")
            return None


def update_user_email(username: str, new_email: str) -> bool:
    """Update an existing user's email address."""
    with SessionLocal() as session:
        try:
            stmt = select(User).where(User.username == username)
            user = session.scalars(stmt).first()

            if not user:
                print(f"User '{username}' not found.")
                return False

            user.email = new_email
            session.commit()
            print(f"Email updated successfully for user '{username}'.")
            return True
        except IntegrityError:
            session.rollback()
            print(f"Error: The email '{new_email}' is already in use.")
            return False
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Database error during update: {e}")
            return False


def delete_user(username: str) -> bool:
    """Delete a user from the database by username."""
    with SessionLocal() as session:
        try:
            stmt = select(User).where(User.username == username)
            user = session.scalars(stmt).first()

            if not user:
                print(f"User '{username}' not found.")
                return False

            session.delete(user)
            session.commit()
            print(f"User '{username}' deleted successfully.")
            return True
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Database error during deletion: {e}")
            return False


def list_users() -> List[User]:
    """Retrieve and list all users in the database."""
    with SessionLocal() as session:
        try:
            stmt = select(User).order_by(User.id)
            users = session.scalars(stmt).all()
            return list(users)
        except SQLAlchemyError as e:
            print(f"Error listing users: {e}")
            return []


# ==========================================
# 4. Demonstration Execution
# ==========================================

if __name__ == "__main__":
    print("--- Initializing Database ---")
    init_db()

    print("\n--- 1. Testing Create ---")
    create_user("alice_dev", "alice@example.com")
    create_user("bob_designer", "bob@example.com")
    # Duplicate attempt to show IntegrityError handling:
    create_user("alice_dev", "alice_alternate@example.com")

    print("\n--- 2. Testing Read/Query ---")
    found_user = get_user_by_username("alice_dev")
    print(f"Fetched User: {found_user}")

    print("\n--- 3. Testing Update ---")
    update_user_email("alice_dev", "alice_new@example.com")

    print("\n--- 4. Testing List ---")
    all_users = list_users()
    for u in all_users:
        print(f" - {u}")

    print("\n--- 5. Testing Delete ---")
    delete_user("bob_designer")

    print("\n--- Final User List ---")
    final_users = list_users()
    for u in final_users:
        print(f" - {u}")