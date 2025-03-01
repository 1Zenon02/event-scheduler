# events/serializers.py
from rest_framework import serializers
from .models import Organizer, Event, RSVP, Bookmark

class OrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    organizer = OrganizerSerializer()

    class Meta:
        model = Event
        fields = '__all__'

    def create(self, validated_data):
        organizer_data = validated_data.pop('organizer')
        organizer, created = Organizer.objects.get_or_create(**organizer_data)
        event = Event.objects.create(organizer=organizer, **validated_data)
        return event

    def update(self, instance, validated_data):
        organizer_data = validated_data.pop('organizer', None)
        if organizer_data:
            organizer, created = Organizer.objects.get_or_create(**organizer_data)
            instance.organizer = organizer
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class RSVPSerializer(serializers.ModelSerializer):
    class Meta:
        model = RSVP
        fields = '__all__'

class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = '__all__'
