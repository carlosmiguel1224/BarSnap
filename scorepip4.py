import sqlite3
from collections import defaultdict, deque
from itertools import chain, combinations
import pandas as pd
from all_ingredientsflatlist import ALL_INGREDIENTS

# --- CONFIG ---
DB_PATH = 'cocktails.db'
TABLE = 'cocktails'


CHAIN_MAP = {
  "151 proof rum": [
    "rum"
  ],
  "7-up": [
    "soda"
  ],
  "7up": [
    "soda"
  ],
  "absinthe": [
    "herbal liqueur"
  ],
  "absolut": [
    "vodka"
  ],
  "absolut citron": [
    "flavored vodka"
  ],
  "absolut kurant": [
    "flavored vodka"
  ],
  "absolut peppar": [
    "flavored vodka"
  ],
  "absolut vodka": [
    "vodka"
  ],
  "agave syrup": [
    "syrup"
  ],
  "allspice": [
    "spice"
  ],
  "almond flavoring": [
    "sweetener"
  ],
  "amaretto": [
    "liqueur"
  ],
  "amaro montenegro": [
    "herbal liqueur"
  ],
  "angostura bitters": [
    "bitters"
  ],
  "anis": [
    "herbal liqueur"
  ],
  "anisette": [
    "liqueur",
    "herbal liqueur"
  ],
  "aperol": [
    "herbal liqueur"
  ],
  "apple": [
    "fruit"
  ],
  "apple brandy": [
    "brandy"
  ],
  "apple juice": [
    "fruit juice"
  ],
  "applejack": [
    "brandy"
  ],
  "appleton estate": [
    "rum"
  ],
  "apricot brandy": [
    "brandy"
  ],
  "apricot nectar": [
    "fruit juice"
  ],
  "asafoetida": [
    "spice"
  ],
  "a\u00f1ejo rum": [
    "rum"
  ],
  "bacardi": [
    "rum"
  ],
  "bacardi limon": [
    "white rum"
  ],
  "baileys": [
    "cream liqueur"
  ],
  "banana": [
    "fruit"
  ],
  "bang": [
    "energy drink"
  ],
  "beefeater": [
    "gin"
  ],
  "beer": [],
  "belvedere": [
    "vodka"
  ],
  "benedictine": [
    "liqueur",
    "herbal liqueur"
  ],
  "bitter lemon": [
    "bitters"
  ],
  "bitters": [],
  "black pepper": [
    "spice"
  ],
  "black sambuca": [
    "liqueur"
  ],
  "blackberries": [
    "fruit"
  ],
  "blackstrap rum": [
    "rum"
  ],
  "blended scotch": [
    "whiskey"
  ],
  "blended whiskey": [
    "whiskey"
  ],
  "blood orange": [
    "fruit"
  ],
  "blue curacao": [
    "liqueur"
  ],
  "bombay sapphire": [
    "gin"
  ],
  "bourbon": [
    "whiskey"
  ],
  "brandy": [],
  "brown sugar": [
    "sweetener"
  ],
  "bulleit": [
    "whiskey"
  ],
  "butter": [
    "sweetener"
  ],
  "butterscotch schnapps": [
    "liqueur"
  ],
  "cachaca": [],
  "campari": [
    "herbal liqueur"
  ],
  "canadian whisky": [
    "whiskey"
  ],
  "captain morgan": [
    "spiced rum"
  ],
  "captain morgan white rum": [
    "white rum"
  ],
  "caramel coloring": [
    "sweetener"
  ],
  "carbonated soft drink": [
    "soda"
  ],
  "carbonated water": [
    "soda"
  ],
  "cardamom": [
    "spice"
  ],
  "cayenne pepper": [
    "spice"
  ],
  "celery salt": [
    "spice"
  ],
  "chambord raspberry liqueur": [
    "liqueur",
    "fruit liqueur"
  ],
  "champagne": [
    "sparkling wine"
  ],
  "cherries": [
    "fruit"
  ],
  "cherry": [
    "fruit"
  ],
  "cherry brandy": [
    "liqueur",
    "fruit liqueur"
  ],
  "cherry heering": [
    "liqueur",
    "fruit liqueur"
  ],
  "cherry juice": [
    "fruit juice"
  ],
  "cherry liqueur": [
    "liqueur",
    "fruit liqueur"
  ],
  "cherry vodka": [
    "flavored vodka",
    "vodka"
  ],
  "chocolate liqueur": [
    "liqueur"
  ],
  "chocolate syrup": [
    "sweetener"
  ],
  "cider": [
    "fermented drink"
  ],
  "cinnamon": [
    "spice"
  ],
  "citrus vodka": [
    "flavored vodka",
    "vodka"
  ],
  "cloves": [
    "spice"
  ],
  "club soda": [
    "soda"
  ],
  "coca-cola": [
    "soda"
  ],
  "cocoa powder": [
    "spice"
  ],
  "coconut liqueur": [
    "liqueur",
    "fruit liqueur"
  ],
  "coffee brandy": [
    "liqueur"
  ],
  "coffee liqueur": [
    "liqueur"
  ],
  "cognac": [
    "liqueur",
    "brandy"
  ],
  "cointreau": [
    "triple sec",
    "liqueur"
  ],
  "coke": [
    "soda"
  ],
  "condensed milk": [
    "sweetener"
  ],
  "coriander": [
    "spice"
  ],
  "corn syrup": [
    "sweetener"
  ],
  "corona": [
    "beer"
  ],
  "courvoisier": [
    "brandy"
  ],
  "cranberry juice": [
    "fruit juice"
  ],
  "cranberry vodka": [
    "flavored vodka",
    "vodka"
  ],
  "cream of coconut": [
    "syrup"
  ],
  "creme de banane": [
    "liqueur",
    "fruit liqueur"
  ],
  "creme de cacao": [
    "liqueur"
  ],
  "creme de cassis": [
    "liqueur",
    "fruit liqueur"
  ],
  "creme de menthe": [
    "liqueur"
  ],
  "creme de mure": [
    "liqueur",
    "fruit liqueur"
  ],
  "crown royal": [
    "whiskey"
  ],
  "cucumber": [
    "fruit"
  ],
  "cumin seed": [
    "spice"
  ],
  "daiquiri mix": [
    "mix"
  ],
  "dark rum": [
    "rum"
  ],
  "demerara sugar": [
    "sweetener"
  ],
  "don julio": [
    "tequila"
  ],
  "dr pepper": [
    "soda"
  ],
  "dr. pepper": [
    "soda"
  ],
  "drambuie": [
    "liqueur"
  ],
  "dry gin": [
    "gin"
  ],
  "energy drink": [],
  "equal": [
    "sweetener"
  ],
  "espolon": [
    "tequila"
  ],
  "fermented drink": [],
  "flavored vodka": [
    "vodka"
  ],
  "fresca": [
    "soda"
  ],
  "fruit": [],
  "fruit juice": [],
  "gin": [],
  "ginger ale": [
    "soda"
  ],
  "grand marnier": [
    "triple sec",
    "liqueur"
  ],
  "grape": [
    "fruit"
  ],
  "grape soda": [
    "soda"
  ],
  "grapefruit juice": [
    "fruit juice"
  ],
  "grenadine": [
    "syrup"
  ],
  "grey goose": [
    "vodka"
  ],
  "guinness stout": [
    "beer"
  ],
  "hendrick's": [
    "gin"
  ],
  "hennessy": [
    "brandy"
  ],
  "herbal liqueur": [],
  "herradura": [
    "tequila"
  ],
  "irish whiskey": [
    "whiskey"
  ],
  "jack daniels": [
    "whiskey"
  ],
  "jagermeister": [
    "herbal liqueur"
  ],
  "jameson": [
    "whiskey"
  ],
  "jim beam": [
    "whiskey"
  ],
  "johnnie walker": [
    "whiskey"
  ],
  "jose cuervo": [
    "tequila"
  ],
  "kahlua": [
    "coffee liqueur"
  ],
  "ketel one": [
    "vodka"
  ],
  "kiwi": [
    "fruit"
  ],
  "lager": [
    "beer"
  ],
  "lemon": [
    "fruit"
  ],
  "lemon juice": [
    "fruit juice"
  ],
  "lemon vodka": [
    "flavored vodka",
    "vodka"
  ],
  "lemon-lime soda": [
    "soda"
  ],
  "light rum": [
    "rum"
  ],
  "lime": [
    "fruit"
  ],
  "liqueur": [],
  "maker's mark": [
    "whiskey"
  ],
  "malibu": [
    "rum"
  ],
  "malibu rum": [
    "rum"
  ],
  "mango": [
    "fruit"
  ],
  "maple syrup": [
    "sweetener"
  ],
  "mix": [],
  "monster": [
    "energy drink"
  ],
  "mount gay": [
    "rum"
  ],
  "mountain dew": [
    "soda"
  ],
  "mr & mrs t": [
    "mix"
  ],
  "nos": [
    "energy drink"
  ],
  "nutmeg": [
    "spice"
  ],
  "old tom gin": [
    "gin"
  ],
  "orange": [
    "fruit"
  ],
  "orange bitters": [
    "bitters"
  ],
  "orange juice": [
    "fruit juice"
  ],
  "orange vodka": [
    "flavored vodka",
    "vodka"
  ],
  "orgeat syrup": [
    "syrup"
  ],
  "overproof rum": [
    "rum"
  ],
  "papaya": [
    "fruit"
  ],
  "passion fruit": [
    "fruit"
  ],
  "passion fruit juice": [
    "fruit juice"
  ],
  "passion fruit syrup": [
    "syrup"
  ],
  "patron": [
    "tequila"
  ],
  "peach": [
    "fruit"
  ],
  "peach vodka": [
    "flavored vodka",
    "vodka"
  ],
  "pepper": [
    "spice"
  ],
  "pepsi": [
    "soda"
  ],
  "pepsi cola": [
    "soda"
  ],
  "peychaud bitters": [
    "bitters"
  ],
  "pineapple": [
    "fruit"
  ],
  "pineapple syrup": [
    "syrup"
  ],
  "plymouth gin": [
    "gin"
  ],
  "pomegranate juice": [
    "fruit juice"
  ],
  "powdered sugar": [
    "sweetener"
  ],
  "prosecco": [
    "sparkling wine"
  ],
  "raspberry syrup": [
    "syrup"
  ],
  "raspberry vodka": [
    "flavored vodka",
    "vodka"
  ],
  "red bull": [
    "energy drink"
  ],
  "remy martin": [
    "brandy"
  ],
  "rockstar": [
    "energy drink"
  ],
  "ron zacapa": [
    "rum"
  ],
  "root beer": [
    "soda"
  ],
  "rose's lime juice": [
    "fruit juice"
  ],
  "rum": [],
  "rye whiskey": [
    "whiskey"
  ],
  "sambuca": [
    "herbal liqueur"
  ],
  "scotch": [
    "whiskey"
  ],
  "smirnoff": [
    "vodka"
  ],
  "soda": [],
  "soda water": [
    "soda"
  ],
  "sparkling wine": [],
  "spice": [],
  "spiced rum": [
    "rum"
  ],
  "splenda": [
    "sweetener"
  ],
  "sprite": [
    "soda"
  ],
  "stevia": [
    "sweetener"
  ],
  "stolichnaya": [
    "vodka"
  ],
  "strawberries": [
    "fruit"
  ],
  "sugar": [
    "sweetener"
  ],
  "surge": [
    "soda"
  ],
  "sweet'n low": [
    "sweetener"
  ],
  "sweetener": [],
  "syrup": [],
  "tanqueray": [
    "gin"
  ],
  "tennessee whiskey": [
    "whiskey"
  ],
  "titos": [
    "vodka"
  ],
  "tonic water": [
    "soda"
  ],
  "triple sec": [
    "liqueur"
  ],
  "truvia": [
    "sweetener"
  ],
  "vanilla vodka": [
    "flavored vodka",
    "vodka"
  ],
  "vodka": [],
  "whiskey": [],
  "whisky": [
    "whiskey"
  ],
  "white rum": [
    "light rum",
    "rum"
  ],
  "wild turkey": [
    "whiskey"
  ],
  "zing zang": [
    "mix"
  ]
}

