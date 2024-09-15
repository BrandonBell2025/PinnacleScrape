from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup
import time

def scrape(url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    time.sleep(3)  # Wait for 5 seconds to allow the page to load

    data = driver.page_source  # Capture the HTML after JavaScript has rendered
    driver.quit()
    soup = BeautifulSoup(data, 'html.parser')

    return soup

def scrapeOdds(soup):
    allOdds = soup.find_all('span', class_='label-e0291710e17e8c18f43f')
    odds = [item.text.strip() for item in allOdds]
    return odds

def scrapeTeams(soup):
    allTeams = soup.find_all('span', class_='ellipsis event-row-participant participant-e4bea5402c4da811c6b7')
    teams = [item.text.strip() for item in allTeams]
    return teams

def display_matchups(teams, odds):
    # Ensure teams and odds are grouped in pairs
    for i in range(0, len(teams), 2):
        team1 = teams[i]
        team2 = teams[i + 1]
        odd1 = odds[i]
        odd2 = odds[i + 1]
        print(f"{team1} vs {team2}: {odd1}, {odd2}")

def main ():
    url = "https://www.pinnacle.com/en/football/matchups/"
    soup = scrape(url)
    games = soup.find_all('div', class_='row-d92d06fbd3b09cc856bc')
    for game in games:
        odds = scrapeOdds(game)
        teams = scrapeTeams(game)
        display_matchups(teams, odds)

if __name__ == "__main__":
    main()