from openai import OpenAI

# Point to your running ArkOS agent
client = OpenAI(base_url="http://localhost:1111/v1", api_key="not-needed")

def test_agent(prompt: str):
    response = client.chat.completions.create(
        model="ark-agent",
        messages=[{"role": "user", "content": prompt}]
    )
    
    message = response.choices[0].message.content
    print("=== Agent Response ===")
    print(message)
    print("======================")
    return message

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ["exit", "quit"]:
            break
        test_agent(user_input)

