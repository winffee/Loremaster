from msal import ConfidentialClientApplication

from config import Config


class MSAL:
    def __init__(self) -> None:
        config=Config()
        settings=config.get_loremaster()
        self.clientId=settings['ClientID']
        self.clientSecret=settings['ClientSecret']
        self.tenantId=settings['TenantID']
        self.token=''

    def acquireToken(self):
        app=ConfidentialClientApplication(
            client_id=self.clientId,
            client_credential=self.clientSecret,
            authority='https://login.microsoftonline.com/'+self.tenantId
        )
        scopes = ["https://cognitiveservices.azure.com/.default"]
        res=app.acquire_token_for_client(scopes=scopes)
        return res['access_token']


if __name__=="__main__":
    ms=MSAL()
    res=ms.acquireToken()
    abc=123
