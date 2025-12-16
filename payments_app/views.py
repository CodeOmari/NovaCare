from django.shortcuts import render, redirect, get_object_or_404
from django_daraja.mpesa.core import MpesaClient
from django.contrib import messages
from django.http import HttpResponse
import json

from user_management.models import Details

from payments_app.models import Payment

# Create your views here.

def payment_page(request):
    detail = Details.objects.filter(user=request.user).order_by('-updated_at').first()
    return render(request, 'payment_page.html', {'detail': detail})


def payment(request, id):
    details = get_object_or_404(Details, pk=id)
    charge = request.POST.get("amount")
    amount = int(charge)

    phone_number = details.phone_number


    cl = MpesaClient()
    phone_number = details.phone_number

    account_reference = "NovaCare"
    transaction_desc = 'Hospital bill'
    callback_url = 'https://flying-regularly-honeybee.ngrok-free.app/callback'
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    if response.response_code == "0":
        payment = Payment.objects.create(details=details,
                                          merchant_request_id=response.merchant_request_id,
                                          checkout_request_id=response.checkout_request_id)
        payment.save()
        messages.success(request, f"Your payment was initiated successfully!")
    return redirect('user_management:dashboard')


def callback(request):
    repo = json.loads(request.body)
    data = repo.get['Body']['stkCallback']
    if data["ResultCode"] == "0":
        m_id = ["MerchantRequestID"]
        c_id = ["CheckoutRequestID"]
        code = ""
        item = data["CallbackMetadata"]["Item"]
        for i in item:
            name = i["Name"]
            if name == "MpesaReceiptNumber":
                code = i["Value"]
        registration = Details.objects.get(merchant_request_id=m_id, checkout_request_id=c_id)
        registration.code = code
        registration.status = "COMPLETED"
        registration.save()
    return HttpResponse("OK")