from collections import defaultdict, deque
from itertools import chain, combinations
import sqlite3
import pandas as pd

# Assumes CHAIN_MAP is already loaded earlier in your code
# CHAIN_MAP = {...}

# --- Build Downward Mapping ---
DOWNWARD_MAP = defaultdict(list)
for general, specifics in CHAIN_MAP.items():
    for specific in specifics:
        DOWNWARD_MAP[general].append(specific)
for item in CHAIN_MAP:
    DOWNWARD_MAP[item]  # Ensure all items are keys

# Get all downward variants
def get_all_descendants(term):
    term = term.lower()
    visited = set()
    queue = deque([term])
    while queue:
        current = queue.popleft()
        if current not in visited:
            visited.add(current)
            queue.extend(DOWNWARD_MAP.get(current, []))
    return visited

# Normalize DB ingredients
def normalize_ingredients(ingredients_str):
    return [i.strip().lower() for i in ingredients_str.split(',') if i.strip()]

# Generate powerset of input_terms (excluding empty set)
def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s) + 1))

# Map number of missing ingredients to completeness label
def get_completeness_label(missing_count):
    if missing_count == 0:
        return "Complete"
    elif missing_count == 1:
        return "Almost"
    elif missing_count == 2:
        return "Close"
    else:
        return None  # No label for 3+ missing

