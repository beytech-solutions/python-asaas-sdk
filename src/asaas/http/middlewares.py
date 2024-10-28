from typing import Union
from requests import Request, Response

from abc import ABC, abstractmethod

class BaseHttpMiddleware(ABC):
    
    @abstractmethod
    def before(self, req: Request) -> Request:
        return req

    @abstractmethod
    def after(self, res: Response) -> Response:
        return res
