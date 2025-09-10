import asyncio
import time
from typing import List, Dict

import httpx
from asgiref.sync import async_to_sync, sync_to_async
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework import status

from .models import Task
from .serializers import TaskSerializer

# ---------- helpers (async) ----------
async def _worker(idx: int, delay: float) -> Dict:
    await asyncio.sleep(delay)
    return {"job": idx, "slept": delay}

async def _wait_many_logic(q):
    try:
        jobs = int(q.get("jobs", "5"))
        delay = float(q.get("delay", "1"))
    except ValueError:
        return {"error": "پارامترهای jobs/delay نامعتبرند."}

    if not (1 <= jobs <= 100):
        return {"error": "jobs باید بین 1 تا 100 باشد."}
    if not (0 <= delay <= 30):
        return {"error": "delay باید بین 0 تا 30 ثانیه باشد."}

    started = time.perf_counter()
    results = await asyncio.gather(*[_worker(i, delay) for i in range(jobs)])
    elapsed = round(time.perf_counter() - started, 3)
    return {"results": results, "elapsed_seconds": elapsed, "concurrent": True}

async def _fetch_many_logic(q):
    urls = q.getlist("url")
    if not urls:
        urls = ["https://httpbin.org/delay/1", "https://httpbin.org/uuid"]

    timeout = httpx.Timeout(10.0, connect=5.0)
    started = time.perf_counter()
    async with httpx.AsyncClient(timeout=timeout, http2=True) as client:
        coros = [client.get(u) for u in urls]
        responses: List[httpx.Response] = await asyncio.gather(*coros, return_exceptions=True)

    payload = []
    for u, r in zip(urls, responses):
        if isinstance(r, Exception):
            payload.append({"url": u, "ok": False, "error": str(r)})
        else:
            info = {
                "url": u,
                "ok": r.is_success,
                "status_code": r.status_code,
                "bytes": len(r.content or b""),
                "content_type": r.headers.get("content-type", ""),
            }
            if "application/json" in info["content_type"]:
                try:
                    info["json_preview"] = r.json()
                except Exception:
                    info["json_preview"] = None
            payload.append(info)

    elapsed = round(time.perf_counter() - started, 3)
    return {"elapsed_seconds": elapsed, "responses": payload}

async def _tasks_list_logic():
    # ORM sync است؛ از sync_to_async استفاده می‌کنیم
    tasks = await sync_to_async(list)(Task.objects.order_by("-created_at").all())
    ser = TaskSerializer(tasks, many=True)
    return {"count": len(ser.data), "items": ser.data}

async def _tasks_create_logic(payload):
    ser = TaskSerializer(data=payload)
    if not ser.is_valid():
        return (ser.errors, status.HTTP_400_BAD_REQUEST)
    task = await sync_to_async(ser.save)()
    out = TaskSerializer(task)
    return (out.data, status.HTTP_201_CREATED)

# ---------- Views (entrypointهای sync) ----------
class Ping(APIView):
    def get(self, request: Request):
        # این یکی اصلاً async لازم ندارد
        return Response({"ok": True, "framework": "DRF", "async_entry": False, "message": "pong"})

class WaitMany(APIView):
    def get(self, request: Request):
        data = async_to_sync(_wait_many_logic)(request.query_params)
        # اگر خطا بود، 400 بده
        if "error" in data:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(data)

class FetchMany(APIView):
    def get(self, request: Request):
        data = async_to_sync(_fetch_many_logic)(request.query_params)
        return Response(data)

class TaskListCreate(APIView):
    def get(self, request: Request):
        data = async_to_sync(_tasks_list_logic)()
        return Response(data)

    def post(self, request: Request):
        data, code = async_to_sync(_tasks_create_logic)(request.data)
        return Response(data, status=code)
