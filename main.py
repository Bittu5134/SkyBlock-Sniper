# Imports
import pandas
import numpy
import requests
import time
import asyncio
import aiohttp
import json
from tabulate import tabulate

# variables
ipt_max_price = int(input("Max Price: "))
ipt_min_price = int(input("Min Price: "))
ipt_min_profit_percent = int(input("Min Profit Percent: "))
ipt_sorting_method = int(input("Sorting Method [1]Price [2]Profit [3]Profit Percent: "))

if ipt_sorting_method == 1: ipt_sorting_method = "price"
elif ipt_sorting_method == 2: ipt_sorting_method = "profit"
elif ipt_sorting_method == 3: ipt_sorting_method = "profit_percent"

lastcheck = time.time()
url = "https://api.hypixel.net/skyblock/auctions"
reforges = [
    "\u278c",
    "\u25c6",
    "\u278a",
    "\u278e",
    "\u278b",
    "\u273f",
    "\u278d",
    " ✦",
    "⚚ ",
    " ✪",
    "✪",
    "Stiff ",
    "Lucky ",
    "Jerry's ",
    "Dirty ",
    "Fabled ",
    "Suspicious ",
    "Gilded ",
    "Warped ",
    "Withered ",
    "Bulky ",
    "Stellar ",
    "Heated ",
    "Ambered ",
    "Fruitful ",
    "Magnetic ",
    "Fleet ",
    "Mithraic ",
    "Auspicious ",
    "Refined ",
    "Headstrong ",
    "Precise ",
    "Spiritual ",
    "Moil ",
    "Blessed ",
    "Toil ",
    "Bountiful ",
    "Candied ",
    "Submerged ",
    "Reinforced ",
    "Cubic ",
    "Warped ",
    "Undead ",
    "Ridiculous ",
    "Necrotic ",
    "Spiked ",
    "Jaded ",
    "Loving ",
    "Perfect ",
    "Renowned ",
    "Giant ",
    "Empowered ",
    "Ancient ",
    "Sweet ",
    "Silky ",
    "Bloody ",
    "Shaded ",
    "Gentle ",
    "Odd ",
    "Fast ",
    "Fair ",
    "Epic ",
    "Sharp ",
    "Heroic ",
    "Spicy ",
    "Legendary ",
    "Deadly ",
    "Fine ",
    "Grand ",
    "Hasty ",
    "Neat ",
    "Rapid ",
    "Unreal ",
    "Awkward ",
    "Rich ",
    "Clean ",
    "Fierce ",
    "Heavy ",
    "Light ",
    "Mythic ",
    "Pure ",
    "Smart ",
    "Titanic ",
    "Wise ",
    "Bizarre ",
    "Itchy ",
    "Ominous ",
    "Pleasant ",
    "Pretty ",
    "Shiny ",
    "Simple ",
    "Strange ",
    "Vivid ",
    "Godly ",
    "Demonic ",
    "Forceful ",
    "Hurtful ",
    "Keen ",
    "Strong ",
    "Superior ",
    "Unpleasant ",
    "Zealous ",
]

def main(df):
    df = df[ df["bin"] == True ]
    df = df[["uuid","item_name","starting_bid","tier"]][~df["item_lore"].str.contains(r"\bfurniture\b")]
    df["item_id"] = df["item_name"].str.replace('|'.join(reforges), '', regex=True).replace(r"\[[^\]]*\] ", "", regex=True).replace(r'^\s+', '', regex=True)
    df["item_id"] = df['item_id'].astype(str) + '|' + df['tier'].astype(str)
    df = df.groupby('item_id').agg({'uuid': lambda x: list(x), 'item_name': lambda x: list(x), 'starting_bid': lambda x: list(x), 'tier': lambda x: list(x)})
    df = df[df['tier'].str.len() >= 2]


    items = pandas.DataFrame(columns=["item_name", "uuid", "price", "profit", "count", "tier", "profit_percent", "mean", "median", "std"])
    items_index = 0


    for index, row in df.iterrows():

        prices = row["starting_bid"]
        modal_index = prices.index(min(prices))
        prices = sorted(prices)

        price = prices[0]
        profit = prices[1] - price
        profit_percent = (profit / price) * 100

        if profit < 500: continue

        uuid = row["uuid"][modal_index]
        tier = row["tier"][modal_index]
        item_name = row["item_name"][modal_index]

        count = len(prices)
        mean = numpy.mean(prices).astype(int)
        std = numpy.std(prices).astype(int)
        median = numpy.median(prices).astype(int)

        items.loc[items_index] = {
            "uuid": uuid,
            "count": count,
            "item_name": item_name,
            "price": price,
            "tier": tier,
            "profit": profit,
            "profit_percent": int(profit_percent),
            "mean": mean,
            "median": median,
            "std": std,
        }

        items_index += 1

    items = items[(items["price"] >= ipt_min_price) & (items["price"] <= ipt_max_price) & (items["profit"] >= ipt_min_profit_percent)]
    items = items.sort_values(ipt_sorting_method, ignore_index=True)
    return items

def checkIfRefresh(_time):
    try:
        response = requests.get(f"{url}?page=0")
        response = response.json()

        _time_r = response["lastUpdated"]

        if _time_r > _time:
            _time = _time_r
            items = response["auctions"]
            pages = response["totalPages"]

            return _time, items, pages

        else:
            return _time, None, None

    except requests.exceptions.RequestException as e:
        return _time, None, None

async def getAllAuctions(session: aiohttp.ClientSession, page):

    response = await session.get(f"{url}?page={page}")
    pageData = json.loads(await response.text())
    return pageData["auctions"]

async def getAllPages(items: list, pages):
    async with aiohttp.ClientSession() as session:
        tasks = [getAllAuctions(session, page) for page in range(1, pages)]
        _items = await asyncio.gather(*tasks, return_exceptions=True)

        if any(isinstance(item, Exception) for item in _items):
            items = None
        else:
            items = [item for sublist in _items for item in sublist]
        return pandas.DataFrame(items)

def show_data(items :pandas.DataFrame):
    print("\n"+"="*30+"\n")
    print(tabulate(items, tablefmt="pipe", headers="keys"))
    items.to_json("pandas_final.json", indent=4)


if __name__ == "__main__":
    while True:
        lastcheck, items, pages = checkIfRefresh(lastcheck)

        if items == None:
            time.sleep(10)

        else:
            items = asyncio.run(getAllPages(items, pages))
            if items is not None:
                items = main(items)
                show_data(items)
                time.sleep(30)