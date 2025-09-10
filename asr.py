import asyncio
import time


async def fetch_data(delay_seconds):
    """Simulates fetching data with a delay."""
    print(f"[{time.strftime('%H:%M:%S')}] Starting data fetch with {delay_seconds}s delay...")

    await asyncio.sleep(delay_seconds)

    print(f"[{time.strftime('%H:%M:%S')}] Finished data fetch after {delay_seconds}s delay.")
    return f"Data fetched after {delay_seconds} seconds"


async def main():
    """Orchestrates multiple asynchronous tasks."""
    print(f"[{time.strftime('%H:%M:%S')}] Main program started.")
    
    # هر دو تسک تقریبا همزمان شروع به کار می‌کنند
    task1 = asyncio.create_task(fetch_data(2))
    task2 = asyncio.create_task(fetch_data(1))

    # منتظر می‌مانیم تا هر دو تسک به پایان برسند
    results = await asyncio.gather(task1, task2) 
    print(f"[{time.strftime('%H:%M:%S')}] All tasks completed. Results: {results}")

if __name__ == "__main__":
    asyncio.run(main())
