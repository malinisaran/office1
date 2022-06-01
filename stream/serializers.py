from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from . import models
import os
import shutil


class ClientFileSerializer(ModelSerializer):
    # media_url = serializers.SerializerMethodField()
    class Meta:
        model = models.ClientFile
        fields = ('file',)

    def get_media_url(self, obj):
        path = self.context['request'].build_absolute_uri(obj.file.url)
        print(f'client_file: {path}')
        return path

    def to_internal_value(self, data):
        print(data)
        return {'file': data}

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['path'] = self.context['request'].build_absolute_uri(instance.file.url)
    #     return response
    # pylint: disable=no-self-use
    # def to_representation(self, instance):
    #     if instance:
    #         upload_dir = instance.data.get_upload_dirname()
    #         return instance.file.path[len(upload_dir) + 1:]
    #     else:
    #         return instance


class DataSerializer(ModelSerializer):
    client_files = ClientFileSerializer(many=True, default=[])

    class Meta:
        model = models.Data
        fields = ('id', 'playlist', 'client_files', 'resolutions')

    def create(self, validated_data):
        client_files = validated_data.pop('client_files')
        db_data = models.Data.objects.create(**validated_data)

        data_path = db_data.get_data_dirname()
        if os.path.isdir(data_path):
            shutil.rmtree(data_path)
        resolutions = (db_data.resolutions).split(',')

        os.makedirs(db_data.get_data_dirname())
        os.makedirs(db_data.get_upload_dirname())
        os.makedirs(db_data.get_chunk_dirname())
        

        for res in resolutions:
            os.makedirs(db_data.create_resolution_dir(res))

        for f in client_files:
            client_file = models.ClientFile(data=db_data, **f)
            client_file.save()

        db_data.save()
        return db_data


class VideoSerializer(ModelSerializer):
    data = serializers.ReadOnlyField(source='data.client_files.file')

    class Meta:
        model = models.Video
        fields = ('id', 'name', 'url', 'data')
