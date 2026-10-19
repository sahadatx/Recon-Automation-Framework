from __future__ import annotations

from collections import deque
from threading import Lock


class CrawlQueue:


    def __init__(self):

        self._queue = deque()

        self._visited = set()

        self._queued = set()

        self._lock = Lock()


    def enqueue(
        self,
        url: str,
        depth: int = 0,
        parent: str | None = None,
    ) -> bool:


        with self._lock:

            if url in self._visited:

                return False

            if url in self._queued:

                return False

            self._queue.append(
                {
                    "url": url,
                    "depth": depth,
                    "parent": parent,
                }
            )

            self._queued.add(url)

            return True


    def dequeue(
        self,
    ) -> dict | None:


        with self._lock:

            if not self._queue:

                return None

            item = self._queue.popleft()

            self._queued.discard(item["url"])

            return item


    def empty(
        self,
    ) -> bool:


        with self._lock:

            return len(self._queue) == 0


    def size(
        self,
    ) -> int:


        with self._lock:

            return len(self._queue)


    def mark_visited(
        self,
        url: str,
    ) -> None:


        with self._lock:

            self._visited.add(url)

            self._queued.discard(url)


    def visited(
        self,
        url: str,
    ) -> bool:


        with self._lock:

            return url in self._visited


    def queued(
        self,
        url: str,
    ) -> bool:


        with self._lock:

            return url in self._queued


    def visited_count(
        self,
    ) -> int:


        with self._lock:

            return len(self._visited)


    def visited_urls(
        self,
    ) -> set:


        with self._lock:

            return set(self._visited)


    def queued_urls(
        self,
    ) -> set:


        with self._lock:

            return set(self._queued)


    def clear(
        self,
    ) -> None:


        with self._lock:

            self._queue.clear()

            self._visited.clear()

            self._queued.clear()
