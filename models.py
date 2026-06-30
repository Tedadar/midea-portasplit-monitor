from dataclasses import dataclass
from datetime import datetime

@dataclass
class Product:
    name: str
    price: float
    url: str
    shop: str
    available: bool
    timestamp: str = datetime.utcnow().isoformat()
