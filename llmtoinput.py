import json
import sqlite3
import pandas as pd

def extract_clean_input_terms(llm_response_str):
    """
    Cleans and extracts brand/type from raw LLM JSON string response.

    Parameters:
        llm_response_str (str): JSON string returned by LLM.

    Returns:
        List[str]: Cleaned input terms like ['titos', 'vodka', 'captain morgan']
    """
    import json

    try:
        data = json.loads(llm_response_str)
    except json.JSONDecodeError as e:
        print("Invalid JSON:", e)
        return []

    input_terms = set()

    for item in data:
        brand = item.get("brand", "").lower().replace("'", "").strip()
        type_ = item.get("type", "").lower().strip()

        if brand and brand != "unknown":
            input_terms.add(brand)
        if type_ and type_ != "unknown":
            input_terms.add(type_)

    return sorted(input_terms)


def fetch_top_cocktails_with_scores(df, db_path='cocktails.db', limit=30):
    """
    Given a DataFrame with columns ['Drink', 'Matched Inputs', 'Completeness'],
    return a list of dicts with full cocktail data and their completeness scores.
    """
    # Sort the DataFrame by completeness score, descending, and take the top results
    df_sorted = df.sort_values(by='Completeness', ascending=False).head(limit)
    
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    results = []

    for _, row in df_sorted.iterrows():
        drink_name = row['Drink']
        score = row['Completeness']

        # Query the cocktail info from the database
        cursor.execute("SELECT * FROM cocktails WHERE LOWER(name) = ?", (drink_name.lower(),))
        cocktail = cursor.fetchone()

        if cocktail:
            cocktail_data = {
                "id": cocktail[0],
                "name": cocktail[1],
                "category": cocktail[2],
                "alcoholic": cocktail[3],
                "glass": cocktail[4],
                "instructions": cocktail[5],
                "ingredients": [i.strip() for i in cocktail[6].split(",") if i.strip()],
                "thumb": cocktail[7],  
                "completeness": score
            }
            results.append(cocktail_data)

    conn.close()
    return results



def fetch_top_cocktails_with_scores_no_dupes(df, db_path='cocktails.db', limit=30):
    """
    Given a DataFrame with columns ['Drink', 'Matched Inputs', 'Completeness'],
    return a list of dicts with full cocktail data and their completeness scores,
    ensuring no duplicate cocktails (by ID).
    """
    # Sort by completeness and take the top results
    df_sorted = df.sort_values(by='Completeness', ascending=False)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    seen_ids = set()
    results = []

    for _, row in df_sorted.iterrows():
        drink_name = row['Drink']
        score = row['Completeness']

        # Query cocktail info
        cursor.execute("SELECT * FROM cocktails WHERE LOWER(name) = ?", (drink_name.lower(),))
        cocktail = cursor.fetchone()

        if cocktail:
            cocktail_id = cocktail[0]
            if cocktail_id in seen_ids:
                continue  # Skip duplicates
            seen_ids.add(cocktail_id)

            cocktail_data = {
                "id": cocktail_id,
                "name": cocktail[1],
                "category": cocktail[2],
                "alcoholic": cocktail[3],
                "glass": cocktail[4],
                "instructions": cocktail[5],
                "ingredients": [i.strip() for i in cocktail[6].split(",") if i.strip()],
                "thumb": cocktail[7],
                "completeness": score
            }
            results.append(cocktail_data)

        if len(results) >= limit:
            break  # Stop once limit is reached

    conn.close()
    return results


def fetch_top_cocktails_with_scores_no_dupes_with_label(df, db_path='cocktails.db', limit=30):
    """
    Given a DataFrame with columns ['Drink', 'Matched Inputs', 'Completeness', 'Label'],
    return a list of dicts with full cocktail data, their completeness scores, and labels,
    ensuring no duplicate cocktails (by ID).
    """
    # Sort by completeness and take the top results
    df_sorted = df.sort_values(by='Completeness', ascending=False)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    seen_ids = set()
    results = []

    for _, row in df_sorted.iterrows():
        drink_name = row['Drink']
        score = row['Completeness']
        label = row['Label']  # Get label from DataFrame

        # Query cocktail info
        cursor.execute("SELECT * FROM cocktails WHERE LOWER(name) = ?", (drink_name.lower(),))
        cocktail = cursor.fetchone()

        if cocktail:
            cocktail_id = cocktail[0]
            if cocktail_id in seen_ids:
                continue  # Skip duplicates
            seen_ids.add(cocktail_id)

            cocktail_data = {
                "id": cocktail_id,
                "name": cocktail[1],
                "category": cocktail[2],
                "alcoholic": cocktail[3],
                "glass": cocktail[4],
                "instructions": cocktail[5],
                "ingredients": [i.strip() for i in cocktail[6].split(",") if i.strip()],
                "thumb": cocktail[7],
                "completeness": score,
                "completeness_label": label  # ✅ Add label to response
            }
            results.append(cocktail_data)

        if len(results) >= limit:
            break  # Stop once limit is reached

    conn.close()
    return results
