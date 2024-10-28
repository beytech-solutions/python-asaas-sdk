from typing import Union
from requests import Request, Response

from abc import ABC, abstractmethod

class BaseMiddleware(ABC):
    
    @abstractmethod
    def before(self, req: Request) -> Request:
        return req
