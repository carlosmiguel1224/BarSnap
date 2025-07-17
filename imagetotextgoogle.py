import requests
import base64
import json



def detect_text_with_requests(image_path, api_key):
    # Read and encode image
    with open(image_path, "rb") as img_file:
        encoded_image = base64.b64encode(img_file.read()).decode("utf-8")

    # Create the JSON payload
    request_body = {
        "requests": [
            {
                "image": {"content": encoded_image},
                "features": [{"type": "TEXT_DETECTION"}]
            }
        ]
    }

    # Send the request
    url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"
    response = requests.post(url, headers={"Content-Type": "application/json"}, json=request_body)

    # Handle response
    if response.status_code != 200 or "error" in response.json():
        print("Error:", response.json())
        return []

    annotations = response.json()["responses"][0].get("textAnnotations", [])
    return [entry["description"] for entry in annotations]

