from .lexer import Lexer, TokenTypes, Token
from .ast import ProgramNode, ObjectNode, MemberNode, ValueNode, ArrayNode

class Parser:
    def __init__(self, input: str) -> None:
        self.lexer = Lexer(input)
        self.currentToken = None # Current token to parse
        self.peekToken = None # Next token that will be parsed. Knowing this will be useful for selecting valid rules.


    def nextToken(self):
        self.currentToken = self.peekToken
        self.peekToken = self.lexer.nextToken()

    def parseArray(self):
        arrayNode = ArrayNode()
        self.nextToken()
        accepted_value_token_types = [TokenTypes.STRING, TokenTypes.NUMERIC, TokenTypes.BOOLEAN_FALSE, TokenTypes.BOOLEAN_TRUE, TokenTypes.NULL]
        while self.currentToken.type != TokenTypes.RIGHT_BRACKET:
            if self.currentToken.type in accepted_value_token_types:
                arrayNode.elements.append(self.currentToken)
                self.nextToken()
                if self.currentToken.type == TokenTypes.COMMA:
                    if self.peekToken.type in accepted_value_token_types:
                        self.nextToken()
                    else:
                        raise Exception(f'Unrecognised array element {self.peekToken.literal}')
                else:
                    if self.currentToken.type == TokenTypes.RIGHT_BRACKET:
                        continue
                    else:
                        raise Exception(f'Unrecognised array element {self.currentToken.literal}')

            else:
                raise Exception(f'Unrecognised array element {self.currentToken.literal}')
        return arrayNode

    def parseValue(self) -> Token:
        valueNode = ValueNode()
        accepted_value_token_types = [TokenTypes.STRING, TokenTypes.NUMERIC, TokenTypes.BOOLEAN_FALSE, TokenTypes.BOOLEAN_TRUE, TokenTypes.NULL]
        if self.currentToken.type in accepted_value_token_types:
            valueNode.value = self.currentToken
        elif self.currentToken.type == TokenTypes.LEFT_BRACKET:
            arrayNode = self.parseArray()
            valueNode.value = arrayNode
        elif self.currentToken.type == TokenTypes.LEFT_BRACE:
            objectNode = self.parseObject()
            valueNode.value = objectNode
        else:
            raise SyntaxError(f'Invalid token for value: {self.currentToken.literal}')
        
        return valueNode

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

        while self.currentToken.type != TokenTypes.RIGHT_BRACE:
            if self.currentToken.type == TokenTypes.STRING:
                member = self.parseMember()
                object_node.members.append(member)
                self.nextToken()

                if self.currentToken.type == TokenTypes.COMMA: # If the current token is a comma
                    if self.peekToken.type == TokenTypes.STRING: # If the next token is a string, then there are more members to follow
                        self.nextToken() # Skip the comma
                    # Otherwise do nothing
                else: # If the current token is not a comma, then that better be the end 
                    if self.currentToken.type != TokenTypes.RIGHT_BRACE:
                        raise SyntaxError(f'Comma expected before next member')

            else:
                raise SyntaxError(f'Invalid token {self.currentToken.literal}')
            
        return object_node