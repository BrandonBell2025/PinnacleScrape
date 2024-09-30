from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd  # Import pandas for DataFrame manipulation

def scrape(url):
    # Setting up Chromedriver and passing it the url 
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.set_window_size(2560, 1440)
    driver.get(url)

    # Attempting to scrape the webpage 
    # Waiting to quit the chromedriver until desired html is loaded on the page 
    try:
        WebDriverWait(driver, 1000).until(EC.visibility_of_element_located((By.CLASS_NAME, 'label-e0291710e17e8c18f43f')))
    except:
        print("Odds didn't load in time")
    finally:
        data = driver.page_source  # Capture the HTML after JavaScript has rendered
        driver.quit()

    soup = BeautifulSoup(data, 'html.parser')
    return soup

def scrapeTeams(soup):
    # Scraping the team names for all the games where we are scraping odds
    allTeams = soup.find_all('span', class_='ellipsis event-row-participant participant-e4bea5402c4da811c6b7')
    teams = [item.text.strip() for item in allTeams]
    return teams

def scrapeOdds(soup):
    allMoneyline = soup.find_all('span', class_="price-af9054d329c985ad490f")
    moneyLineDecimal = [item.text.strip() for item in allMoneyline]
    return moneyLineDecimal

def save_to_csv(all_games):
    # Create a DataFrame to save the data
    data = []

    for teams, odds in all_games:
        # Initialize the odds as None if there aren't enough values
        spread_1 = odds[0] if len(odds) > 0 else None
        spread_2 = odds[1] if len(odds) > 1 else None
        moneyline_1 = odds[2] if len(odds) > 2 else None
        moneyline_2 = odds[3] if len(odds) > 3 else None
        over = odds[4] if len(odds) > 4 else None
        under = odds[5] if len(odds) > 5 else None

        # Format each game as required
        data.append({
            'Team 1': teams[0],
            'Team 2': teams[1],
            'Spread 1': spread_1,
            'Spread 2': spread_2,
            'Moneyline 1': moneyline_1,
            'Moneyline 2': moneyline_2,
            'Over': over,
            'Under': under
        })

    df = pd.DataFrame(data)
    df.to_csv('Pinnacle_Football.csv', index=False)  # This will overwrite the file
    print("Data saved to teams_and_odds.csv")

def main():
    url = "https://www.pinnacle.com/en/football/matchups/"
    soup = scrape(url)
    games = soup.find_all('div', class_='row-d92d06fbd3b09cc856bc')
    
    all_games = []

    for game in games:
        teams = scrapeTeams(game)
        odds = scrapeOdds(game)

        # Append the teams and odds for each game to the list
        all_games.append((teams, odds))

    # Save the collected data to a CSV file, overwriting any existing file
    save_to_csv(all_games)

if __name__ == "__main__":
    main()
