from flask import Flask, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/bin-data')
def bin_data():
    today = datetime.now().date()
    
    # 1. Recycling (Every Wednesday)
    days_until_wed = (2 - today.weekday() + 7) % 7
    next_wednesday = today + timedelta(days=days_until_wed)
    
    # 2. Black Bin (Every 2 weeks on Friday)
    # Anchor: Feb 6, 2026 was a collection day
    anchor_date = datetime(2026, 2, 6).date()
    days_since_anchor = (today - anchor_date).days
    
    # Calculate weeks since anchor (integer division)
    weeks_since = days_since_anchor // 7
    
    # If weeks_since is even, this Friday is a collection day
    # If weeks_since is odd, next Friday is a collection day
    if weeks_since % 2 == 0:
        days_until_fri = (4 - today.weekday() + 7) % 7
    else:
        days_until_fri = (4 - today.weekday() + 14) % 7
        
    next_friday = today + timedelta(days=days_until_fri)

    return jsonify({
        "merge_variables": {
            "recycling_day": next_wednesday.strftime("%A, %b %d"),
            "black_bin_day": next_friday.strftime("%A, %b %d"),
            "is_black_bin_week": (weeks_since % 2 == 0)
        }
    })

if __name__ == '__main__':
    app.run()

