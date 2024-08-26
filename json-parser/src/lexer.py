
import sys
from typing import List
from .token import Token, TokenTypes

keywords = {"true": TokenTypes.BOOLEAN_TRUE, "false": TokenTypes.BOOLEAN_FALSE, "null": TokenTypes.NULL}

class Lexer:
    def __init__(self, input: str):
        self.tokens: List[Token] = []
        self.position = 0
        self.input = input
        self.line_number = 1

    def readCharacter(self) -> None | str:
        if self.position >= len(self.input):
            return None
        
        character = self.input[self.position]
        self.position += 1
        return character
    
    def readString(self):
        string = ""
        while char := self.readCharacter():
            if char == '"':
                break
            else:
                string = string + char
        return string
    
    def readNumeric(self):
        numeric = self.input[self.position - 1]
        while char := self.readCharacter():
            if not char.isnumeric():
                break
            else:
                numeric = numeric + char
        self.position -= 1
        return numeric
    
    '''
    This checks if a set of characters is either a boolean value or null
    '''
    def readKeyword(self):
        start_position = self.position - 1
        keyword = self.input[start_position]
        while char := self.readCharacter():
            if not char.isalpha():
                break
            else:
                keyword = keyword + char
        if keyword in keywords.keys():
            token_type = keywords[keyword]
            self.position -= 1
            return keyword, token_type
        else:
            raise Exception(f'character at position {start_position} not recognised')
    
    def skipSpaces(self):
        while char := self.readCharacter():
            if char.isspace():
                if char == '\n' or char == '\r':
                    self.line_number += 1
                continue
            else:
                self.position -= 1
                break


    def nextToken(self):
        character = self.readCharacter()
        token = None

        if character == "{":
            token = Token(character, TokenTypes.LEFT_BRACE)
            self.tokens.append(token)
        elif character == "}":
            token = Token(character, TokenTypes.RIGTH_BRACE)
            self.tokens.append(token)
        elif character == "]":
            token = Token(character, TokenTypes.RIGHT_BRACKET)
            self.tokens.append(token)
        elif character == "[":
            token = Token(character, TokenTypes.LEFT_BRACKET)
            self.tokens.append(token)
        elif character == '"':
            name = self.readString()
            token = Token(name, TokenTypes.STRING)
            self.tokens.append(token)
        elif character == ':':
            token = Token(character, TokenTypes.COLON)
            self.tokens.append(token)
        elif character == ",":
            token = Token(character, TokenTypes.COMMA)
            self.tokens.append(token)
        elif character == None:
            token = Token("", TokenTypes.EOF)
        elif character.isspace():
            # If character is space, skip it
            self.skipSpaces()
            return self.nextToken()
        elif character.isnumeric():
            numeric = self.readNumeric()
            token = Token(numeric, TokenTypes.NUMERIC)
            self.tokens.append(token)
        elif character.isalpha():
            keyword, token_type = self.readKeyword()
            token = Token(keyword, token_type)
            self.tokens.append(token)
        else:
            raise Exception(f'character at position {self.position - 1} not recognised')
        return token
    
    def scan(self):
        while token := self.nextToken():
            self.tokens.append(token)
            if token.type == TokenTypes.EOF:
                break

            
    def get_tokens(self):
        return self.tokens
