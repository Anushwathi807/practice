# Backend Microservices

Two Flask microservices built as part of a backend development assessment.

## Project Structure
backend-microservices/

├── q1/

│   └── app.py   # Numbers microservice

└── q2/

└── app.py   # Prefix microservice

## Q1 — Numbers Microservice

Fetches numbers from multiple URLs concurrently, merges them, removes duplicates, and returns a sorted list within 500ms.

### How to run
cd q1

python3 app.py

### API
GET /numbers?url=<url1>&url=<url2>

### Example
GET /numbers?url=http://example.com/primes&url=http://example.com/fibo

Response:
```json
{"numbers": [1, 2, 3, 5, 8, 13]}
```

## Q2 — Prefix Microservice

Finds the shortest unique prefix for each keyword in a predefined word list using a Trie data structure.

### How to run
cd q2

python3 app.py

### API
GET /prefix?keywords=<word1>,<word2>

### Example
GET /prefix?keywords=bonfire,bonsai

Response:
```json
{
  "results": [
    {"keyword": "bonfire", "status": "found", "prefix": "bonf"},
    {"keyword": "bonsai", "status": "found", "prefix": "bons"}
  ]
}
```

## Requirements
flask

requests

Install with:
pip install flask requests
