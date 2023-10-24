from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from tier.models import Tier,CurrentTier
from tier.serializers import TierSerializer,CurrentTier

class GetTierInformation(APIView):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        tiers = Tier.objects.all()
        serializer = TierSerializer(tiers,many=True)
        if request.user.is_authenticated:
            return Response({
                "success":1,
                "data": serializer.data
            })
            