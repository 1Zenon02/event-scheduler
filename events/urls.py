# events/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # CRUD endpoints for events
    path('', views.event_list_create, name='event_list_create'),
    path('<int:pk>/', views.event_detail, name='event_detail'),
    # Non‑CRUD endpoints
    path('upcoming/', views.upcoming_events_view, name='upcoming_events'),
    path('past/', views.past_events_view, name='past_events'),
    path('today/', views.today_events_view, name='today_events'),
    path('category/<str:category>/', views.events_by_category_view, name='events_by_category'),
    path('organizer/<int:organizer_id>/', views.events_by_organizer_view, name='events_by_organizer'),
    path('search/', views.search_events_view, name='search_events'),
    path('venue/<str:venue_name>/', views.events_by_venue_view, name='events_by_venue'),
    path('count/', views.total_events_count_view, name='total_events_count'),
    path('count/category/', views.events_count_by_category_view, name='events_count_by_category'),
    path('popular/', views.popular_events_view, name='popular_events'),
    path('trending/', views.trending_events_view, name='trending_events'),
    path('average-attendance/', views.average_attendance_view, name='average_attendance'),
    path('recommendations/<int:user_id>/', views.recommendations_view, name='recommendations'),
    path('similar/<int:event_id>/', views.similar_events_view, name='similar_events'),
    path('<int:event_id>/rsvp/', views.rsvp_event_view, name='rsvp_event'),
    path('<int:event_id>/cancel_rsvp/', views.cancel_rsvp_view, name='cancel_rsvp'),
    path('<int:event_id>/completed/', views.mark_event_completed_view, name='mark_event_completed'),
    path('<int:event_id>/cancel/', views.cancel_event_view, name='cancel_event'),
    path('<int:event_id>/update/', views.update_event_status_view, name='update_event_status'),
    path('<int:event_id>/bookmark/', views.bookmark_event_view, name='bookmark_event'),
]
