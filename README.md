
# 🖼️ AI Diagram Generator

Generate cloud architecture diagrams from natural-language prompts using a FastAPI backend powered by **Gemini (via LangChain + LangGraph)** and rendered with [`diagrams`](https://diagrams.mingrammer.com/).

---

## 📁 Project Structure

```text
ai-diagram-generator/
├── src/
│   ├── main.py            # FastAPI app + endpoints
│   ├── agent.py           # LangGraph agent logic
│   ├── diagram_tool.py    # Diagram generation logic
│   ├── llm_client.py      # Gemini/HuggingFace fallback setup
│   ├── config.py          # Pydantic-based env loader
│   └── prompts.py         # Optional prompt templates
├── tests/
├── outputs/               # PNG files created by the app
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md           
```

---

## ⚙️ Local Setup

```bash
# 1. Clone and enter the project
git clone https://github.com/Orbenson/Engini-Home-Assignment.git
cd Engini-Home-Assignment

# 2. Set up virtual environment
python3.10 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Configure env variables
cp .env.example .env    # Add your GOOGLE_API_KEY
export $(cat .env | xargs)  # Optional (dotenv is auto-loaded)

# 5. Launch the server
uvicorn src.main:app --reload
# → Now running at http://127.0.0.1:8000
```

---

## 🐳 Docker Setup

```bash
# Build and run with Docker Compose
docker compose up --build
# Server: http://localhost:8000
```

Make sure your `GOOGLE_API_KEY` is set in your shell or `.env` file.

---

## 🔐 Environment Variables

| Variable         | Description                                        |
|------------------|----------------------------------------------------|
| `GOOGLE_API_KEY` | **Required**. Gemini API key.                      |
| `MODEL_NAME`     | Optional. Default: `gemini-2.0-flash-001`          |
| `TEMPERATURE`    | Optional. Controls LLM creativity. Default: `0.3`  |
| `FALLBACK_MODEL` | Optional. HuggingFace fallback, default: `distilgpt2` |

---

## 📡 API Endpoints

### `GET /diagram`

Generates a static diagram (non-LLM) from a description.

```http
GET http://127.0.0.1:8000/diagram?description=...
```

Example:

```http
GET http://127.0.0.1:8000/diagram?description=Design a microservices architecture with three services: an authentication service, a payment service, and an order service. Include an API Gateway for routing, an SQS queue for message passing between services, and a shared RDS database. Group the services in a cluster called 'Microservices'. Add CloudWatch for monitoring.
```

---

### `POST /assistant_chat`

LLM-powered conversational interface.

**Request:**

```json
POST http://127.0.0.1:8000/assistant_chat
Content-Type: application/json

{
  "conversation_id": "demo-chat-1",
  "message": "Design a microservices architecture with three services: an authentication service, a payment service, and an order service. Include an API Gateway for routing, an SQS queue for message passing between services, and a shared RDS database. Group the services in a cluster called 'Microservices'. Add CloudWatch for monitoring."
}
```

**Response:**

```json
{
  "conversation_id": "demo-chat-1",
  "response": "The diagram has been generated and saved to outputs/micro_a1b2c3.png",
  "image_path": "outputs/micro_a1b2c3.png"
}
```

---

## 🧪 Running Tests

```bash
pytest
```

Includes `pytest.ini` to auto-include `src/` in the Python path.

---

## 📬 Postman Collection

Import these two requests via **Postman → Import → Raw Text**:

<details>
<summary>📥 GET /diagram</summary>

```json
{
  "info": { "name": "GET /diagram", "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json" },
  "item": [
    {
      "name": "GET /diagram",
      "request": {
        "method": "GET",
        "url": {
          "raw": "http://127.0.0.1:8000/diagram?description=Design%20a%20microservices%20architecture%20with%20three%20services%3A%20authentication%2C%20payment%2C%20order.%20Include%20an%20API%20Gateway%2C%20an%20SQS%20queue%2C%20a%20shared%20RDS%20database%2C%20and%20CloudWatch.",
          "host": ["127", "0", "0", "1"],
          "port": "8000",
          "path": ["diagram"],
          "query": [
            {
              "key": "description",
              "value": "Design a microservices architecture with three services: authentication, payment, order. Include an API Gateway, an SQS queue, a shared RDS database, and CloudWatch."
            }
          ]
        }
      }
    }
  ]
}
```
</details>

<details>
<summary>📥 POST /assistant_chat</summary>

```json
{
  "info": { "name": "POST /assistant_chat", "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json" },
  "item": [
    {
      "name": "POST /assistant_chat",
      "request": {
        "method": "POST",
        "header": [{ "key": "Content-Type", "value": "application/json" }],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"conversation_id\": \"demo-chat-1\",\n  \"message\": \"Design a microservices architecture with three services: authentication, payment, order. Include an API Gateway, an SQS queue, a shared RDS database, and CloudWatch.\"\n}"
        },
        "url": {
          "raw": "http://127.0.0.1:8000/assistant_chat",
          "host": ["127", "0", "0", "1"],
          "port": "8000",
          "path": ["assistant_chat"]
        }
      }
    }
  ]
}
```
</details>

---

## 🛠️ Common Issues

| Problem | Solution |
|--------|----------|
| `langchain_google_genai` not found | `pip install langchain-google-genai` |
| Gemini schema `items[]` error | Already fixed in `diagram_tool.py` |
| Torch `_ARRAY_API` crash | NumPy pinned to `<2` in `requirements.txt` |

---

## 🚀 Production Deployment

```bash
docker build -t ai-diagram-generator .
docker run -p 8000:8000 --env GOOGLE_API_KEY=YOUR_KEY ai-diagram-generator
```

---

## 📜 License

MIT – free to use, modify, and launch your own LLM-powered diagram service.




