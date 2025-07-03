# =========|Crafted By Shovit Dutta|===================================================
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from colorama import Fore, Style, init
init()
print(f"{Fore.CYAN}Loading environment variables...{Style.RESET_ALL}")
load_dotenv()
mongo_url = os.getenv("MONGO_URL")
if not mongo_url:
    print(f"{Fore.RED}Error: MONGO_URL not found in environment variables. Exiting.{Style.RESET_ALL}")
    exit(1)
print(f"{Fore.GREEN}Environment variables loaded.{Style.RESET_ALL}")
# =========|Crafted By Shovit Dutta|===================================================
try:
    print(f"{Fore.CYAN}Attempting to connect to MongoDB at {mongo_url}...{Style.RESET_ALL}")
    client = MongoClient(mongo_url)
    db = client.github_events
    print(f"{Fore.YELLOW}Connected to MongoDB. Dropping database: {db.name}...{Style.RESET_ALL}")
    client.drop_database(db.name)
    print(f"{Fore.GREEN}Database '{db.name}' dropped successfully.{Style.RESET_ALL}")
except Exception as e:
    print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")
finally:
    if "client" in locals() and client:
        print(f"{Fore.CYAN}Closing MongoDB connection.{Style.RESET_ALL}")
        client.close()
    else:
        print(f"{Fore.YELLOW}MongoDB client not initialized or already closed.{Style.RESET_ALL}")
# =========|Crafted By Shovit Dutta|===================================================