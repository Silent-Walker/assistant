def get_default_tasks():
    """
    Default daily routine if user adds nothing.
    """
    return [
        {"time": "07:00", "title": "Wake up", "category": "Personal"},
        {"time": "07:30", "title": "Exercise", "category": "Personal"},
        {"time": "09:00", "title": "PhD Research", "category": "PhD"},
        {"time": "13:00", "title": "Lunch", "category": "General"},
        {"time": "14:00", "title": "App Development", "category": "App"},
        {"time": "22:30", "title": "Sleep", "category": "Personal"}
    ]