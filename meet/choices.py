STATUS_CHOICES = [
    ('scheduled', 'Scheduled'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
]
    
VALID_STATUS_CHANGE = {
    'scheduled': ['in_progress', 'completed', 'cancelled'],
    'in_progress': ['completed', 'cancelled'],
    'completed': [],
    'cancelled': [],
}

MEETING_TYPE_CHOICES = [
    ('in_person', 'In Person'),
    ('online', 'Online'),
]