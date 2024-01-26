# Import Flask and requests libraries
from flask import Flask, jsonify, abort
import requests
import calendar

# Necessary header if you're hitting the endpoints using a browser
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
# Create a Flask app instance
app = Flask(__name__)

@app.route("/")
def home():
    return jsonify("Home")
    
# Retrieve a list of the most viewed articles of a month for a certain week
@app.route("/most-viewed/<year>/<month>/<week>")
def most_viewed_week(year, month, week):
    validate_input(None, year, month, week)
    # Get the number of days in the month, find the start day of the week as long as it exists in the month
    days = calendar.monthrange(int(year), int(month)) [1]
    start_day = clean_int_less_than_10(int(week) * 7)
    end_day = clean_int_less_than_10(start_day + 7)
    # Get the days 1 week after start, and if it exceeds the months last day, end at the final day of the month
    if end_day > days:
        end_day = days
    if start_day < days:
        return most_viewed_helper(year, month, start_day, end_day)
    else: 
        return jsonify({"error": "The week " + week + " is too large"})

# Retrieve a list of the most viewed articles for a month
@app.route("/most-viewed/<year>/<month>")
def most_viewed(year, month):
    validate_input(None, year, month, None)
    days = calendar.monthrange(int(year), int(month)) [1]
    return most_viewed_helper(year, month, 1, days)
    
def most_viewed_helper(year, month, start_day, end_day):
    language = "en.wikipedia"
    base_url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/top/"
    articles = {}
    base_url = base_url + language + "/all-access/" + str(year) + "/" + str(month) + "/"
    for day in range(start_day, end_day + 1):         
        day = clean_int_less_than_10(day)
        api_url = base_url + str(day)
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            articles_day = data["items"][0]["articles"]
            for article in articles_day:
                title = article["article"]
                views = article["views"]
                articles[title] = articles.get(title, 0) + views
        else:
            return jsonify({"error": "Wikipedia API request failed."})
    sorted_articles = sorted(articles.items(), key=lambda item: item[1], reverse=True)
    json_articles = [{"article": k, "views": v} for k, v in sorted_articles]
    return jsonify(json_articles)

# Retrieve the view count of a specific article in a month for a week
@app.route("/view-count/<article>/<year>/<month>/<week>")
def view_count_week(article, year, month, week):
    validate_input(article, year, month, week)
    days = calendar.monthrange(int(year), int(month)) [1]
    month = clean_int_less_than_10(month)
    start_day = clean_int_less_than_10(int(week) * 7)
    end_day = clean_int_less_than_10(start_day + 7)
    if end_day > days:
        end_day = days
    dateBeg = str(year) + str(month) + str(start_day) + "00"
    dateEnd = str(year) + str(month) + str(end_day) + "00"
    return view_count_helper(article, dateBeg, dateEnd, "daily")

# Retrieve the view count of a specific article for a month
@app.route("/view-count/<article>/<year>/<month>")
def view_count(article, year, month): 
    validate_input(article, year, month, None)
    days = calendar.monthrange(int(year), int(month)) [1]
    month = clean_int_less_than_10(month)
    dateBeg = str(year) + str(month) + "0100"
    dateEnd = str(year) + str(month) + str(days) + "00"
    return view_count_helper(article, dateBeg, dateEnd, "monthly")
    
def view_count_helper(article, dateBeg, dateEnd, timeScale):
    language = "en.wikipedia"
    base_url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
    # all-agents specifies the view counts for every person, can change it to users if you only want humans
    api_url = base_url + language + "/all-access/all-agents/" + article + "/" + timeScale + "/" + dateBeg + "/" + dateEnd
    response = requests.get(api_url, headers=headers)
    views = 0
    if response.status_code == 200:
        data = response.json()
        views = data["items"][0]["views"]
    else:
        return jsonify({"error": "Wikipedia API request failed."})
    return jsonify(views)

# Retrieve the day of the month where an article got the most page views
@app.route("/most-viewed-day/<article>/<year>/<month>")
def most_viewed_day(article, year, month):
    validate_input(article, year, month, None)
    language = "en.wikipedia"
    base_url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
    days = calendar.monthrange(int(year), int(month)) [1]
    month = clean_int_less_than_10(month)
    date = str(year) + str(month)
    api_url = base_url + language + "/all-access/all-agents/" + article + "/daily/" + date + "0100/" + date + str(days) + "00" 
    response = requests.get(api_url, headers=headers)
    most_viewed_day = 0
    if response.status_code == 200:
        most_viewed_day = most_viewed_day_helper(most_viewed_day, response.json())
    else:
        return jsonify({"error": "Wikipedia API request failed."})
    return jsonify(most_viewed_day)

def most_viewed_day_helper(most_viewed_day, data):
    max_views = 0
    curr_day = 0
    for day in data["items"]:
        curr_day = curr_day + 1
        views = day["views"]
        if views > max_views:
            max_views = views
            most_viewed_day = curr_day
    return most_viewed_day

def validate_input(article, year, month, week):
    try:
        if article is not None:
            if not isinstance(article, str):
                abort(404, "Invalid Article")
        # Check if the year and month are valid, Wikipedia was founded in 2001
        year = int(year)
        if year < 2001 or year > 2023:
            abort(404, "Invalid Year")
        month = int(month)
        if month < 1 or month > 12:
            abort(404, "Invalid Month")
        # If the endpoint has a week argument, convert it to integer and check if it is valid
        if week is not None:
            week = int(week)
            if week != -1:
                if week < 1 or week > 4:
                    abort(404, "Invalid Week")
    except ValueError:
        # If any argument cannot be converted to the expected type, return False
        abort(404, "Invalid Parameters")
    # If all checks pass, return True
    return True

def clean_int_less_than_10(value):
    if int(value) < 10:
        value = "0" + str(value)
    return value

if __name__ == "__main__":
    app.run(debug=True)