
import sys
from typing import List
from .token import Token, TokenTypes



class Lexer:
    def __init__(self, input):
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
        elif character and character.isspace():
            # If character is space, skip it
            self.skipSpaces()
            return self.nextToken()
        elif character == None:
            token = Token("", TokenTypes.EOF)
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
