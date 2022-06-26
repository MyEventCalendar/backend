from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Event
from .serializers import EventSerializer, LoginSerializer, RegistrationSerializer
import datetime
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status


class MainEvent(APIView):

    event = Event.objects
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        actual = self.request.query_params.get('actual', None)
        hidden = self.request.query_params.get('hidden', None)
        if not pk:
            if actual == "all" and hidden == "all":
                events = self.event.all()
            elif actual == "all" and hidden == "true":
                events = self.event.filter(hidden=True)
            elif actual == "all" and hidden == "false":
                events = self.event.filter(hidden=False)
            elif actual == "true" and hidden == "all":
                events = self.event.filter(start_time__gte=datetime.datetime.now()).order_by('start_time')
            elif actual == "true" and hidden == "true":
                events = self.event.filter(hidden=True,
                                           start_time__gte=datetime.datetime.now()).order_by('start_time')
            elif actual == "false" and hidden == "all":
                events = self.event.filter(start_time__lt=datetime.datetime.now()).order_by('start_time')
            elif actual == "false" and hidden == "true":
                events = self.event.filter(hidden=False,
                                           start_time__lt=datetime.datetime.now()).order_by('start_time')
            elif actual == "false" and hidden == "true":
                events = self.event.filter(hidden=True,
                                           start_time__lt=datetime.datetime.now()).order_by('start_time')

            else:
                events = self.event.filter(hidden=False,
                                           start_time__gte=datetime.datetime.now()).order_by('start_time')
        else:
            events = self.event.filter(pk=pk)

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self, request, pk):
        instance = get_object_or_404(self.event.all(), pk=pk)
        serializer = EventSerializer(data=request.data, instance=instance, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        events = get_object_or_404(self.event.all(), pk=pk)
        events.delete()
        return Response({"message": "Event with id {} has been deleted.".format(pk)})


class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
