
class MercadoLivreToken:

    access_token = None
    refresh_token = None

    def __init__(self, access_token, refresh_token):
        self.access_token = access_token
        self.refresh_token = refresh_token

