from __future__ import annotations

from typing import List

from classes.youtube.search_filters import SortOrder, Duration, UploadDate


class SearchResult:
    def __init__(self, data: dict):
        self._data = data

    @property
    def title(self) -> str:
        return self._data['title']

    @property
    def id(self) -> str:
        return self._data['id']

    @property
    def link(self) -> str:
        return self._data['link']

    @property
    def type(self) -> str:
        return self._data['type']

    @property
    def view_count(self) -> int:
        count = self._data['viewCount']['text'].replace(',', '').replace('views', '').replace(' ', '')
        if count == 'No':
            count = 0
        return int(count)

    @property
    def _duration(self) -> str:
        return self._data['duration']

    @property
    def duration_stamp(self) -> str:
        return self._duration

    @property
    def seconds(self) -> int:
        seconds = 0
        for i in self._duration.split(':'):
            seconds = seconds * 60 + int(i)
        return seconds

    @property
    def minutes(self) -> int:
        return self.seconds // 60

    @property
    def hours(self) -> int:
        return self.minutes // 60


class SearchResults:
    def __init__(self, data: dict, search_filter: str):
        self._data = data
        self._filter_used = search_filter
        self.results = [SearchResult(r) for r in self._data['result']]

    @property
    def most_views(self) -> SearchResult | None:
        if self._filter_used == SortOrder.VIEW_COUNT:
            return self.results[0]
        return max(self.results, key=lambda r: r.view_count)

    @property
    def least_views(self) -> SearchResult | None:
        if self._filter_used == SortOrder.VIEW_COUNT:
            return self.results[-1]
        return min(self.results, key=lambda r: r.view_count)

    @property
    def longest_video(self) -> SearchResult | None:
        return max(self.results, key=lambda r: r.seconds)

    @property
    def shortest_video(self) -> SearchResult | None:
        return min(self.results, key=lambda r: r.seconds)

    @property
    def newest_video(self) -> SearchResult | None:
        if self._filter_used == SortOrder.UPLOAD_DATE:
            return self.results[0]
        return None

    def get_results_longer_than(self, seconds: int) -> List[SearchResult]:
        return [r for r in self.results if r.seconds > seconds]

    def get_results_shorter_than(self, seconds: int) -> List[SearchResult]:
        return [r for r in self.results if r.seconds < seconds]

    def get_results_between(self, min_seconds: int, max_seconds: int) -> List[SearchResult]:
        return [r for r in self.results if min_seconds <= r.seconds <= max_seconds]

    def get_results_with_more_than(self, views: int) -> List[SearchResult]:
        return [r for r in self.results if r.view_count > views]

    def get_results_with_less_than(self, views: int) -> List[SearchResult]:
        return [r for r in self.results if r.view_count < views]

    def get_results_of_type(self, item_type: str) -> List[SearchResult]:
        return [r for r in self.results if r.type == item_type]
