
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tunisian_sites.db")