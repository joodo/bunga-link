from abc import abstractmethod
from dataclasses import dataclass

import requests


@dataclass
class LinkerInfo:
    id: str
    name: str
    url: str


@dataclass
class SearchResult:
    title: str
    path: str
    thumb_url: str | None
    year: int | None
    country: str | None


@dataclass
class Episode:
    id: str
    title: str


@dataclass
class Media:
    title: str
    thumb_url: str | None
    year: int | None
    country: str | None

    director: list[str] | None
    cast: list[str] | None
    genres: list[str] | None
    aka: str | None
    summary: str | None

    episodes: list[Episode]


@dataclass
class Source:
    title: str
    url: str


class BungaLinker:
    @classmethod
    @abstractmethod
    def info(cls) -> LinkerInfo: ...

    @classmethod
    @abstractmethod
    def search(cls, keyword: str) -> list[SearchResult]: ...

    @classmethod
    @abstractmethod
    def detail(cls, path: str) -> Media: ...

    @classmethod
    @abstractmethod
    def sources(cls, path: str, ep_id: str) -> list[Source]: ...

    @classmethod
    def _get_http(cls, url: str) -> str:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
