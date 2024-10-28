import requests
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse

class Paginator:
    def __init__(self, response: requests.Response, limit: int = 10, offset: int = 0):
        self.response = response
        self.limit = limit
        self.offset = offset
        self.base_url = response.url

    def _update_query_params(self, url: str, **params) -> str:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)

        # Atualiza ou adiciona novos parâmetros de consulta
        for key, value in params.items():
            query_params[key] = [str(value)]

        # Reconstrói a URL com os parâmetros modificados
        new_query = urlencode(query_params, doseq=True)
        return urlunparse(parsed_url._replace(query=new_query))

    def next(self) -> requests.Response:
        # Incrementa o offset para a próxima página
        self.offset += self.limit
        
        # Cria a URL com o novo offset para a próxima página
        next_url = self._update_query_params(self.base_url, limit=self.limit, offset=self.offset)

        # Realiza a requisição e atualiza o objeto response
        self.response = requests.get(next_url)
        return self.response
