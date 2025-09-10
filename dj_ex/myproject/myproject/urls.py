from django.contrib import admin
from django.urls import path
from asy.views import drf_index_view, StreamingAIResponseDRFView

urlpatterns = [
    path('admin/', admin.site.urls),

    # صفحه‌ی تست
    path('drf-example/', drf_index_view, name='drf_example_index'),

    # اندپوینت استریم SSE
    path('api/v1/stream-ai-response/', StreamingAIResponseDRFView.as_view(), name='api_stream_drf'),
]
