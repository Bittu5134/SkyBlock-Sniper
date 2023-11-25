## SKYBLOCK SNIPER 🔫

**This is a small project I made while trying to find different uses for the [Hypixel API](https://api.hypixel.net).**
**This script will get the data of all the items currently being auctioned in the SkyBlock Auction house(always around 50-60k). Then it will use different methods to sort and filter the data and give you a list of items you can purchase for low and then sell for higher prices in the Auction.**

### How to use

- Install all the dependencies with this command: `python -m pip install -r requirements.txt`.
- Run the `main.py` file.
- You will be prompted to provide filtering parameters.
```bash
Max Price: 2570000 # The maxing price of the items
Min Price: 2000
Min Profit Percent: 57
Sorting Method [1]Price [2]Profit [3]Profit Percent: 1
``` 
- After filling the parameters, it will take some time to get the data.
- It will then filter the data and give you a list of items you can purchase for low and then sell for higher prices in the Auction.

|     | item_name                                 | uuid                             |   price |   profit |   count | tier      |   profit_percent |      mean |    median |       std |
|----:|:------------------------------------------|:---------------------------------|--------:|---------:|--------:|:----------|-----------------:|----------:|----------:|----------:|
|   0 | ◆ Pestilence Rune I                       | 6d39d589491a4a4a8300e120cec090ed |    2311 |      789 |      16 | RARE      |               34 |    297926 |     50000 |    644689 |
|   1 | ◆ Golden Rune I                           | 7e7f364fdfef4789a8aac4a24cad3f00 |    2500 |     6500 |       8 | EPIC      |              260 |     40524 |     29500 |     34102 |
|   2 | Tall Holiday Tree                         | 968e143764404fc7807a68d660347609 |    4000 |     1000 |      14 | COMMON    |               25 |    258214 |     22500 |    764771 |
|   3 | ◆ Hot Rune I                              | 27e193a0e4384270a11eb4ac75ac9b5f |    4000 |     1000 |       8 | UNCOMMON  |               25 |  13140378 |     13000 |  32870294 |
|   4 | Music Disc - Blocks                       | 5bb1a1d1c8bb45c3830bf260471a6035 |    4000 |     1000 |       3 | UNCOMMON  |               25 |     16333 |      5000 |     16739 |
|   5 | ◆ Lava Rune I                             | 662d61a04a24464c8bbbf25b7cb0dd02 |    5000 |    75000 |      11 | COMMON    |             1500 |   1393999 |    500000 |   2762135 |

- you can use the `/viewah {UUID}` command In-Game to view the item in the auction.