from .lexer import Lexer, TokenTypes, Token
from .ast import ProgramNode, ObjectNode, MemberNode

class Parser:
    def __init__(self, input: str) -> None:
        self.lexer = Lexer(input)
        self.currentToken = None # Current token to parse
        self.peekToken = None # Next token that will be parsed. Knowing this will be useful for selecting valid rules.


    def nextToken(self):
        self.currentToken = self.peekToken
        self.peekToken = self.lexer.nextToken()

    def parseValue(self) -> Token:
        if self.currentToken.type != TokenTypes.STRING:
            raise SyntaxError(f'Invalid token for value: {self.currentToken.literal}')
        
        return self.currentToken

    def parseProgram(self) -> ProgramNode:

        # Call next token twice to allow currentToken and peekToken to be properly initialised
        self.nextToken()
        self.nextToken()
        program_node = ProgramNode()
        if self.currentToken.type == TokenTypes.LEFT_BRACE: 
            parent_object: ObjectNode = self.parseObject()
            program_node.parent_object = parent_object
        else:
            raise SyntaxError(f'Invalid token {self.currentToken.literal}')

        return program_node
    
    def parseMember(self) -> MemberNode:
        member_node = MemberNode()
        if self.peekToken.type != TokenTypes.COLON:
            raise SyntaxError('Colon required in defining a member')
        member_node.key = self.currentToken
        # Skip the colon and go to the next token
        self.nextToken()
        self.nextToken()

        member_node.value = self.parseValue()

        return member_node

    def parseObject(self):
        object_node = ObjectNode()
        self.nextToken()

        while self.currentToken.type != TokenTypes.RIGTH_BRACE:
            if self.currentToken.type == TokenTypes.STRING:
                member = self.parseMember()
                object_node.members.append(member)
                self.nextToken()

                if self.currentToken.type == TokenTypes.COMMA: # If the current token is a comma
                    if self.peekToken.type == TokenTypes.STRING: # If the next token is a string, then there are more members to follow
                        self.nextToken() # Skip the comma
                    # Otherwise do nothing
                else: # If the current token is not a comma, then that better be the end 
                    if self.currentToken.type != TokenTypes.RIGTH_BRACE:
                        raise SyntaxError(f'Comma expected before next member')

            else:
                raise SyntaxError(f'Invalid token {self.currentToken.literal}')
            
        return object_node