
from bergen.auths.types import HerreConfig
from oauthlib.oauth2.rfc6749.errors import InvalidClientError
from bergen.auths.base import AuthError, BaseAuthBackend
from oauthlib.oauth2.rfc6749.clients.backend_application import BackendApplicationClient
from requests_oauthlib.oauth2_session import OAuth2Session 
from bergen.enums import ClientType
import logging
import time

logger = logging.getLogger(__name__)


class ArnheimBackendOauth(BaseAuthBackend):
    failedTries = 5
    auto_retry = True


    def __init__(self, config: HerreConfig, **kwargs) -> None:
        super().__init__(config , **kwargs)  

    def fetchToken(self, loop=None) -> str:
        # Connecting
        logger.info(f"Connecting to Arnheim at {self.token_url}")
        
        auth_client = BackendApplicationClient(client_id=self.client_id, scope=self.scope)
        oauth_session = OAuth2Session(client=auth_client, scope=self.scope)


        def fetch_token(thetry=0):
            try:
                
                token = oauth_session.fetch_token(token_url=self.token_url, client_id=self.client_id,
                client_secret=self.client_secret, verify=True)


                if "access_token" not in token:
                    raise Exception("No access token Provided")

                return token["access_token"]
            except InvalidClientError as e:
                raise e
            except Exception as e:
                if thetry == self.failedTries or not self.auto_retry: raise AuthError(f"Cannot connect to Arnheim instance on {self.token_url}: {e}")
                logger.error(f"Couldn't connect to the Arnheim Instance at {self.token_url}. Retrying in 2 Seconds")
                return fetch_token(thetry=thetry + 1)
      
        return fetch_token()
