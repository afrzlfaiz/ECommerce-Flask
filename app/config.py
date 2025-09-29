import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret")
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
    SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")  # DO NOT use in requests
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000")
    PORT = int(os.getenv("PORT", "5000"))

    @property
    def ALLOWED_ORIGINS_LIST(self):
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",") if o.strip()]