# Match function using completeness score and label
def match_with_completeness(db_ingredients, subset):
    ingredients = normalize_ingredients(db_ingredients)
    matched_terms = set()
    for term in subset:
        variants = get_all_descendants(term)
        for var in variants:
            if var in ingredients:
                matched_terms.add(var)
                break
        else:
            return None, 0.0, None  # skip if one required term not matched

    matched_count = len(matched_terms)
    total_required = len(ingredients)
    missing_count = total_required - matched_count
    completeness_score = matched_count / total_required if total_required else 0
    label = get_completeness_label(missing_count)
    return True, completeness_score, label

# Run query and return ranked matches with scores and labels
def run_ranked_query(input_terms):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {TABLE}")
    rows = cur.fetchall()
    conn.close()

    results = []
    for subset in powerset(input_terms):
        subset = list(subset)
        for row in rows:
            ingredients_str = row[6]
            matched, score, label = match_with_completeness(ingredients_str, subset)
            if matched:
                results.append((row[1], subset, score, label))  # name, input, score, label

    # Sort: highest completeness first, then longest match
    results = sorted(results, key=lambda x: (-x[2], -len(x[1])))
    return results


def filter_known_ingredients(input_ingredients: list[str]) -> list[str]:
    """Return only the ingredients that are in the known all_ingredients list."""
    known_set = set(ALL_INGREDIENTS)
    return [item for item in input_ingredients if item.lower() in known_set]



# --- Testing section ---
if __name__ == "__main__":
    input_terms = ['absolut vodka', 'gin', 'tonic water', 'vodka']  # Replace with your test inputs
    results = run_ranked_query(input_terms)
    df = pd.DataFrame(results, columns=["Drink", "Matched Inputs", "Completeness", "Label"])
    print(df.to_string(index=False))
