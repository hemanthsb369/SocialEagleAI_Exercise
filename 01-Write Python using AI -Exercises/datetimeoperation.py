# date_time_operations.py

from datetime import datetime, timedelta

# Current date and time
now = datetime.now()
print("Current Date and Time:", now)

# Format date and time
formatted = now.strftime("%Y-%m-%d %H:%M:%S")
print("Formatted Date and Time:", formatted)

# Extract individual components
print("Year:", now.year)
print("Month:", now.month)
print("Day:", now.day)
print("Hour:", now.hour)
print("Minute:", now.minute)
print("Second:", now.second)

# Add 7 days to current date
future_date = now + timedelta(days=7)
print("Date after 7 days:", future_date.strftime("%Y-%m-%d"))

# Subtract 30 minutes
past_time = now - timedelta(minutes=30)
print("Time 30 minutes ago:", past_time.strftime("%H:%M:%S"))

# Convert string to datetime
date_str = "2025-11-06 19:00:00"
converted = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
print("Converted from string:", converted)