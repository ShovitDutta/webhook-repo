# =========|Crafted By Shovit Dutta|===================================================
import os
from dotenv import load_dotenv
from pymongo import MongoClient
load_dotenv()
mongo_url = os.getenv("MONGO_URL")
if not mongo_url: exit(1)
# =========|Crafted By Shovit Dutta|===================================================
try:
    client = MongoClient(mongo_url)
    db = client.github_events
    client.drop_database(db.name)
except Exception as e:
    pass
finally:
    if "client" in locals() and client: client.close()
# =========|Crafted By Shovit Dutta|===================================================