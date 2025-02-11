from rest_framework import serializers

class SummarySerializer(serializers.Serializer):
    summary = serializers.CharField()
    suggested_titles = serializers.ListField(child=serializers.CharField())
    transcription = serializers.CharField()