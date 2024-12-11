import ast
import os

from configparser import ConfigParser

class Config:

    __FILTER_SECTION_NAME = "FILTER"
    __FILTER_SPARQL_KEY_NAME = "sparql"

    __PROMPT_SECTION_NAME = "PROMPT"
    __PROMPT_INSTRUCTIONS_KEY_NAME = "instructions"
    __PROMPT_FEWSHOTS_KEY_NAME = "fewshots"
    __PROMPT_INPUT_PREDS_KEY_NAME = "input_predicates"

    __parser = None

    def __init__(self):
        self.__parser = ConfigParser(delimiters=('='))
        self.__parser.optionxform = str # we want case-sensitive keys
        self.__parser.read(os.path.join(os.path.dirname(__file__),'res/config.ini'))

    def getFilterQuery(self):
        return self.__parser.get(self.__FILTER_SECTION_NAME, self.__FILTER_SPARQL_KEY_NAME)

    def getPromptInstructions(self):
        return self.__parser.get(self.__PROMPT_SECTION_NAME, self.__PROMPT_INSTRUCTIONS_KEY_NAME)

    def getPromptFewShotExamples(self):
        e = self.__parser.get(self.__PROMPT_SECTION_NAME, self.__PROMPT_FEWSHOTS_KEY_NAME)
        return ast.literal_eval(e)

    def getPromptInputPredicates(self):
        e = self.__parser.get(self.__PROMPT_SECTION_NAME, self.__PROMPT_INPUT_PREDS_KEY_NAME)
        return ast.literal_eval(e)
