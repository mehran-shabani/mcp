import asyncio
from django.http import StreamingHttpResponse
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import renderers
# from rest_framework.permissions import IsAuthenticated
# از این کلاس فقط برای مذاکره‌ی محتوا استفاده می‌کنیم
class EventStreamRenderer(renderers.BaseRenderer):
    media_type = "text/event-stream"
    format = "event-stream"
    charset = "utf-8"
    render_style = "text"  # محتوای متنی (SSE)

    def render(self, data, accepted_media_type=None, renderer_context=None):
        # در عمل استفاده نمی‌شود، چون Response ما StreamingHttpResponse است.
        # اما باید وجود داشته باشد تا مذاکره‌ی محتوا 406 ندهد.
        return data

def drf_index_view(request):
    """نمایش صفحه‌ی ساده‌ی تست."""
    return render(request, 'index.html')

class StreamingAIResponseDRFView(APIView):
    """
    استریم SSE در DRF.
    نکته: get باید sync باشد؛ بدنه‌ی استریم می‌تواند async باشد.
    """
    # permission_classes = [IsAuthenticated]
    renderer_classes = [EventStreamRenderer]  # ⇐ کلید رفع 406

    async def _astream(self):
        full_response = (
            "This is a streamed response from a Django REST Framework API endpoint. "
            "It demonstrates how to integrate asynchronous generators with APIViews "
            "for real-time data transfer."
        )
        for idx, word in enumerate(full_response.split()):
            # قالب استاندارد SSE: 'data: ...\n\n'
            yield f"data: Token {idx + 1}: {word}\n\n"
            await asyncio.sleep(0.2)
        yield "data: --- Stream Finished ---\n\n"

    def get(self, request, format=None):
        resp = StreamingHttpResponse(
            self._astream(),                 # async iterator
            content_type="text/event-stream"
        )
        resp["Cache-Control"] = "no-cache"
        # اگر پشت Nginx هستید و با بافرینگ مشکل دارید:
        # resp["X-Accel-Buffering"] = "no"
        return resp
