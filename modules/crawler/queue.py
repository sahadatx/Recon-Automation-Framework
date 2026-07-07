"""
Crawler Queue

Queue management for BFS crawling.
"""

from collections import deque


# ==========================================================
# Crawl Queue
# ==========================================================

class CrawlQueue:
    """
    Breadth-First Search queue.

    Stores:

        URL
        Depth
        Parent URL
    """

    def __init__(self):

        self._queue = deque()

        self._visited = set()

    # ------------------------------------------------------
    # Enqueue
    # ------------------------------------------------------

    def enqueue(
        self,
        url: str,
        depth: int = 0,
        parent: str | None = None,
    ):
        """
        Add URL into queue.
        """

        self._queue.append(

            {

                "url": url,

                "depth": depth,

                "parent": parent,

            }

        )

    # ------------------------------------------------------
    # Dequeue
    # ------------------------------------------------------

    def dequeue(
        self,
    ):
        """
        Remove next URL.

        Returns:
            dict | None
        """

        if self.empty():

            return None

        return self._queue.popleft()

    # ------------------------------------------------------
    # Empty
    # ------------------------------------------------------

    def empty(
        self,
    ):
        """
        Check whether queue is empty.
        """

        return len(
            self._queue
        ) == 0

    # ------------------------------------------------------
    # Queue Size
    # ------------------------------------------------------

    def size(
        self,
    ):
        """
        Current queue size.
        """

        return len(
            self._queue
        )

    # ------------------------------------------------------
    # Mark Visited
    # ------------------------------------------------------

    def mark_visited(
        self,
        url: str,
    ):
        """
        Mark URL as visited.
        """

        self._visited.add(
            url
        )

    # ------------------------------------------------------
    # Is Visited
    # ------------------------------------------------------

    def visited(
        self,
        url: str,
    ):
        """
        Check visited URL.
        """

        return url in self._visited

    # ------------------------------------------------------
    # Total Visited
    # ------------------------------------------------------

    def visited_count(
        self,
    ):
        """
        Number of visited URLs.
        """

        return len(
            self._visited
        )



    # ------------------------------------------------------
    # Visited URLs
    # ------------------------------------------------------

    def visited_urls(
        self,
    ):
        """
        Return visited URL set.

        Returns:
            set
        """

        return self._visited


    # ------------------------------------------------------
    # Clear
    # ------------------------------------------------------

    def clear(
        self,
    ):
        """
        Reset queue.
        """

        self._queue.clear()

        self._visited.clear()


