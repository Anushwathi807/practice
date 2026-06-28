import requests
from flask import Flask, jsonify, request
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

def fetch_numbers(url):
    """Fetch numbers from a single URL with timeout handling."""
    try:
        response = requests.get(url, timeout=0.5)
        data = response.json()
        return data.get('numbers', [])
    except requests.exceptions.Timeout:
        print(f"Timeout: {url} did not respond in 500ms")
        return []
    except requests.exceptions.ConnectionError:
        print(f"ConnectionError: could not reach {url}")
        return []
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []

@app.route('/numbers', methods=['GET'])
def numbers():
    """
    GET /numbers?url=<url1>&url=<url2>&url=<url3>
    Fetches numbers from all URLs concurrently,
    merges them, removes duplicates, returns sorted list.
    """
    urls = request.args.getlist('url')

    if not urls:
        return jsonify({"error": "no urls provided"}), 400

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(fetch_numbers, urls))

    all_numbers = []
    for result in results:
        all_numbers.extend(result)

    unique_sorted = sorted(set(all_numbers))
    return jsonify({"numbers": unique_sorted})

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "route not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
