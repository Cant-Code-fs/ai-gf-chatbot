from flask import Flask, request, jsonify, render_template
import json
from llama_cpp import Llama

# Load AI Model (Adjust path to your GGUF model)
MODEL_PATH = "C:/AI_Models/pygmalion-2-7b.Q5_K_M.gguf"
llm = Llama(model_path=MODEL_PATH)

# Flask app setup
app = Flask(__name__)

# Memory file to remember chats
MEMORY_FILE = "chat_memory.json"

# Load memory
try:
    with open(MEMORY_FILE, "r") as f:
        memory = json.load(f)
except FileNotFoundError:
    memory = {"name": "Bro", "chats": []}

your_name = memory.get("name", "Bro")

@app.route("/")
def home():
    return render_template("chat.html")  # Loads the chat UI

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    if not user_input:
        return jsonify({"error": "No message received"})

    # Add chat history to prompt
    prompt = f"You are my fun, flirty, and caring Indian girlfriend named Aisha. You talk casually with me ({your_name}).\n\n"
    for chat in memory["chats"][-5:]:
        for k, v in chat.items():
            prompt += f"{k}: {v}\n"

    prompt += f"{your_name}: {user_input}\nAI GF: "

    # Get AI response
    output = llm(prompt, max_tokens=150, temperature=0.8)
    response = output["choices"][0]["text"].strip()

    # Store in memory
    memory["chats"].append({"You": user_input})
    memory["chats"].append({"AI GF": response})

    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f)

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

