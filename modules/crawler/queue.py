"""
Crawler Queue

Thread-safe Breadth-First Search queue used by the
URL Discovery module.
"""

from __future__ import annotations

from collections import deque
from threading import Lock

# ==========================================================
# Crawl Queue
# ==========================================================


class CrawlQueue:
    """
    Thread-safe Breadth-First Search queue.

    Stores:

        • URL
        • Crawl depth
        • Parent URL
    """

    def __init__(self):

        self._queue = deque()

        self._visited = set()

        self._queued = set()

        self._lock = Lock()

    # ------------------------------------------------------
    # Enqueue
    # ------------------------------------------------------

    def enqueue(
        self,
        url: str,
        depth: int = 0,
        parent: str | None = None,
    ) -> bool:
        """
        Add URL into queue.

        Returns:
            True  -> queued
            False -> already queued/visited
        """

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

    # ------------------------------------------------------
    # Dequeue
    # ------------------------------------------------------

    def dequeue(
        self,
    ) -> dict | None:
        """
        Remove next URL from queue.
        """

        with self._lock:

            if not self._queue:

                return None

            item = self._queue.popleft()

            self._queued.discard(item["url"])

            return item

    # ------------------------------------------------------
    # Empty
    # ------------------------------------------------------

    def empty(
        self,
    ) -> bool:
        """
        Check whether queue is empty.
        """

        with self._lock:

            return len(self._queue) == 0

    # ------------------------------------------------------
    # Queue Size
    # ------------------------------------------------------

    def size(
        self,
    ) -> int:
        """
        Current queue size.
        """

        with self._lock:

            return len(self._queue)

    # ------------------------------------------------------
    # Mark Visited
    # ------------------------------------------------------

    def mark_visited(
        self,
        url: str,
    ) -> None:
        """
        Mark URL as visited.
        """

        with self._lock:

            self._visited.add(url)

            self._queued.discard(url)

    # ------------------------------------------------------
    # Is Visited
    # ------------------------------------------------------

    def visited(
        self,
        url: str,
    ) -> bool:
        """
        Check whether URL has been visited.
        """

        with self._lock:

            return url in self._visited

    # ------------------------------------------------------
    # Is Queued
    # ------------------------------------------------------

    def queued(
        self,
        url: str,
    ) -> bool:
        """
        Check whether URL is already waiting
        inside the queue.
        """

        with self._lock:

            return url in self._queued

    # ------------------------------------------------------
    # Total Visited
    # ------------------------------------------------------

    def visited_count(
        self,
    ) -> int:
        """
        Number of visited URLs.
        """

        with self._lock:

            return len(self._visited)

    # ------------------------------------------------------
    # Visited URLs
    # ------------------------------------------------------

    def visited_urls(
        self,
    ) -> set:
        """
        Return visited URL set.
        """

        with self._lock:

            return set(self._visited)

    # ------------------------------------------------------
    # Queued URLs
    # ------------------------------------------------------

    def queued_urls(
        self,
    ) -> set:
        """
        Return queued URL set.
        """

        with self._lock:

            return set(self._queued)

    # ------------------------------------------------------
    # Clear
    # ------------------------------------------------------

    def clear(
        self,
    ) -> None:
        """
        Reset queue state.
        """

        with self._lock:

            self._queue.clear()

            self._visited.clear()

            self._queued.clear()
