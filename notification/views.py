from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification

class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        notifications = Notification.objects.filter(receiver=user).order_by('created_at')

        notification_data = [
            {
                "message" : notification.message,
                "time": notification.time_since_created()
            }
            for notification in notifications
        ]

        return Response({"notifications" : notification_data}, status=200)

# Create your views here.
