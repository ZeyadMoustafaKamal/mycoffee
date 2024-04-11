from rest_framework.generics import CreateAPIView

from .serializers import CreateUserSerializer


class CreateUserView(CreateAPIView):
    serializer_class = CreateUserSerializer
