from typing import TypedDict, Optional
from requests import Response
from abc import ABC, abstractmethod


class BaseAPIRequest(ABC):
    
    @abstractmethod
    def call(
        self,
        base_url: str,
        headers: dict,
        *args,
        **kwargs
    ) -> Response:
        raise NotImplementedError("Subclasses should implement this method")    


class RequestHandler:
    def __init__(
        self,
        base_url: str,
        user_agent: str,
        access_token: str
    ):
        self.base_url = base_url
        self.user_agent = user_agent
        self.access_token = access_token
        
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": user_agent,
            "access_token": access_token
        }


    def call(self, api_request: BaseAPIRequest, *args, **kwargs) -> Response:
        return api_request.call(self.headers, *args, **kwargs)