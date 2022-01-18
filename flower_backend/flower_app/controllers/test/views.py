from django.core.mail import EmailMultiAlternatives
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from http import HTTPStatus

class TestView(APIView):
    def get(self, request):

        print("coucou, début du test.")

        msg = EmailMultiAlternatives(
            "test_title",
            # message:
            "test_message",
            # from:
            "coucouTest@mail.com",
            # to:
            ["timothe.rosaz@insa-rennes.fr"]
        )
        print("Sending..." + str(msg))
        msg.send()
        print("over !")

        return Response("oui", status=HTTPStatus.UNAUTHORIZED)

