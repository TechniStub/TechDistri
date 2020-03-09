import paypalrestsdk
import qrcode

class Token():
    def __init__(self, id, secret):
        self.id = id
        self.secret = secret


class PayPal():
    def __init__(self, token, sandbox=False, return_url="http://localhost:3000/payment/execute",
                 cancel_url="http://localhost:3000/payment/cancel", fablab_name="Technistub"):
        self.token = token
        self.fablab_name = fablab_name
        self.return_url = return_url
        self.cancel_url = cancel_url
        self.api = paypalrestsdk.Api({
            'mode': 'sandbox' if sandbox else 'live',
            'client_id': self.token.id,
            'client_secret': self.token.secret})

        print('sandbox' if sandbox else 'live')

    def createPayment(self, value, curency="EUR"):
        self.payment = paypalrestsdk.Payment({

            "intent": "sale",

            # Payer
            # A resource representing a Payer that funds a payment
            # Payment Method as 'paypal'
            "payer": {
                "payment_method": "paypal"
            },

            # Redirect URLs
            "redirect_urls": {
                "return_url": self.return_url,
                "cancel_url": self.cancel_url
            },

            # Transaction
            # A transaction defines the contract of a
            # payment - what is the payment for and who
            # is fulfilling it.
            "transactions": [{
                # ItemList
                "item_list": {
                    "items": [{
                        "name": "Ajout de crédit au distributeur du {}".format(self.fablab_name),
                        "sku": "Distributeur",
                        "tax": str(0.0),
                        "price": str(float(value)),
                        "currency": "EUR",
                        "quantity": "1"
                    }]},

                # Amount
                # Let's you specify a payment amount.
                "amount": {
                    "total": str(float(value)),
                    "currency": "EUR"},
                "description": "Ajout de {}{} de crédit au distributeur du {}".format(str(float(value)), curency,
                                                                                      self.fablab_name)}]},
            api=self.api)

        res = self.payment.create()

        self.id = self.payment.id

        return res, self.payment

    def getURL(self, payment=None):
        if payment is None:
            if self.payment is not None:
                payment = self.payment
            else:
                raise NameError(
                    "Payment is not defined, please call self.createPayment() first or give a correct paypalrestsdk.Payment()")

        self.url = ""
        for link in payment.links:
            if link.rel == "approval_url":
                # Convert to str to avoid google appengine unicode issue
                # https://github.com/paypal/rest-api-sdk-python/pull/58
                self.url = str(link.href)
                # print("Redirect for approval: %s" % (approval_url))

        return self.url

    def getQR(self, url=None):
        if url is None:
            if self.url is not None:
                url = self.url
            else:
                raise NameError("URL is not defined, please call self.getUTL() first or give a correct URL")

        return qrcode.make(url)

    def getTransactionState(self, _id=None):
        if _id is None:
            if self.id is not None:
                _id = self.id
            else:
                raise NameError("ID is not defined, please call self.createPayment() first or give a correct ID")

        # print(_id)

        payment = paypalrestsdk.Payment.find(_id, api=self.api)

        return payment.state, payment, payment.transactions[0]

    def acceptPayment(self, payer_id, _id=None):
        if _id is None:
            if self.id is not None:
                _id = self.id
            else:
                raise NameError("ID is not defined, please call self.createPayment() first or give a correct ID")

        self.payment = paypalrestsdk.Payment.find(_id, api=self.api)

        return self.payment.execute({"payer_id": payer_id})


if __name__ == "__main__":
    import PIL
    from time import sleep
    import json

    ppl = PayPal(Token("Token-id",
                       "Token-secret"),
                 sandbox=True,
                 return_url="http://192.168.1.45:3000/return", cancel_url="http://192.168.1.45:3000/cancel")

    res, payment = ppl.createPayment(25)

    print("Res : " + str(res))

    print(ppl.getURL())

    ppl.getQR().show()

    stop = False

    while not stop:
        tr = ppl.getTransactionState()

        print(tr[0])

        data = {}

        try:
            with open('db.json') as json_file:
                data = json.load(json_file)
                if ppl.id in data:
                    print("Validated")
                    break
                else:
                    print("Waiting ", end="")
                    sleep(0.4)
                    for x in range(3):
                        print(".", end="")
                        sleep(0.4)
                    print()
        except:
            print("Something went wrong")

    tr = ppl.getTransactionState()

    print("Approved, email : " + str(tr[2]))

    if ppl.acceptPayment(data[ppl.id]["PayerID"]):  # return True or False
        print("Payment[%s] execute successfully" % payment.id)
    else:
        print(payment.error)

    # TODO : Change PayPal transactionState to mysql w/ nodejs using it
    #  |--> Reference nodejs server in dns or get ip or whatever
    #  |--> Use mysql w/ nodejs