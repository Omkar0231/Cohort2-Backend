from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from .models import Hackathon, HackathonApplication
from .serializers import HackathonSerializer, ApplyHackathonSerializer

class HackathonListView(generics.ListAPIView):
    queryset = Hackathon.objects.all().order_by('-start_date')
    serializer_class = HackathonSerializer
    permission_classes = [permissions.AllowAny]

class HackathonDetailView(generics.RetrieveAPIView):
    queryset = Hackathon.objects.all()
    serializer_class = HackathonSerializer
    lookup_field = 'id'
    permission_classes = [permissions.AllowAny]

class ApplyHackathonView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ApplyHackathonSerializer(data=request.data)
        if serializer.is_valid():
            hackathon = serializer.validated_data['hackathon']
            already_applied = HackathonApplication.objects.filter(user=request.user, hackathon=hackathon).exists()
            if already_applied:
                return Response({'message': 'Already applied'}, status=status.HTTP_400_BAD_REQUEST)

            HackathonApplication.objects.create(user=request.user, hackathon=hackathon)
            return Response({'message': 'Application submitted'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
