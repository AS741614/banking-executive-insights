import logging
import asyncio
import heapq
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from ecos.contracts.base import CognitiveTask, CognitiveTaskPriority
from ecos.runtime.coordinator import CognitiveRuntimeCoordinator

logger = logging.getLogger("ecos.scheduler.distributed")

class DistributedCognitionScheduler:
    """
    Manages the temporal scheduling of cognitive tasks across the distributed enterprise.
    Optimizes for throughput and governance-safe execution windows.
    """
    
    def __init__(self, coordinator: CognitiveRuntimeCoordinator):
        self.coordinator = coordinator
        self._scheduled_tasks: List[tuple[datetime, CognitiveTask]] = []
        self._is_running = False
        self._task_scheduled_event = asyncio.Event()

    def schedule_task(self, task: CognitiveTask, delay_seconds: int = 0):
        """
        Schedules a task for future execution.
        """
        run_at = datetime.utcnow() + timedelta(seconds=delay_seconds)
        heapq.heappush(self._scheduled_tasks, (run_at, task))
        logger.info(f"Task {task.task_id} scheduled for {run_at.isoformat()}")
        self._task_scheduled_event.set()
        self._task_scheduled_event.clear()

    async def _scheduler_loop(self):
        """
        Internal loop to check for tasks ready for execution.
        """
        while self._is_running:
            if not self._scheduled_tasks:
                # Operationalized: Wait for event instead of sleep(1) polling
                await self._task_scheduled_event.wait()
                continue
            
            now = datetime.utcnow()
            run_at, task = self._scheduled_tasks[0]
            
            if now >= run_at:
                heapq.heappop(self._scheduled_tasks)
                logger.info(f"Triggering scheduled task: {task.task_id}")
                await self.coordinator.submit_task(task)
            else:
                # Sleep until the next task is ready or check again soon
                wait_time = (run_at - now).total_seconds()
                try:
                    # Operationalized: Wait for event OR next task time, whichever is first
                    await asyncio.wait_for(self._task_scheduled_event.wait(), timeout=min(wait_time, 1))
                except asyncio.TimeoutError:
                    pass

    async def start(self):
        """
        Starts the distributed cognition scheduler.
        """
        logger.info("Starting ESOTERIC Distributed Cognition Scheduler...")
        self._is_running = True
        asyncio.create_task(self._scheduler_loop())

    async def stop(self):
        """
        Shuts down the scheduler.
        """
        logger.info("Stopping Distributed Cognition Scheduler...")
        self._is_running = False
