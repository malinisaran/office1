import os 
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import (
    VideoSerializer, DataSerializer
)
from .models import Video, Data
from .video_handler import get_file_path, convert_to_hls
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings
# from .ffmpeg_streaming import encrypted_hls
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from django.http import HttpResponse,FileResponse

from stream import serializers


# class UserDetailView(APIView):
@login_required
def home(request):
    return render(request, 'pages/home.html')

def login(request):
    return render(request, 'registration/login.html')


class VideoViewset(viewsets.ModelViewSet):
    queryset = Video.objects.all().select_related('data')
    serializer_class = VideoSerializer
    http_method = ['GET','POST']
    permissions = [IsAuthenticated]

    # def get_permissions(self):
    #     http_method = self.request.method
    #     permissions = [IsAuthenticated]

    @action(methods=['GET', ], detail=False)
    def key(self,request, pk):
        if request.user.is_authenticated():
            print(request.user)
        if request.method == 'GET':
            path = os.path.join(settings.BASE_DIR,"enc.keyinfo")
            with open(path, 'r') as F:
                file = F.read()
            response = HttpResponse(file, content_type="application/keyinfo")
            response['Content-Disposition'] = 'attachment; filename=enc.keyinfo'
            return response

    @action(detail=True, methods=['POST', 'GET'])
    def data(self, request, pk):
        db_video = self.get_object()
        if request.method == 'POST':
            # if db_video.data:
            #     return Response(data='Adding more data is not supported',
            #     status=status.HTTP_400_BAD_REQUEST)
            serializer = DataSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            db_data = serializer.save()
            db_video.data = db_data
            db_video.save()
            data = {k: v for k, v in serializer.data.items()}
            path = db_data.get_upload_dirname()
            hls_path = db_data.get_chunk_dirname()
            full_path = get_file_path(path)
            convert_to_hls(full_path, hls_path)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        elif request.method == 'GET':
            db_data = Data.objects.filter(
                id=db_video.data.id
            ).select_related('data')
            serializer = DataSerializer(db_data, many=True,
                                        context={'request': request})
            print(serializer.data)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

    # @app.get("/playlists/{video_name}.m3u8")
    # async def get_playlist(video_name: str):
    # playlist = here / "data" / "playlists" / f"{sanitize(video_name)}.m3u8"
    # if not playlist.exists():
    #     return HTMLResponse(status_code=404)
    # identifier = secrets.token_hex(16)  # Would be best to do check to make sure there is no conflict with existing
    # m3u8_enc_line = '#EXT-X-KEY:METHOD=AES-128,URI="{base_url}/key/{identifier}/{number}.key",IV=0x{iv}'
    # keys = []
    # out_lines = []
    # instance = -1
    # for line in playlist.read_text().splitlines():
    #     if line.startswith("{{ video_path }}"):
    #         instance += 1
    #         # Generate a secure key and IV to use for encryption.
    #         key = secrets.token_bytes(16)
    #         iv = secrets.token_hex(16)
    #         keys.append({"key": key, "iv": iv})
    #         out_lines.insert(-1, m3u8_enc_line.format(base_url=MY_URL, identifier=identifier, number=instance, iv=iv))
    #         out_lines.append(line.replace("{{ video_path }}", f"/encrypted_video/{identifier}/{instance}/{video_name}"))
    #         continue
    #     out_lines.append(line)
    # encrypted[identifier] = keys
    # return serve_bytes_as_file("\n".join(out_lines).encode("utf-8"), media_type="application/x-mpegURL")