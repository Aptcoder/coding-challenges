# File should contain everything related to generating the abstract syntax tree other than the parser itself
# To complete this coding challenge, generating a Abstract syntax tree isn't necessary but for personal learning purposes I will atttempt this
from abc import ABC, abstractmethod
from typing import List
from .token import Token

class Node(ABC):
    @abstractmethod
    def token_literal(self):
        pass


class ProgramNode(Node):
    def __init__(self):
        self.parent_object = None

    def token_literal(self):
        return  
    

class ObjectNode(Node):
    def __init__(self):
        self.members: List[MemberNode] = []

    def token_literal(self):
        return  
    
class ValueNode(Node):
    def __init__(self) -> None:
        self.value: Token | ArrayNode | ObjectNode = None

    def token_literal(self):
        return  
    
class ArrayNode(Node):
    def __init__(self) -> None:
        self.elements: List[Token] = []

    def token_literal(self):
        return  

class MemberNode(Node):
    def __init__(self) -> None:
        self.key: Token | None = None
        self.value: ValueNode = None
    
    def token_literal(self):
        return 
    