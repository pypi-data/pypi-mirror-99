from redpay.charge_card import ChargeCard
from redpay.charge_ach import ChargeACH
from redpay.tokenize_card import TokenizeCard
from redpay.tokenize_ach import TokenizeACH
from redpay.charge_token import ChargeToken
from redpay.void import Void
from redpay.refund import Refund
from redpay.get_transaction import GetTransaction


class RedPay:
    def __init__(self, app, key, endpoint) -> None:
        self.app = app
        self.key = key
        self.endpoint = endpoint

    def ChargeCard(self, request):
        charge_card = ChargeCard(self.app, self.key, self.endpoint)
        return charge_card.Process(request)

    def ChargeACH(self, request):
        charge_ach = ChargeACH(self.app, self.key, self.endpoint)
        return charge_ach.Process(request)

    def TokenizeCard(self, request):
        tokenize_card = TokenizeCard(self.app, self.key, self.endpoint)
        return tokenize_card.Process(request)

    def TokenizeACH(self, request):
        tokenize_ach = TokenizeACH(self.app, self.key, self.endpoint)
        return tokenize_ach.Process(request)

    def ChargeToken(self, request):
        charge_token = ChargeToken(self.app, self.key, self.endpoint)
        return charge_token.Process(request)

    def Refund(self, request):
        refund = Refund(self.app, self.key, self.endpoint)
        return refund.Process(request)

    def Void(self, request):
        void = Void(self.app, self.key, self.endpoint)
        return void.Process(request)

    def GetTransaction(self, request):
        get_transaction = GetTransaction(self.app, self.key, self.endpoint)
        return get_transaction.Process(request)
