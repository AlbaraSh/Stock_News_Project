import requests
from tkinter import *

FONT = ('Courier', 35, "bold")
BG_COLOR = "#A1FEFF"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "LYM7JFSHTGXKW3WW"
NEWS_API_KEY = "0bee828957a54310abebcf855b333639"

stock_name = "TSLA"
company_name = "Tesla Inc"

# methods used in UI
def confirm():
    global stock_name
    stock_name = user_input.get()
    if user_input.get() == "":
        stock_name = "TSLA"
    overview_params = {
        "function": "OVERVIEW",
        "symbol": stock_name,
        "apikey": STOCK_API_KEY,
    }
    overview_response = requests.get(STOCK_ENDPOINT, params=overview_params)
    overview_data = overview_response.json()
    global company_name
    company_name = overview_data["Name"]
    label.config(text=(stock_name + up_down))
    print(overview_data["Name"])


def stock_data():
    # get yesterday's closing stock price
    stock_params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": stock_name,
        "apikey": STOCK_API_KEY,
    }

    response = requests.get(STOCK_ENDPOINT, params=stock_params)
    data = response.json()["Time Series (Daily)"]
    data_list = [value for (key, value) in data.items()]
    yesterday_data = data_list[0]
    yesterday_closing_price = yesterday_data["4. close"]
    print(yesterday_closing_price)

    # get the day before yesterday's closing stock price
    day_before_yesterday_data = data_list[1]
    day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
    print(day_before_yesterday_closing_price)

    difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)

    if difference > 0:
        global up_down
        up_down = "🔺"

    diff_percent = round((difference / float(yesterday_closing_price)) * 100)
    print(diff_percent)

    # getting news articles
    if abs(diff_percent) > 0:
        news_params = {
            "apiKey": NEWS_API_KEY,
            "qInTitle": company_name,
        }

        news_response = requests.get(NEWS_ENDPOINT, params=news_params)
        articles = news_response.json()["articles"]

        three_articles = articles[:3]
        print(three_articles)

        # formatting the articles for the message
        formatted_articles = [
            f"{stock_name}: {diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}"
            for article in three_articles]
        print(formatted_articles)

        for article in formatted_articles:
            print(article)


# setting up Tkinter UI
# setting up window
window = Tk()
window.title("Stock Market")
window.config(width=300, height=250, padx=50, pady=50, bg=BG_COLOR)

# current stock Label

up_down = "🔻"
label = Label(text=(stock_name + up_down), bg=BG_COLOR, highlightthickness=0, font=FONT, fg="black")
label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# setting up user input
user_input = Entry(window, bd=5, width=20, font=('Courier', 15, "bold"))
user_input.grid(row=1, column=0, columnspan=2, padx=20, pady=20)

# confirm button
confirm_button = Button(text="Confirm?", highlightthickness=0, command=confirm)
confirm_button.grid(row=2, column=0, padx=20, pady=20)

# phone message button
send_button = Button(text="Send Info?", highlightthickness=0, command=stock_data)
send_button.grid(column=1, row=2, padx=20, pady=20)

stock_data()

window.mainloop()
