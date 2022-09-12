from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('', views.home, name="home"),
    path('like', views.like, name='like'),
    path('tags/<str:key>', views.browse_tags, name='browse_tags'),
    path('campus/<str:key>', views.browse_campus, name='browse_campus'),
    path('department/<str:key>', views.browse_department, name='browse_department'),
    path('events/',views.events, name="events"),
    path('dashboard/',views.events, name="dashboard"),
    path('list/',views.myListing, name="list"),
    path('delete/<str:pk>',views.deleteEvent, name="delete"),
    path('create-event/',views.createEvent, name="create-event"),
    path('edit-event/<str:pk>',views.Edit_Event, name="edit-event"),
    # path('event/<str:pk>',views.singlEvent, name="event"),
    path('singlevent/<str:pk>/',views.singlEvent, name="single-event"),
    path('update-event/<str:pk>/',views.updateEvent, name="update-event"),
    path('search/', views.Event_search, name='search'),

    # path('room_page/<str:pk>/', views.room, name="room"),

    # path('create-room/', views.createRoom, name="create-room"),
    #  path('update-room/<str:pk>', views.updateRoom, name="update-room"),
    #  path('delete-room/<str:pk>', views.deleteRoom, name="delete-room"),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
