from parser.models import Entry

from rest_framework import serializers


class EntrySerializer(serializers.Serializer):
    type = serializers.IntegerField()
    date = serializers.DateField()
    value = serializers.IntegerField()
    cpf = serializers.CharField()
    card = serializers.CharField()
    time = serializers.TimeField()
    owner = serializers.CharField()
    outlet = serializers.CharField()
    
    def create(self, validated_data):
        if not Entry.objects.filter(card=validated_data['card'], date=validated_data['date'], time=validated_data['time']).exists() :
            return Entry.objects.create(**validated_data)
        else:
            raise Exception("Duplicate entries found.")


class EntryViewSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    type = serializers.IntegerField()
    date = serializers.DateField()
    value = serializers.IntegerField()
    cpf = serializers.CharField(write_only=True)
    card = serializers.CharField()
    time = serializers.TimeField()
    owner = serializers.CharField(write_only=True)
    outlet = serializers.CharField(write_only=True)
   
