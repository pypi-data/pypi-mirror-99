class EndPoints:

    def __init__(self, sandbox=False):
        self.base_endpoint = 'https://sandbox.dojah.io'
        self.sandbox = sandbox
        if not self.sandbox:
            self.base_endpoint = 'https://api.dojah.io'

        self.wallet_balance = '/api/v1/balance' # ----GET

        self.messaging = '/api/v1/messaging/sms' #needs sender id(default is dojah), priority, channel(whether whatsapp or sms), message, destination(number you are sending to)----- POST

        self.request_sender_id = '/api/v1/messaging/sender_id' # needs sender_id -----POST
        self.fetch_sender_ids = '/api/v1/messaging/sender_ids'

        self.message_status = '/api/v1/messaging/sms/get_status' #Query Parameters -- message_id(can be gotten from the response of messaging)---GET

        self.otp = '/api/v1/messaging/otp' # POST ------  needs priority(Boolean; default is False), expiry(optional; integer; number of minutes before OTP expires), length(optional; integer; length of otp), sender_id, destination, channel(list)

        self.validate_otp = '/api/v1/messaging/otp/validate' #GET ----Query Parameters- otp received by user; reference_id to identify otp

        self.airtime = '/api/v1/purchase/airtime' #POST ---- takes in amount and destination

        self.data_plans = '/api/v1/purchase/data/plans' #GET lists out all the available data plans

        self.buy_data = '/api/v1/purchase/data' # POST ------takes in data plan(can be gotten from data plans endpoint), destination

        self.crypto_wallet = '/api/v1/wallet/create' # POST ------takes in wallet_type
        self.get_crypto_wallet = '/api/v1/wallet' # ----- Query Parameter of wallet_id

        self.send_crypto = '/api/v1/wallet/send' # POST----- Takes in sender wallet id, amount, recipient crypto wallet address

        self.internal_crypto = '/api/v1/wallet/send/internal'

        self.transaction_details = '/api/v1/wallet/transaction' # GET --- takes in transaction id

    
 

    def wallet_balance_endpoint(self):
        return f"{self.base_endpoint}{self.wallet_balance}"

    def messaging_endpoint(self):
        return f"{self.base_endpoint}{self.messaging}"

    def request_sender_id_endpoint(self):
        return f"{self.base_endpoint}{self.request_sender_id}"

    def send_crypto_endpoint(self):
        return f"{self.base_endpoint}{self.send_crypto}"

    def send_crypto_internal_endpoint(self):
        return f"{self.base_endpoint}{self.internal_crypto}"

    def get_crypto_wallet_endpoint(self):
        return f"{self.base_endpoint}{self.get_crypto_wallet}"

    def crypto_wallet_endpoint(self):
        return f"{self.base_endpoint}{self.crypto_wallet}"

    def transaction_details_endpoint(self):
        return f"{self.base_endpoint}{self.transaction_details}"

    def buy_data_endpoint(self):
        return f"{self.base_endpoint}{self.buy_data}"
    
    def data_plans_endpoint(self): 
        return f"{self.base_endpoint}{self.data_plans}"

    def airtime_endpoint(self):
        return f"{self.base_endpoint}{self.airtime}" 

    def fetch_sender_ids_endpoint(self):
        return f"{self.base_endpoint}{self.fetch_sender_ids}"

    def message_status_endpoint(self):
        return f"{self.base_endpoint}{self.message_status}"

    def otp_endpoint(self):
        return f"{self.base_endpoint}{self.otp}"

    def validate_otp_endpoint(self):
        return f"{self.base_endpoint}{self.validate_otp}"




       

