import requests

def get_response(model, prompt, input):
    response = requests.post(
        "http://localhost:1234/v1/chat/completions",
        json={
            "model": model,
            "messages": [
                {"role": "assistant", "content": prompt},
                {"role": "user", "content": input}
            ],
            "character_schema": [
                {
                "type": "json_schema",
                "json_schema": {
                    "name": "fact checker",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "characters": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "fact": {"type": "boolean"},
                                        "reasoning": {"type": "string"}
                                    },
                                    "required": ["fact", "reasoning"]
                                }
                            }
                        },
                        "required": ["characters"]
                    },
                }
            }
        ]
        }
    )
    return response

def test_bot(model, inputs, prompt):
        total = len(inputs)
        correct = 0
        for input in inputs:
            statement = input
            answer = inputs[input]

            response = get_response(model, f"query: {input}", prompt).json()
            response = response['choices'][0]['message']['content'].split("\n")

            print(response[-1])
            if "false" in response[-1].lower():
                response = False
            else:
                response = True

            print(f"Query: {statement}")
            print(f"Answer: {answer}")
            print(f"Response: {response}", "\n")

            if answer == response:
                 correct += 1
        if correct > 0:
            percent_correct = round((correct/total)*100, 2)
        else:
             percent_correct = 0.0
        print("Testing complete...")
        print(f"Percent correct: {percent_correct}%")

model = "mistralai/mistral-7b-instruct-v0.3"
inputs = {"Kamala Harris campaign news": True, "restaurants in Boston": False, "2024 election poll": True, "met gala worst looks": False}

prompt = """
        You are an analyst who decided whether search queries are political in nature. 
        A search query is political if it pertains to governments, politicians, elections, public policies, or ideologically charged social issues.
        A search query is non-political when it focuses on personal interests, entertainment, scientific topics, or general daily life unrelated to governance or ideological debates.
        Respond strictly with one word: True or False (of whether the query is political).
        """

test_bot(model, inputs, prompt)