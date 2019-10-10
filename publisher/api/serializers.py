from rest_framework import serializers

from .models import Journal, Publisher

class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        exclude = ('publisher', )


class PublisherSerializer(serializers.ModelSerializer):
    journals = JournalSerializer(many = True)

    class Meta:
        model = Publisher
        fields = ('uuid', 'name', 'editor', 'address', 'journals' )

    def create(self, validated_data: dict) -> Publisher:
        journal_s_data = validated_data.pop('journals')

        publisher_ = Publisher.objects.create(**validated_data)

        for journal_data in journal_s_data:
            try:
                journal_ = Journal.objects.get(**journal_data)
            
            except Journal.DoesNotExist:
                journal_ = Journal.objects.create(publisher = publisher_, **journal_data)

        return publisher_