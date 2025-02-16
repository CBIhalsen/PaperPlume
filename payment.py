from alipay import AliPay
import stripe
from flask import jsonify
import yaml

from decimal import Decimal

class receiver_payment:

    def __init__(self,type=None,amount=None,uid=None,trade_number=None):
        self.type = type
        self.amount = amount
        self.uid =uid
        self.trade_number = trade_number
    def payment(self):
        print(self.type,"selftype")
        if self.type =="alipay":

            return self.alipay()
        elif self.type == "stripe":
            self.stripe()
            return self.stripe()


    def alipay(self):
        print("alipay")
        with open("./config/alipay_private_key.pem", "r") as private_key_file:
            app_private_key_string = private_key_file.read()

        with open("./config/alipay_public_key.pem", "r") as public_key_file:
            alipay_public_key_string = public_key_file.read()

        #
        with open('./config/currency.yaml', 'r', encoding='utf-8') as config_file:
            config = yaml.safe_load(config_file)
        with open('./config/alipay.yaml', 'r', encoding='utf-8') as config_file:
            appid = yaml.safe_load(config_file)['appid']
        num_str = config['USD-CNY']
        print(num_str)
        # num = Decimal(num_str)
        exchange_rate = Decimal(num_str)
        # exchange_rate = exchange_rate.quantize(Decimal("0.00"))
        print("汇率", exchange_rate)
        # appid="2021004101646681",

        alipay = AliPay(

            appid=appid,
            app_notify_url=None,
            app_private_key_string=app_private_key_string,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",

            debug=False,

        )
        # 调用接口
        # total_pay = order.total_price + order.transit_price
        total_pay =  Decimal(self.amount) * exchange_rate
        print(total_pay)
        total_pay = total_pay.quantize(Decimal("0.00"))+ Decimal("0.01")
        print(total_pay)
        print(self.amount)
        print("浮点金额",float(self.amount),"付款总额",total_pay)
        # uid = str(self.uid)
        # alipay.api_alipay_trade_wap_pay

        order_string = alipay.api_alipay_trade_precreate(
            out_trade_no='uid={},amount={},trade_number={}'.format(self.uid,self.amount,self.trade_number),
            total_amount=str(total_pay),
            timeout_express='15m',
            subject='PaperPlume,汇率：1.00 USD = {} CNY'.format(num_str),
            return_url=None,
            notify_url='https://huge-model-javelin.ngrok-free.app/payment-notification',
        )
        print(order_string)
        # 返回应答\
        # "https://openapi.alipaydev.com/gateway.do",
        # pay_url = "https://openapi.alipay.com/gateway.do?" + order_string
        pay_url = order_string['qr_code']
        print(pay_url)

        return pay_url

    def stripe(self):
        print("stripe")
        with open('./config/stripe.yaml', 'r', encoding='utf-8') as config_file:
            config = yaml.safe_load(config_file)

        stripe.api_key = config['api_key']

        # 创建一个Product
        product = 'prod_OTiqJ0R8CrreCF',

        # 创建一个Price
        price = stripe.Price.create(
            product=config['product'],
            unit_amount=50,  # 设置单位价格，例如500表示5.00美元
            currency='usd',
        )

        # 创建一个Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price.id,
                'quantity': 1,
                "adjustable_quantity": {
                    "enabled": True,
                    "minimum": 1,
                },
            }],

            metadata={
                'user_uid': self.uid  # 替换为您的用户 UID
            },
            invoice_creation={"enabled": True},
            mode='payment',
            success_url='https://your-website.com/success',
            cancel_url='https://your-website.com/cancel',
        )

        # 获取付款链接
        payment_link = session.url

        print(payment_link)
        return payment_link

        # try: payment element methods
        #     # Create a PaymentIntent with the order amount and currency
        #     intent = stripe.PaymentIntent.create(
        #         amount=self.amount,
        #         currency='usd',
        #         automatic_payment_methods={
        #             'enabled': True,
        #         },
        #         metadata={
        #             'user_uid': str(self.uid)  # 替换为您的用户 UID
        #         },
        #         adjustable_quantity={
        #                                  'enabled': True,
        #                                  'minimum': 1,
        #                              },
        #     )
        #     print("stripe yes")
        #     return jsonify({
        #         'clientSecret': intent['client_secret'],
        #         'amount': intent['amount']
        #     })
        # except Exception as e:
        #     print('error')
        #     return jsonify(error=str(e)), 403

