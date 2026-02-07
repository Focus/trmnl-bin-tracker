@app.route('/bin-data')
def bin_data():
    today = datetime.now().date()
    
    # 1. Recycling (Every Wednesday)
    days_until_wed = (2 - today.weekday() + 7) % 7
    # If today is Wednesday, we show today. If you want to show NEXT Wed, change % 7 to + 7
    next_wed = today + timedelta(days=days_until_wed)
    wed_suffix = get_date_suffix(next_wed.day)
    
    # 2. Black Bin (Every 2 weeks on Friday)
    anchor_date = datetime(2026, 2, 6).date()
    
    # Calculate weeks elapsed since the anchor Friday
    days_since_anchor = (today - anchor_date).days
    weeks_since = days_since_anchor // 7
    
    # LOGIC:
    # Week 0 (Feb 6 - Feb 12): Collection was Feb 6. Next is in 14 days from Feb 6.
    # Week 1 (Feb 13 - Feb 19): This is the 'off' week. Next is coming up this Friday.
    
    if weeks_since % 2 == 0:
        # We are in the week FOLLOWING a collection. Next one is 2 Fridays away.
        # We calculate days until the Friday that is (weeks_since + 2) from anchor.
        next_collection_date = anchor_date + timedelta(weeks=(weeks_since + 2))
    else:
        # We are in the 'off' week. Next one is the very next Friday.
        next_collection_date = anchor_date + timedelta(weeks=(weeks_since + 1))
        
    fri_suffix = get_date_suffix(next_collection_date.day)

    return jsonify({
        "recycling_day": next_wed.strftime(f"%a {next_wed.day}{wed_suffix}"),
        "black_bin_day": next_collection_date.strftime(f"%a {next_collection_date.day}{fri_suffix}"),
        "is_black_bin_week": (next_collection_date - today).days <= 6
    })
