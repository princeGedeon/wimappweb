from django.shortcuts import render
from rest_framework import status

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CardInformationSerializer
import stripe



class PaymentAPI(APIView):
    serializer_class = CardInformationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        response = {}
        if serializer.is_valid():
            data_dict = serializer.data
            stripe.api_key = 'your-key-goes-here'
            response = self.stripe_card_payment(data_dict=data_dict)

        else:
            response = {'errors': serializer.errors, 'status':
                status.HTTP_400_BAD_REQUEST
                        }

        return Response(response)


    def stripe_card_payment(self, data_dict):
        try:
            # Créer les détails de la carte
            card_details = {
                "type": "card",
                "card": {
                    "number": data_dict['card_number'],
                    "exp_month": data_dict['expiry_month'],
                    "exp_year": data_dict['expiry_year'],
                    "cvc": data_dict['cvc'],
                },
            }

            # Créer un PaymentIntent
            payment_intent = stripe.PaymentIntent.create(
                amount=10000,  # Montant en centimes (10000 = 100.00 INR)
                currency='inr',
                payment_method_data=card_details,
                confirm=False  # Ne pas confirmer immédiatement
            )

            # Modifier le PaymentIntent pour ajouter les détails de la carte
            payment_intent_modified = stripe.PaymentIntent.modify(
                payment_intent['id'],
                payment_method_data=card_details
            )

            try:
                # Confirmer le PaymentIntent
                payment_confirm = stripe.PaymentIntent.confirm(
                    payment_intent['id']
                )
                payment_intent_modified = stripe.PaymentIntent.retrieve(payment_intent['id'])
            except stripe.error.CardError as e:
                # Gérer les erreurs de paiement
                payment_intent_modified = stripe.PaymentIntent.retrieve(payment_intent['id'])
                payment_confirm = {
                    "stripe_payment_error": "Failed",
                    "code": payment_intent_modified['last_payment_error']['code'],
                    "message": payment_intent_modified['last_payment_error']['message'],
                    'status': "Failed"
                }

            if payment_intent_modified and payment_intent_modified['status'] == 'succeeded':
                response = {
                    'message': "Card Payment Success",
                    'status': 200,
                    "card_details": card_details,
                    "payment_intent": payment_intent_modified,
                    "payment_confirm": payment_confirm
                }
            else:
                response = {
                    'message': "Card Payment Failed",
                    'status': 400,
                    "card_details": card_details,
                    "payment_intent": payment_intent_modified,
                    "payment_confirm": payment_confirm
                }
        except stripe.error.StripeError as e:
            # Gérer les erreurs Stripe générales
            response = {
                'error': str(e),
                'status': 400,
                "payment_intent": {"id": "Null"},
                "payment_confirm": {'status': "Failed"}
            }
        except Exception as e:
            # Gérer d'autres exceptions
            response = {
                'error': str(e),
                'status': 400,
                "payment_intent": {"id": "Null"},
                "payment_confirm": {'status': "Failed"}
            }

        return response
