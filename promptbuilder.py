class PromptBuilder:

    __config = None

    def __init__(self, config):
        self.__config = config

    def __getBasePrompt(self):
        prompt = self.__config.getPromptInstructions()
        fewshots = self.__config.getPromptFewShotExamples()
        for ex in fewshots:
            prompt += f'\n{ex}\n\n\n'

        return prompt

    def __genRequestWithNewTriples(self, triples):
        content = " ".join(triples)

        return f'Triples: {content}\nDescription: '

    def build(self, triples):
        base = self.__getBasePrompt()
        request = self.__genRequestWithNewTriples(triples)

        return f'{base}\n{request}'

