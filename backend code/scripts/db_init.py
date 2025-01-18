import uuid
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.db.models import Site, Story, Audio, User, Artifact
from app.db.database import Base
from app.config import Config
from app.db.database import engine
from passlib.context import CryptContext

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_tables():
    """Creates the tables in the database using SQLAlchemy."""
    try:
        Base.metadata.create_all(engine)
        print("Tables created successfully!")

    except Exception as ex:
        print(f"Error creating tables using sqlalchemy: {ex}")


def seed_database():
    """Populates the database with initial data using SQLAlchemy."""
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    try:
         
         sites = [
             Site(site_id=uuid.uuid4(), name="Amphitheatre of El Jem", latitude=35.3008, longitude=10.7054,
                  description="A UNESCO World Heritage Site, the Amphitheatre of El Jem is one of the largest and best-preserved Roman amphitheaters in the world, showcasing Tunisia's rich Roman heritage. It could seat 35,000 spectators. The amphitheater was built in the 3rd century.", opening_hours="8 AM to 6 PM",
                  accessibility_info="Accessible by paved paths; limited wheelchair access inside the structure.",
                  tour_url = "https://www.tourismtunisia.com/el-jem-amphitheatre",
                     map_url = "https://example.com/el_jem_map.png",
                     past_image="https://upload.wikimedia.org/wikipedia/commons/2/2a/El_Djem_Amphitheatre.jpg", now_image = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/El_Jem_amphitheatre_tunisia.jpg/800px-El_Jem_amphitheatre_tunisia.jpg"),
              Site(site_id=uuid.uuid4(), name="Dougga", latitude=36.4176, longitude=9.2178,
                 description="Dougga is a well-preserved Roman town with theaters, temples, and baths, showcasing ancient urban planning and engineering. It is also listed as a UNESCO World Heritage Site. The site, which covers 75 hectares (190 acres), dates back to the Numidian period, and its current Roman layout took place during the second and third centuries.", opening_hours="9 AM to 5 PM",
                 accessibility_info="Uneven terrain; limited wheelchair access.", tour_url = "https://www.tourismtunisia.com/dougga", map_url = "https://example.com/dougga_map.png",
                past_image="https://upload.wikimedia.org/wikipedia/commons/a/a5/Dougga_Capitol.jpg", now_image = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/Dougga_Th%C3%A9%C3%A2tre.jpg/800px-Dougga_Th%C3%A9%C3%A2tre.jpg"),
             Site(site_id=uuid.uuid4(), name="Bardo National Museum", latitude=36.7949, longitude=10.1658,
                 description="One of Africa's most important museums, the Bardo National Museum houses a vast collection of Roman mosaics, Islamic artifacts, and Punic relics. The museum houses one of the world's largest collections of Roman mosaics, and includes artifacts from prehistory and all historical periods of Tunisia, including Punic, Roman, Byzantine, and Arab-Islamic.", opening_hours="10 AM to 6 PM",
                 accessibility_info="Partially accessible; some trails are uneven", tour_url = "https://www.tourismtunisia.com/ichkeul-national-park", map_url = "https://example.com/bardo_museum_map.png",
                 past_image="https://upload.wikimedia.org/wikipedia/commons/d/d9/Ichkeul_Lake.jpg", now_image = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/64/Bardo_Museum_Tunis_Tunisia.jpg/800px-Bardo_Museum_Tunis_Tunisia.jpg")
         ]
         stories = [
             Story(story_id=uuid.uuid4(), site_id=sites[0].site_id,  title="Gladiator Fight",
                 summary="A description of a typical gladiator fight in the amphitheater.",
                 full_text="A detailed story about the gladiator fight.",
                 audio_url="audio_url_gladiator.mp3", author="Historian A", source="Historical Document A",
                 type="oral_history"),
              Story(story_id=uuid.uuid4(), site_id=sites[1].site_id,  title="A Roman Life",
                 summary="A story about how life was in Dougga.",
                  full_text="A detailed story of life in Dougga",
                 audio_url="audio_url_roman.mp3", author="Historian B", source="Historical Document B",
                  type="legend"),
             Story(story_id=uuid.uuid4(), site_id=sites[2].site_id,  title="The Legend of Didon",
                 summary="The legend of the queen Didon.",
                 full_text="A detailed story about the queen Didon.",
                 audio_url="audio_url_didon.mp3", author="Historian C", source="Historical Document C",
                  type="legend")
         ]
         audio_files = [
             Audio(audio_id = uuid.uuid4(), site_id = sites[0].site_id, audio_url = "audio_url_gladiator.mp3",
                  title = "Gladiator Fight Narration", duration = 120, transcripts = "The gladiator is here"),
              Audio(audio_id = uuid.uuid4(), site_id = sites[1].site_id, audio_url = "audio_url_roman.mp3",
                  title = "Roman Life Narration", duration = 120, transcripts = "A long life in the roman empire"),
              Audio(audio_id = uuid.uuid4(), site_id = sites[2].site_id, audio_url = "audio_url_didon.mp3",
                  title = "Didon legend Narration", duration = 120, transcripts = "The queen didon"),

         ]
         artifacts = [
              Artifact(artifact_id=uuid.uuid4(), site_id = sites[0].site_id, name="Roman Coin",
                   description="A small bronze coin with the roman emperor portrait", image_url ="coin.jpg", model_url = "coin.glb"),
                Artifact(artifact_id=uuid.uuid4(), site_id = sites[1].site_id, name="Roman pottery",
                   description="A well preserved Roman pottery from Dougga", image_url ="pottery.jpg", model_url = "pottery.glb")
         ]
         users = [
          User(username="admin",email="admin@example.com", password_hash=pwd_context.hash("admin*+65@))"),
                role = "admin", user_id=uuid.uuid4())
       
         ]
         session.add_all(sites)
         session.add_all(stories)
         session.add_all(audio_files)
         session.add_all(artifacts)
         session.add_all(users)
         session.commit()

         print("Database seeded successfully!")
    except Exception as ex:
        session.rollback()
        print(f"Error seeding the database using sqlalchemy: {ex}")

    finally:
        session.close()


def init_db():
    create_tables()
    seed_database()

if __name__ == "__main__":
    init_db()
