import re
import asyncio
import json
import time

import aiohttp
import requests

url = "https://api.hypixel.net/skyblock/auctions"
pages = 0
items = []
lastcheck = 0
reforges = [
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
        return items


class Sorting:
    @staticmethod
    def start(data):
        data = Sorting.newList(data)
        return data

    @staticmethod
    def newList(data):
        _data = {}
        for item in data:
            if Sorting.isValid(item):
                item = {
                    "tier": item["tier"],
                    "uuid": item["uuid"],
                    "name": item["item_name"],
                    "price": item["starting_bid"],
                    "id": Sorting.itemID(item["item_name"]),
                }
                index = item["id"] + "|" + item["tier"]
                if index in _data:
                    _data[index].append(item)
                else:
                    _data[index] = []

        return _data
    

    @staticmethod
    def isValid(item):
        if (
            item["bin"] == True
            and "Skin" not in item["item_name"]
            and "Cake" not in item["item_name"]
            and "Crab Hat" not in item["item_name"]
            and "Furniture" not in item["item_lore"]
        ):
            return True
        else:
            return False


    @staticmethod
    def itemID(name):
        name = re.sub("\[[^\]]*\] ", "", name)
        for reforge in reforges:
            name = name.replace(reforge, "")
        return name


class snipeAuction:
    @staticmethod
    def start(data):
        _data = []
        for items in data:
            if len(data[items]) >= 2:
                snipe = snipeAuction.quickSort(data[items])
                if snipe != None:
                    _data.append(snipe)

        return _data

    @staticmethod
    def quickSort(items):
        items = sorted(items, key=lambda k: k["price"])

        item1 = items[0]
        item2 = items[1]

        profit = item2["price"] - item1["price"]
        profitPercent = round((profit * 100) / item1["price"])

        if profitPercent < 1:
            return

        return {
            "name1": item1["name"],
            "name2": item2["name"],
            "price1": item1["price"],
            "price2": item2["price"],
            "uuid1": item1["uuid"],
            "uuid2": item2["uuid"],
            "tier": item1["tier"],
            "profit": profit,
            "profitPercent": profitPercent,
        }


if __name__ == "__main__":
    while True:
        lastcheck, items, pages = checkIfRefresh(lastcheck)

        if items == None:
            time.sleep(10)

        else:
            start_time = time.time()#TEMP
            items = asyncio.run(getAllPages(items, pages))
            if items is not None:
                items = Sorting.start(items)
                items = snipeAuction.start(items)
                print("Total time taken:", time.time() - start_time) #TEMP


###################################################################################

                items = sorted(items, key=lambda k: k["profitPercent"])
                with open("client/items.json", "w", encoding="utf-8") as file:
                    file.write(json.dumps(items, indent=4))
                print("Total Items:", len(items))
                time.sleep(30)

###################################################################################