# from ffmpeg_streaming import Formats,Bitrate, Representation, Size,input
# from django import Formats
# import os 



# def encrypted_hls(video):
#     video = input('/media/video/2/raw/video.mp4')
#     hls = video.hls(Formats.h264())
#     _480p  = Representation(Size(854, 480), Bitrate(750 * 1024, 192 * 1024))
#     hls.auto_generate_representations(_480p)
#     hls.output(os.path.join(video.src_dir, 'encrypted_hls', 'test.m3u8'), stderr=True)
    
