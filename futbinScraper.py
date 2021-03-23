import requests
from bs4 import BeautifulSoup
import re
import csv
import time
import random

header = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0"
}
url = "https://www.futbin.com/21/players?version=gold_all&page="
player_information = []

# Loop through each page
for page in range(1, 138):
    FBin = requests.get(url + str(page), headers=header)
    soup = BeautifulSoup(FBin.text, "html.parser")
    tbody = soup.find("tbody")
    players = tbody.find_all("tr")
    # For each individual player/card
    for individual in players:
        name = individual.find("a", class_="player_name_players_table").text
        league = individual.find("span", class_="players_club_nation").find_all("a")[0][
            "data-original-title"
        ]
        country = individual.find("span", class_="players_club_nation").find_all("a")[
            1
        ]["data-original-title"]
        price = individual.find(
            "span", class_="ps4_color font-weight-bold").text
        rating = individual.find("td", class_="").text
        base_stats = individual.find_all("td")[-2].text
        total_stats = individual.find_all("td")[-1].text
        popularity = individual.find_all("td")[-3].text
        weight = individual.find_all("td")[-4].find_all("div")[1].text
        weight = re.search("\(.+kg", weight).group()[1:-2]
        height = individual.find_all("td")[-4].find_all("div")[0].text
        height = height[1: height.find("cm")]
        pace = individual.find_all("td")[8].text
        shooting = individual.find_all("td")[9].text
        dribling = individual.find_all("td")[10].text
        defending = individual.find_all("td")[11].text
        physicality = individual.find_all("td")[12].text
        weak_foot = individual.find_all("td")[6].text
        skills = individual.find_all("td")[5].text
        card_type = individual.find_all("td")[3].text
        position = individual.find_all("td")[2].text
        player_information.append(
            [
                name,
                league,
                country,
                position,
                price,
                rating,
                base_stats,
                total_stats,
                popularity,
                weight,
                height,
                pace,
                shooting,
                dribling,
                defending,
                physicality,
                weak_foot,
                skills,
                card_type,
            ]
        )
    # Conservative sleep time
    time.sleep(random.randint(10, 15))
    # print("done page: " + str(page))

# Write to csv file
with open("futbin.csv", "w", newline="", encoding="utf-16") as f:
    writer = csv.writer(f)
    writer.writerow(
        [
            "name",
            "league",
            "country",
            "position",
            "price",
            "rating",
            "base_stats",
            "total_stats",
            "popularity",
            "weight",
            "height",
            "pace",
            "shooting",
            "dribling",
            "defending",
            "physicality",
            "weak_foot",
            "skills",
            "card_type",
        ]
    )
    writer.writerows(player_information[0:269])
