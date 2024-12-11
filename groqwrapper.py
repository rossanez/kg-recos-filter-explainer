from groq import Groq

KEY_FILE = 'res/groq.key'

class GroqWrapper:

    __key = None

    def __init__(self):
        self.__key = self.__getKey()

    def __getKey(self):
        try:
            with open(KEY_FILE, 'r') as key:
                value = key.read()
        except FileNotFoundError:
            print(f'ERROR: No token for groq found! Insert yours at {KEY_FILE}')
            value = "<insert your token here>"
            key = open(KEY_FILE, 'w')
            key.write(value)
            key.close()

            exit(1)

        return value.strip()

    def query(self, content, model="llama3-70b-8192", temp=1):
        client = Groq(
            api_key=self.__key,
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": content,
                }
            ],
            model=model,
            temperature=temp,
        )

        return chat_completion.choices[0].message.content

