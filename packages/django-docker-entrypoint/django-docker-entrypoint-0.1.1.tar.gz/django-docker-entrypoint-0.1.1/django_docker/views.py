from typing import Optional

from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import LocalhostPermission
from .serializers import RequestSerializer


class HealthCheck(APIView):
    permission_classes = [LocalhostPermission]

    def _get_request_info(self) -> Optional[dict]:
        serializer = RequestSerializer(data={}, context={'request': self.request})
        return serializer.validated_data if serializer.is_valid() else None

    def get(self, request, format=None):
        return Response(
            {
                'STATUS': 'OK',
                'request': self._get_request_info(),
            }
        )
