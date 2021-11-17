from youtubesearchpython import CustomSearch, VideoSortOrder, VideoDurationFilter, VideoUploadDateFilter

from classes.youtube import SearchResults, UploadDate, Duration, SortOrder


class YouTubeSearcher:
    def __init__(self):
        pass

    def search(self,
               query: str,
               max_results: int = 20,
               language: str = 'en',
               region: str = 'US',
               search_filter: str = VideoSortOrder.relevance) -> SearchResults:
        if not search_filter:
            search_filter = VideoSortOrder.relevance
        search = CustomSearch(query=query, limit=max_results, language=language, region=region,
                              searchPreferences=search_filter)
        return SearchResults(search.result(), search_filter=search_filter)

    def search_with_duration(self,
                             query: str,
                             max_results: int = 20,
                             language: str = 'en',
                             region: str = 'US',
                             duration: Duration = None) -> SearchResults:
        return self.search(query, max_results, language, region, duration.value)

    def search_with_sort_order(self,
                               query: str,
                               max_results: int = 20,
                               language: str = 'en',
                               region: str = 'US',
                               sort_order: SortOrder = None) -> SearchResults:
        return self.search(query, max_results, language, region, sort_order.value)

    def search_with_upload_date(self,
                                query: str,
                                max_results: int = 20,
                                language: str = 'en',
                                region: str = 'US',
                                upload_date: UploadDate = None) -> SearchResults:
        return self.search(query, max_results, language, region, upload_date.value)
