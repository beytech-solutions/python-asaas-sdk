from enum import Enum
from typing import Optional, List, TypedDict, Iterable, Union
from requests import Response
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse

from asaas.exceptions import SDKMisconfiguration
from asaas.http import RequestHandler
from asaas.sdk.middlewares import BaseMiddleware
from asaas.http.middlewares import BaseHttpMiddleware


class AsaasResponseErrorItem(TypedDict):
    code: str
    description: str


class AsaasResponseStatus(Enum):
    OK = "OK"
    BAD_REQUEST = "BAD_REQUEST"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    NOT_FOUND = "NOT_FOUND"
    TOO_MANY_REQUESTS = "TOO_MANY_REQUESTS"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"


class RateLimitDict(TypedDict):
    limit: int
    remaining: int
    reset: int


class AsaasResponse:
    def __init__(self, res: Response):
        self.http_response = res
        
        try:
            self.data = res.json()
        except Exception as e:
            self.data = str(e)


    @property
    def ok(self) -> bool:
        return self.http_response.status_code == 200 and isinstance(self.data, dict)
    
    
    @property
    def errors(self) -> List[AsaasResponseErrorItem]:
        err_list = self.data.get("errors", [])
        return err_list if isinstance(err_list, list) else []


    @property
    def rate_limit(self) -> Union[RateLimitDict, None]:
        try:
            limit = int(http_response.headers.get("RateLimit-Limit"))
            remaining = int(http_response.headers.get("RateLimit-Remaining"))
            reset = int(http_response.headers.get("RateLimit-Reset"))
            
            return RateLimitDict(limit=limit, remaining=remaining, reset=reset)
        except (TypeError, ValueError):
            return None
    
    
    @property
    def has_more(self) -> bool:
        return self.data.get("hasMore", False)
    
    
    @property
    def next(self, limit: Optional[int] = 10):
        # refazer chamada e retornar outro AsaasResponse
        return self
    
    
    @property
    def status(self) -> AsaasResponseStatus:
        if self.http_response.status_code == 200:
            return AsaasResponseStatus.OK
        elif self.http_response.status_code == 400:
            return AsaasResponseStatus.BAD_REQUEST
        elif self.http_response.status_code == 401:
            return AsaasResponseStatus.UNAUTHORIZED
        elif self.http_response.status_code == 403:
            return AsaasResponseStatus.FORBIDDEN
        elif self.http_response.status_code == 404:
            return AsaasResponseStatus.NOT_FOUND
        elif self.http_response.status_code == 500:
            return AsaasResponseStatus.INTERNAL_SERVER_ERROR
        else:
            return AsaasResponseStatus.OK
        
        
class Asaas:
    TOO_MANY_REQUESTS_MAX_DELAY = 30
    
    def __init__(
        self,
        user_agent: str,
        access_token: str,
        environment: Optional[Union["production", "sandbox"]] = "production",
        version: Optional[str] = "v3",
        http_middlewares: Optional[Iterable[BaseHttpMiddleware]] = [],
        middlewares: Optional[Iterable[BaseMiddleware]] = [],
        retry_when_many_requests: Optional[bool] = True,
        max_delay_when_many_requests: Optional[int] = TOO_MANY_REQUESTS_MAX_DELAY,
    ):
        """ User Agent """
        if not user_agent:
            raise SDKMisconfiguration("'user_agent' is required")
        
        self.user_agent = user_agent
        
        """ Access Token """
        if not access_token:
            raise SDKMisconfiguration("'access_token' is required")
        
        self.access_token = access_token
        
        """ Version """
        if version not in ['v3']:
            raise SDKMisconfiguration(f"Invalid version: {version}")
        
        self.version = version
        
        """ Environment """
        if environment not in ['production', 'sandbox']:
            raise SDKMisconfiguration(f"Invalid environment: {version}. Use 'production' or 'sandbox'")
        
        self.version = version
        
        """ Http Middlewares Instances """
        if isinstance(http_middlewares, Iterable):
            for m in http_middlewares:
                if not isinstance(m, BaseHttpMiddleware):
                    raise SDKMisconfiguration(f"{m.__repr__} is not a instance of BaseHttpMiddleware")
            
            self.http_middlewares = http_middlewares
        
        """ Middlewares Instances """
        if isinstance(middlewares, Iterable):
            for m in middlewares:
                if not isinstance(m, BaseMiddleware):
                    raise SDKMisconfiguration(f"{m.__repr__} is not a instance of BaseMiddleware")
            
            self.middlewares = middlewares
        
    