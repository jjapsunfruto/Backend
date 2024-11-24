from Housework.models import Housework
from Housework.serializers import HouseworkSerializer
from rest_framework.views import APIView


class CalendarView(APIView):
    def get(self, request, date):
        tasks = Housework.objects.filter(hoseworkDate = date)
        serializer = HouseworkSerializer(tasks, many=True)
        return Response(serializer.data)



# Create your views here.
