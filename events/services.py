# events/services.py
from .models import Event, RSVP, Bookmark
from django.db.models import Count, Avg, Q
from datetime import datetime, date

def get_upcoming_events():
    return Event.objects.filter(start_time__gt=datetime.now())

def get_past_events():
    return Event.objects.filter(end_time__lt=datetime.now())

def get_today_events():
    today = date.today()
    return Event.objects.filter(start_time__date=today)

def filter_events_by_category(category):
    return Event.objects.filter(category__iexact=category)

def get_events_by_organizer(organizer_id):
    return Event.objects.filter(organizer__id=organizer_id)

def search_events(keyword):
    return Event.objects.filter(
        Q(title__icontains=keyword) |
        Q(description__icontains=keyword) |
        Q(location__icontains=keyword)
    )

def get_events_by_venue(venue_name):
    return Event.objects.filter(venue__iexact=venue_name)

def get_total_event_count():
    return Event.objects.count()

def get_event_count_by_category():
    return Event.objects.values('category').annotate(count=Count('id'))

def get_popular_events():
    return Event.objects.order_by('-rsvp_count')[:10]

def get_trending_events():
    # For demonstration: trending events are those starting soon.
    return Event.objects.filter(start_time__gt=datetime.now()).order_by('start_time')[:10]

def get_average_attendance():
    return Event.objects.aggregate(avg_attendance=Avg('attendees_count'))

def get_recommendations_for_user(user_id):
    # Simple recommendation: return popular events.
    return get_popular_events()

def get_similar_events(event_id):
    try:
        event = Event.objects.get(id=event_id)
        return Event.objects.filter(category=event.category, venue=event.venue).exclude(id=event_id)
    except Event.DoesNotExist:
        return Event.objects.none()

# Action functions for endpoints that modify data
def rsvp_event(event, user):
    rsvp, created = RSVP.objects.get_or_create(event=event, user=user)
    if created:
        event.rsvp_count += 1
        event.save()
    return rsvp

def cancel_rsvp_event(event, user):
    try:
        rsvp = RSVP.objects.get(event=event, user=user)
        rsvp.delete()
        event.rsvp_count = max(0, event.rsvp_count - 1)
        event.save()
        return True
    except RSVP.DoesNotExist:
        return False

def mark_event_completed(event):
    event.status = 'Completed'
    event.save()
    return event

def cancel_event(event):
    event.status = 'Canceled'
    event.save()
    return event

def update_event_status(event, status):
    event.status = status
    event.save()
    return event

def bookmark_event(event, user):
    bookmark, created = Bookmark.objects.get_or_create(event=event, user=user)
    return bookmark
