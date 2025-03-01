# events/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Event
from .serializers import EventSerializer, RSVPSerializer, BookmarkSerializer
from .services import (
    get_upcoming_events, get_past_events, get_today_events,
    filter_events_by_category, get_events_by_organizer, search_events,
    get_events_by_venue, get_total_event_count, get_event_count_by_category,
    get_popular_events, get_trending_events, get_average_attendance,
    get_recommendations_for_user, get_similar_events,
    rsvp_event, cancel_rsvp_event, mark_event_completed, cancel_event,
    update_event_status, bookmark_event
)

# --- CRUD Endpoints for Events ---
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def event_list_create(request):
    if request.method == 'GET':
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'GET':
        serializer = EventSerializer(event)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# --- Non‑CRUD Endpoints ---
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def upcoming_events_view(request):
    events = get_upcoming_events()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def past_events_view(request):
    events = get_past_events()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def today_events_view(request):
    events = get_today_events()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def events_by_category_view(request, category):
    events = filter_events_by_category(category)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def events_by_organizer_view(request, organizer_id):
    events = get_events_by_organizer(organizer_id)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_events_view(request):
    keyword = request.query_params.get('q', '')
    events = search_events(keyword)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def events_by_venue_view(request, venue_name):
    events = get_events_by_venue(venue_name)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def total_events_count_view(request):
    count = get_total_event_count()
    return Response({'total_events': count})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def events_count_by_category_view(request):
    counts = get_event_count_by_category()
    return Response(counts)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def popular_events_view(request):
    events = get_popular_events()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trending_events_view(request):
    events = get_trending_events()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def average_attendance_view(request):
    avg = get_average_attendance()
    return Response(avg)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommendations_view(request, user_id):
    events = get_recommendations_for_user(user_id)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def similar_events_view(request, event_id):
    events = get_similar_events(event_id)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rsvp_event_view(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    user = request.user
    rsvp = rsvp_event(event, user)
    serializer = RSVPSerializer(rsvp)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_rsvp_view(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    user = request.user
    success = cancel_rsvp_event(event, user)
    if success:
        return Response({'message': 'RSVP cancelled successfully'})
    else:
        return Response({'error': 'RSVP not found'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_event_completed_view(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    event = mark_event_completed(event)
    serializer = EventSerializer(event)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_event_view(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    event = cancel_event(event)
    serializer = EventSerializer(event)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_event_status_view(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    new_status = request.data.get('status')
    if new_status not in dict(Event.STATUS_CHOICES):
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
    event = update_event_status(event, new_status)
    serializer = EventSerializer(event)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bookmark_event_view(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    user = request.user
    bookmark = bookmark_event(event, user)
    serializer = BookmarkSerializer(bookmark)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
