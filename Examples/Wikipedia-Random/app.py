from flask import Flask, request
import requests

app = Flask(__name__)


@app.route("/get_data", methods=["GET"])
def get_data():

    num_characters = request.args.get("num_characters", default=128, type=int)
    # Get a random Wikipedia page
    random_url = "https://en.wikipedia.org/api/rest_v1/page/random/summary"

    try:
        response = requests.get(random_url)
        response.raise_for_status()

        # Extract the title and summary from the response
        data = response.json()
        title = data["title"]
        summary = data["extract"]
        retrieved_num_chars = len(summary)
        print(f"Retrieved {retrieved_num_chars} characters from Wikipedia.")

        # Create a string with the specified number of characters
        if retrieved_num_chars > num_characters:
            summary = summary[:num_characters]
        elif retrieved_num_chars < num_characters:
            zero_data = "0" * (num_characters - retrieved_num_chars)
            summary = summary + zero_data
        else:
            summary = summary
        return {"data": summary}
    except requests.exceptions.RequestException as e:
        zero_data = "0" * num_characters
        return {"data": zero_data}
