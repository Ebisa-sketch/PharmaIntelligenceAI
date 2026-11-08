import os

# Configure test environment variables before importing app modules
os.environ["DATABASE_URL"] = "sqlite:///./pharmaintelligence_test.db"
os.environ["ENVIRONMENT"] = "testing"
os.environ["DEBUG"] = "False"
