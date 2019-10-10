from .models import Journal
from rest_framework.serializers import ModelSerializer

class JournalSerializer(ModelSerializer):
    class Meta:
        model = Journal
        fields = '__all__'