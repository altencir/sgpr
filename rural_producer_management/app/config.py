from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://user:password@localhost:5432/rural_db"
    test_database_url: str = "postgresql://user:password@localhost:5432/rural_test_db"
    
    class Config:
        env_file = ".env"

settings = Settings()