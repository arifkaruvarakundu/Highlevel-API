from rest_framework import serializers

class ContactSerializer(serializers.Serializer):
    id = serializers.CharField()
    customFields = serializers.ListField(child=serializers.DictField())

class UpdateCustomFieldSerializer(serializers.Serializer):
    status = serializers.CharField()
