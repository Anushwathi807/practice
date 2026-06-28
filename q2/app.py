import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def find_prefix(self, word):
        node = self.root
        prefix = ""
        prev_node = None
        for char in word:
            if char not in node.children:
                return None
            prev_node = node
            node = node.children[char]
            prefix += char
            if len(prev_node.children) > 1 or node.is_end:
                return prefix
        return prefix

WORD_LIST = [
    "bonfire", "bonsai", "bonus", "bond", "bone",
    "bonnet", "bongo", "bonito", "bonanza", "bondage",
    "bonder", "bonefish", "bonehead", "boney", "bonfire",
    "boniface", "bonk", "bonny", "bonsai", "bonus"
]

trie = Trie()
for word in WORD_LIST:
    trie.insert(word)

@app.route('/prefix', methods=['GET'])
def prefix():
    """
    GET /prefix?keywords=bonfire,bonsai
    Returns shortest unique prefix for each keyword.
    """
    keywords_param = request.args.get('keywords', '')
    if not keywords_param:
        return jsonify({"error": "no keywords provided"}), 400

    keywords = keywords_param.split(',')
    results = []

    for keyword in keywords:
        keyword = keyword.strip()
        prefix_found = trie.find_prefix(keyword)
        if prefix_found is None:
            results.append({
                "keyword": keyword,
                "status": "not_found",
                "prefix": None
            })
        else:
            results.append({
                "keyword": keyword,
                "status": "found",
                "prefix": prefix_found
            })

    return jsonify({"results": results})

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "route not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)