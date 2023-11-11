# %%
import pandas
df_raw = pandas.read_json("raw_data.json")

# %%
# %%time
# Variables

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

df = df_raw.query("bin == False")
df = df[["uuid","item_name","starting_bid","tier"]][~df["item_lore"].str.contains(r"\bfurniture\b")]
df["item_id"] = df["item_name"].str.replace('|'.join(reforges), '', regex=True).replace(r"\[[^\]]*\] ", "", regex=True).replace(r'^\s+', '', regex=True)
df["item_id"] = df['item_id'].astype(str) + '|' + df['tier'].astype(str)
df = df.groupby('item_id').agg({'uuid': lambda x: list(x), 'item_name': lambda x: list(x), 'starting_bid': lambda x: list(x), 'tier': lambda x: list(x)})


# %%
# print(df.loc["Arack|EPIC"].to_frame().to_json("pandas_final.json", indent=4))
from pprint import pprint
for column in df.columns:
    data = df[column]
    pprint(f"Column: {column}, Data: {data.describe()}")

# %%
print(len(df_raw))
print(len(df))
df.to_json("pandas_final.json", indent=4)


