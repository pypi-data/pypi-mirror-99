from manga_py.provider import Provider
from manga_py.download_methods import WholeArchiveDownloader
from .helpers.std import Std

class MyMangaListOrg(Provider, Std):
    _downloader = WholeArchiveDownloader

    def get_chapter_index(self) -> str:
        # re = self.re.compile(r'/chapter-[^/]+-(\d+)')
        re = self.re.compile(r'/download/[^/]+?(\d+)')
        return re.search(self.chapter).group(1)

    def get_content(self):
        return self._get_content('{}/read-{}')

    def get_manga_name(self) -> str:
        if ~self.get_url().find('/read'):
            re = r'/read-([^/]+)'
        else:
            re = r'/chapter-([^/]+)-\d+'
        return self._get_name(re)

    def get_chapters(self):
        return self._elements('.chapter_info_download a')

    def get_files(self):
        return []

    def prepare_cookies(self):
        self.cf_scrape(self.get_url())

    def get_cover(self) -> str:
        return self._cover_from_content('img.manga_info_image')

    def book_meta(self) -> dict:
        pass


main = MyMangaListOrg
