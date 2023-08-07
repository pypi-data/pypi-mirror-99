from redpay.session import Session


class ChargeToken:
    def __init__(self, app, key, endpoint) -> None:
        self.app = app
        self.key = key
        self.endpoint = endpoint
        self.route = "/ecard"

    def Process(self, request):
        # Create a session with the server
        session = Session(self.app, self.key, self.endpoint, self.route)

        # Contruct charge token packet
        req = {
            "token": request["token"],
            "action": "TA",
            "amount": request["amount"],
        }

        if "ref1" in request:
            req["ref1"] = request["ref1"]

        if "ref2" in request:
            req["ref2"] = request["ref2"]

        if "ref3" in request:
            req["ref3"] = request["ref3"]

        if "ref4" in request:
            req["ref4"] = request["ref4"]

        if "ref5" in request:
            req["ref5"] = request["ref5"]

        return session.Send(req)
