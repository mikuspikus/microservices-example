from .models import Journal
from rest_framework import serializers

from django.conf import settings

class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = '__all__'

class AppAuthSerializer(serializers.Serializer):
    '''
    '''
    APP_ID = settings.APP_ID
    APP_SECRET = settings.APP_SECRET

    app_id = serializers.CharField(label = 'App ID')
    app_secret = serializers.CharField(label = 'App Secret')

    def __custom_validation(self, app_id: str, app_secret: str) -> bool:
        return app_id == self.APP_ID and app_secret == self.APP_SECRET

    def validate(self, attrs: dict) -> dict:
        app_id, app_secret = attrs.get('app_id'), attrs.get('app_secret')

        if app_id and app_secret:
            is_valid = self.__custom_validation(app_id, app_secret)

            if not is_valid:
                msg = 'Invalid APP_ID and APP_SECRET'
                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = 'Must include \'app_id\' and \'app_secret\''
            raise serializers.ValidationError(msg, code='authorization')

        return attrs