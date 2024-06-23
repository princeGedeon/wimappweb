from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from licenceapp.serializers import AddLicenceSerializer


class AddLicenceKeyView(generics.GenericAPIView):
    serializer_class = AddLicenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Licence ajoutée avec succès."}, status=status.HTTP_200_OK)
