import mercadopago
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from backend.models import Agendamento
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

sdk = mercadopago.SDK("TEST-8599656277955093-031311-ea1558b606c8d91e9177213ec237c9dd-447564530")

@csrf_exempt
def webhook_mercadopago(request):

    if request.method == "POST":

        data = json.loads(request.body)

        print("WEBHOOK RECEBIDO:", data)

        if data.get("type") == "payment":

            payment_id = data["data"]["id"]

            payment = sdk.payment().get(payment_id)["response"]

            print("STATUS:", payment["status"])

            if payment["status"] == "approved":

                agendamento = Agendamento.objects.get(payment_id=payment_id)

                agendamento.pago = True
                agendamento.save()

                print("Pagamento confirmado!")

    return JsonResponse({"status": "ok"})


@login_required
def pagar_pix(request, agendamento_id):

    agendamento = get_object_or_404(Agendamento, id=agendamento_id)

    payment_data = {
        "transaction_amount": .10,
        "description": "Reserva de quadra",
        "payment_method_id": "pix",
        "payer": {
            "email": request.user.email
        }
    }

    payment_response = sdk.payment().create(payment_data)
    payment = payment_response["response"]

    qr_code = payment["point_of_interaction"]["transaction_data"]["qr_code"]
    qr_code_base64 = payment["point_of_interaction"]["transaction_data"]["qr_code_base64"]

    agendamento.payment_id = payment["id"]
    agendamento.save()

    context = {
        "qr_code": qr_code,
        "qr_code_base64": qr_code_base64,
        "agendamento": agendamento
    }

    return render(request, "pagamento.html", context)