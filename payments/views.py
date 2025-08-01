# ✅ Backend: views.py

import razorpay
import hmac
import hashlib
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

# class CreateOrderAPIView(APIView):
#     def post(self, request):
#         amount = request.data.get("amount")  # in rupees
#         client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

#         payment = client.order.create({
#             "amount": int(amount) * 100,  # convert to paise
#             "currency": "INR",
#             "payment_capture": "1"
#         })

#         return Response({
#             "id": payment["id"],
#             "amount": payment["amount"],
#             "currency": payment["currency"],
#             "key": settings.RAZORPAY_KEY_ID
#         })
@api_view(['POST'])
def create_order(request):
    try:
        amount = request.data.get("amount")
        print("Received amount:", amount)

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))

        order = client.order.create({
            "amount": int(amount) * 100,  # Razorpay needs paise
            "currency": "INR",
            "payment_capture": "1"
        })

        return Response({
            "id": order["id"],
            "amount": order["amount"],
            "currency": order["currency"],
            "key": settings.RAZORPAY_KEY_ID
        })
    except Exception as e:
        print("💥 ERROR:", str(e))
        return Response({"error": str(e)}, status=500)

# ////////////////////////////


# def create_order(request):
#     try:
#         amount = request.data.get('amount')  # Make sure this is passed from frontend
#         client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))

#         order = client.order.create({
#             'amount': int(amount),  # Must be in paisa
#             'currency': 'INR',
#             'payment_capture': 1
#         })

#         return Response(order)
#     except Exception as e:
#         print("💥 ERROR:", e)
#         return Response({'error': str(e)}, status=500)




@api_view(["POST"])
def verify_payment(request):
    razorpay_order_id = request.data['razorpay_order_id']
    razorpay_payment_id = request.data['razorpay_payment_id']
    razorpay_signature = request.data['razorpay_signature']

    key_secret = bytes(settings.RAZORPAY_SECRET_KEY, 'utf-8')
    msg = f"{razorpay_order_id}|{razorpay_payment_id}".encode()
    generated_signature = hmac.new(key_secret, msg, hashlib.sha256).hexdigest()

    if generated_signature == razorpay_signature:
        return Response({"status": "Payment Verified"})
    else:
        return Response({"status": "Verification Failed"}, status=400)