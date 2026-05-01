# Fake customer database — simulates a real internal database table

CUSTOMERS = [
    {"id": 1, "name": "John Smith",     "credit_score": 720, "income": 45000, "status": "active"},
    {"id": 2, "name": "Priya Sharma",   "credit_score": 810, "income": 72000, "status": "active"},
    {"id": 3, "name": "Marcus Johnson", "credit_score": 640, "income": 31000, "status": "active"},
    {"id": 4, "name": "Li Wei",         "credit_score": 755, "income": 58000, "status": "active"},
    {"id": 5, "name": "Sarah O'Brien",  "credit_score": 690, "income": 41000, "status": "active"},
    {"id": 6, "name": "Arjun Patel",    "credit_score": 780, "income": 63000, "status": "active"},
    {"id": 7, "name": "Emma Clarke",    "credit_score": 720, "income": 52000, "status": "active"},
    {"id": 8, "name": "David Okonkwo",  "credit_score": 605, "income": 28000, "status": "active"},
    {"id": 9, "name": "Fatima Al-Hassan","credit_score": 830, "income": 95000,"status": "active"},
    {"id": 10,"name": "Tom Nguyen",     "credit_score": 700, "income": 47000, "status": "active"},
]

def get_customer_by_name(name: str) -> dict | None:
    for c in CUSTOMERS:
        if c["name"].lower() == name.lower():
            return c
    return None

def get_all_customers() -> list:
    return CUSTOMERS