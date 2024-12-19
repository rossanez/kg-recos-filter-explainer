import ast
import os

from configparser import ConfigParser

class Config:

    __RERANKER_SECTION_NAME = "FILTER"
    __RERANKER_SPARQL_KEY_NAME = "sparql"

    __FILTER_SECTION_NAME = "FILTER"
    __FILTER_SPARQL_KEY_NAME = "sparql"
    __FILTER_USER_SPARQL_KEY_NAME = "user_sparql"

    __USER_SECTION_NAME = "USER"
    __USER_PREDS_KEY_NAME = "predicates"

    __PROMPT_SECTION_NAME = "PROMPT"
    __PROMPT_INSTRUCTIONS_KEY_NAME = "instructions"
    __PROMPT_FEWSHOTS_KEY_NAME = "fewshots"
    __PROMPT_INPUT_PREDS_KEY_NAME = "input_predicates"

    __parser = None

    def __init__(self):
        self.__parser = ConfigParser(delimiters=('='))
        self.__parser.optionxform = str # we want case-sensitive keys
        self.__parser.read(os.path.join(os.path.dirname(__file__),'res/config.ini'))

    def getRerankerQuery(self):
        return self.__parser.get(self.__RERANKER_SECTION_NAME, self.__RERANKER_SPARQL_KEY_NAME)

    def getFilterQuery(self):
        return self.__parser.get(self.__FILTER_SECTION_NAME, self.__FILTER_SPARQL_KEY_NAME)

    def getFilterUserQuery(self):
        return self.__parser.get(self.__FILTER_SECTION_NAME, self.__FILTER_USER_SPARQL_KEY_NAME)

    def getUserPredicates(self):
        e = self.__parser.get(self.__USER_SECTION_NAME, self.__USER_PREDS_KEY_NAME)
        return ast.literal_eval(e)

    def getPromptInstructions(self):
        return self.__parser.get(self.__PROMPT_SECTION_NAME, self.__PROMPT_INSTRUCTIONS_KEY_NAME)

    def getPromptFewShotExamples(self):
        e = self.__parser.get(self.__PROMPT_SECTION_NAME, self.__PROMPT_FEWSHOTS_KEY_NAME)
        return ast.literal_eval(e)

    def getPromptInputPredicates(self):
        e = self.__parser.get(self.__PROMPT_SECTION_NAME, self.__PROMPT_INPUT_PREDS_KEY_NAME)
        return ast.literal_eval(e)
