import time
import pandas as pd
from datetime import datetime

def mock_process(name, feedback, category, priority):
    time.sleep(2)  # Simulate delay
    result_text = f"Thanks {name}, your feedback has been recorded."
    result_data = [
        {"ID": 1, "Category": category, "Priority": priority, "Status": "Received"},
        {"ID": 2, "Category": category, "Priority": priority, "Status": "In Progress"},
    ]
    return result_text, result_data

def get_initial_data():
    inial_data = pd.DataFrame({
        "Incident ID": ["INC1001", "INC1002", "INC1003", "INC1004"],
        "Date Reported": [
            datetime(2025, 8, 26),
            datetime(2025, 8, 27),
            datetime(2025, 8, 27),
            datetime(2025, 8, 28),
        ],
        "Status": ["Open", "In Progress", "Resolved", "Open"],
        "Priority": ["High", "Medium", "Low", "High"],
        "Assigned To": ["Alice", "Bob", "Charlie", "Dana"],
        "Description": [
            "Email service outage",
            "VPN connection issue",
            "Password reset request",
            "Slow internet connectivity"
        ]
    })
    return inial_data