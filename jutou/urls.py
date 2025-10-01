from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'jutou'

urlpatterns = [
    path('', views.index, name='index'),
    path('topics/', views.topics, name='topics'),
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    path('new_topic/', views.new_topic, name='new_topic'),
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    path('delete_entry/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    path('delete_topic/<int:topic_id>/', views.delete_topic, name='delete_topic'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)