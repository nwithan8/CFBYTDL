from enum import Enum

from youtubesearchpython import VideoDurationFilter, VideoSortOrder, VideoUploadDateFilter


def is_enum(enum, filter_to_check: str) -> bool:
    return filter_to_check in enum.enum_members.values()


class Duration(Enum):
    SHORT = VideoDurationFilter.short
    LONG = VideoDurationFilter.long


class SortOrder(Enum):
    RELEVANCE = VideoSortOrder.relevance
    UPLOAD_DATE = VideoSortOrder.uploadDate
    VIEW_COUNT = VideoSortOrder.viewCount
    RATING = VideoSortOrder.rating


class UploadDate(Enum):
    LAST_HOUR = VideoUploadDateFilter.lastHour
    TODAY = VideoUploadDateFilter.today
    THIS_WEEK = VideoUploadDateFilter.thisWeek
    THIS_MONTH = VideoUploadDateFilter.thisMonth
    THIS_YEAR = VideoUploadDateFilter.thisYear
