import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()


# You can also move this to an environment variable
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

def send_prompt(message_content, model="qwen/qwen-2.5-72b-instruct:free", system_prompt=None):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": message_content})

    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": 30000,
    }

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        data=json.dumps(payload)
    )

    try:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print("❌ API Error:", e)
        print("Response:", response.text)
        return None


def main():
    image_path = "IMG_8921.png"
    ocr_labels = run_easyocr(image_path)


    prompt = message_content = f"""
You are an expert in interpreting OCR output from liquor bottles and matching it to known alcohol brands and drink ingredient types.

Here is a dictionary of known brands and the type of drink each represents:
- Tanqueray → gin
- Espolon → tequila
- Baileys → Irish cream
- Tito's → vodka
- Cointreau → triple sec
- Absolut → vodka
- Captain Morgan → rum
- Coca-Cola → mixer
- Orange Juice → juice
- Sprite → mixer
- Jack Daniel's → whiskey
- Jameson → whiskey
- Maker's Mark → bourbon
- Bulleit → bourbon
- Johnnie Walker → scotch
- Chivas Regal → scotch
- Crown Royal → whiskey
- Grey Goose → vodka
- Smirnoff → vodka
- Ketel One → vodka
- Stolichnaya → vodka
- Belvedere → vodka
- Don Julio → tequila
- Jose Cuervo → tequila
- Patrón → tequila
- 1800 → tequila
- Hornitos → tequila
- Bacardi → rum
- Malibu → rum
- Mount Gay → rum
- Ron Diplomatico → rum
- Bombay Sapphire → gin
- Hendrick's → gin
- Beefeater → gin
- Gordon's → gin
- Grand Marnier → triple sec
- Amaretto Disaronno → almond liqueur
- Kahlúa → coffee liqueur
- Frangelico → hazelnut liqueur
- Chambord → raspberry liqueur
- Campari → bitter liqueur
- Aperol → aperitif
- Midori → melon liqueur
- Jägermeister → herbal liqueur
- Martini & Rossi → vermouth
- Dolin → vermouth
- Noilly Prat → vermouth
- Angostura → bitters
- Pepsi → mixer
- Canada Dry → mixer
- Schweppes → mixer
- Red Bull → mixer
- Club Soda → mixer
- Tonic Water → mixer
- Ginger Ale → mixer
- Cranberry Juice → juice
- Pineapple Juice → juice
- Lime Juice → juice
- Lemon Juice → juice
- Grenadine → syrup
- Simple Syrup → syrup
- Agave → syrup


Use this dictionary to identify and correct any misspelled or partial brand names detected by OCR.

If you're not confident in a match, return "unknown".

Detected OCR Labels:
{ocr_labels}

Return the result as a JSON array like:
[
  {{ "input": "Baile", "brand": "Baileys", "type": "Irish cream" }},
  ...
]
"""
    response = send_prompt(prompt)
    print(response)

if __name__ == "__main__":
    main()