from scorepip4 import *
from llmtest import *
from llmtoinput import *
from imagetotextgoogle import *
from safety import *
import os
from dotenv import load_dotenv

load_dotenv()

def image_to_results(image_path, API_KEY, user_ingredients=None):
    
    if user_ingredients == None:
        user_ingredients = []
    ocr_labels = detect_text_with_requests(image_path, API_KEY)
    #print(ocr_labels)
    clean_ocr_labels = filter_meaningful_multiline_block(ocr_labels)
    prompt = f"""You are an expert in interpreting OCR output from liquor bottles, mixers, and related drink products.
Your job is to match each OCR string to the most likely brand and ingredient type.

You have broad knowledge of real-world alcohol brands, mixers, sodas, juices, and ingredients.
Use all of your knowledge — not just the examples below — to classify the input.

Each item must return:

- The most likely brand name (or product name)
- The type of drink ingredient it represents (e.g., "vodka", "rum", "beer", "mixer", "juice", etc.)
- If you're not confident in a match, return "unknown" for both fields.

Here are a few examples (not a complete list):

- Tanqueray → gin
- Tito's → vodka
- Captain Morgan → rum
- 7-Up → mixer
- Coca-Cola → mixer
- Baileys → Irish cream
- Red Bull → mixer
- Beer → beer
- Wine → wine
- Jack Daniel's → whiskey
- Malibu → rum
- Aperol → herbal liqueur

Detected OCR Labels:
{clean_ocr_labels}

Return the result as a JSON array like:

[
  {{ "input": "Baile", "brand": "Baileys", "type": "Irish cream" }},
  {{ "input": "7 Up", "brand": "7-Up", "type": "mixer" }},
  {{ "input": "Beer", "brand": "Beer", "type": "beer" }}
]

Only return the full valid JSON array. No extra characters, no trailing commas, and no text before or after.
"""
    
    print(f"Cleaned ocr: {clean_ocr_labels}")
    response = send_prompt(prompt)
    print(response)
    raw_input = extract_clean_input_terms(pre_parser(response))
    safe_input = safe_json_parse(raw_input)

    combined_ingredients = list(set(safe_input + user_ingredients))

    # Run the cocktail matcher
    df = run_ranked_query(combined_ingredients)
   
    df = pd.DataFrame(df, columns=["Drink", "Matched Inputs", "Completeness", "Label"])
    
    # Display results
    #print(df.to_string(index=False))
    results = fetch_top_cocktails_with_scores_no_dupes_with_label(df)
    return results


if __name__ == "__main__":
    print("hello world")


