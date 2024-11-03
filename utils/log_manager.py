from pymongo import MongoClient
from datetime import datetime

# Configuração do MongoDB
client = MongoClient("mongodb://smartpet:smartpet@localhost:27017/")
db = client.smartpet
logs_collection = db.logs

def save_log(level, screen, message):
    """Salva o log na coleção MongoDB."""
    log_entry = {
        "level": level,
        "screen": screen,
        "message": message,
        "timestamp": datetime.now()
    }
    logs_collection.insert_one(log_entry)
