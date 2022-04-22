from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Event
from .serializers import EventSerializer
import datetime


class MainEvent(APIView):
    event = Event.objects

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        actual = self.request.query_params.get('actual', None)
        if not pk:
            if actual == "true":
                events = self.event.filter(start_time__gte=datetime.datetime.now()).order_by('start_time')
            else:
                events = self.event.all().order_by('start_time')
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
