from rest_framework import serializers

from .models import Journal, Publisher
from django.conf import settings

class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        exclude = ('publisher', 'id')


class PublisherSerializer(serializers.ModelSerializer):
    journals = JournalSerializer(many = True)

    class Meta:
        model = Publisher
        fields = ('uuid', 'name', 'editor', 'address', 'journals' )

        extra_kwargs = {'journals': {'allow_null': True, 'required': False}}

    def create(self, validated_data: dict) -> Publisher:
        journal_s_data = validated_data.pop('journals')

        publisher_ = Publisher.objects.create(**validated_data)

        if journal_s_data:
            for journal_data in journal_s_data:
                try:
                    journal_ = Journal.objects.get(**journal_data)
                    # staying here means there is journal exists and
                    # some publisher have it
                    # what should we do? raise error or take journal from publisher (bad idea)
                    raise serializers.ValidationError(f'journal {journal_data} already has a publisher')

                except Journal.DoesNotExist:
                    journal_ = Journal.objects.create(publisher = publisher_, **journal_data)

        return publisher_

    def update(self, instance: Publisher, validated_data: dict) -> Publisher:
        journals_data = validated_data.pop('journals')

        journals_ = instance.journals

        instance.name = validated_data.get('name', instance.name)
        instance.editor = validated_data.get('editor', instance.editor)
        instance.address = validated_data.get('address', instance.address)

        if journals_data:
            '''
            journal has reference to publisher
            so, creating new journal with reference to instance
            or changing reference of existing journal (bad idea)
            '''
            for j_item in journals_data:
                try:
                    journal_ = Journal.objects.get(uuid = j_item.get('uuid'))
                    # journal_.publisher = instance
                    raise serializers.ValidationError(f'journal {journal_data} already has a publisher')

                except Journal.DoesNotExist:
                    journal_ = Journal.objects.create(publisher = instance, uuid = j_item.get('uuid'))

        instance.save()

        return instance


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
