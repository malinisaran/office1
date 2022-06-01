from django.conf import settings
import os
from django.db import models
from django.core.files.storage import FileSystemStorage

# Create your models here.


class Data(models.Model):
    playlist = models.CharField('playlist_name', max_length=1024)
    resolutions = models.CharField(
        'video resolution', max_length=100, null=True)

    def get_data_dirname(self):
        return os.path.join(settings.MEDIA_VIDEO_ROOT, str(self.id))

    def get_upload_dirname(self):
        return os.path.join(self.get_data_dirname(), "raw")

    def get_chunk_dirname(self):
        return os.path.join(self.get_data_dirname(), "hls")

    def create_resolution_dir(self, resolution):
        return os.path.join(self.get_chunk_dirname(), resolution)

    def get_360_chunk_dirname(self):
        return os.path.join(self.get_chunk_dirname(), "360")

    def get_480_chunk_dirname(self):
        return os.path.join(self.get_chunk_dirname(), "480")

    def get_720_chunk_dirname(self):
        return os.path.join(self.get_chunk_dirname(), "720")

    def get_1080_chunk_dirname(self):
        return os.path.join(self.get_chunk_dirname(), "1080")

    def get_preview_path(self):
        return os.path.join(self.get_data_dirname(), 'preview.jpeg')

    def get_video_path(self):
        return os.path.join(self.get_upload_dirname(), self.clientfile_set.file)


class MyFileSystemStorage(FileSystemStorage):
    def get_valid_name(self, name):
        return name

    def get_available_name(self, name, max_length=None):
        if self.exists(name) or (max_length and len(name) > max_length):
            raise IOError(
                '`{}` file already exists or its name is too long'.format(name))
        return name


def upload_path_handler(instance, filename):
    # relative path is required since Django 3.1.11
    path = os.path.join(os.path.relpath(
        instance.data.get_upload_dirname(), settings.MEDIA_ROOT), filename)
    print(path)
    return os.path.join(os.path.relpath(instance.data.get_upload_dirname(), settings.MEDIA_ROOT), filename)


# For client files which the user is uploaded
class ClientFile(models.Model):
    data = models.ForeignKey(
        Data, on_delete=models.CASCADE, null=True, related_name='client_files')
    file = models.FileField(upload_to=upload_path_handler,
                            max_length=1024, storage=MyFileSystemStorage)

    class Meta:
        unique_together = ("data", "file")

    def get_file_name(self):
        return self.file.name


class Video(models.Model):
    name = models.CharField('video_name', max_length=1024)
    data = models.OneToOneField(Data, on_delete=models.CASCADE, null=True,
                                related_name='data')
