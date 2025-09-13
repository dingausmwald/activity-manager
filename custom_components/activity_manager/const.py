DOMAIN = "activity_manager"

# Default state terms
DEFAULT_STATE_SCHEDULED = "scheduled"
DEFAULT_STATE_DUE = "due"
DEFAULT_STATE_OVERDUE = "overdue"

# Default update interval
DEFAULT_UPDATE_INTERVAL = "daily"

# Update interval options
UPDATE_INTERVALS = {
    "daily": 24 * 60 * 60,      # 24 hours in seconds
    "hourly": 60 * 60,          # 1 hour in seconds  
    "15min": 15 * 60,           # 15 minutes in seconds
    "5min": 5 * 60,             # 5 minutes in seconds
}