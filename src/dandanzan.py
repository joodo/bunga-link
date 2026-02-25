import json
from typing import override
from urllib.parse import quote_plus
import re

from bs4 import BeautifulSoup

from .bunga_link import *


class DandanzanLinker(BungaLinker):
    @classmethod
    @override
    def info(cls) -> LinkerInfo:
        return LinkerInfo(
            id="dandanzan",
            name="蛋蛋赞",
            url="https://dandanzan.org/",
        )

    @classmethod
    @override
    def search(cls, keyword: str) -> list[SearchResult]:
        url = "https://dandanzan.org/so?q=" + quote_plus(keyword)
        soup = BeautifulSoup(cls._get_http(url), "html.parser")

        li_elements = soup.select("div.lists-content li")

        results = []

        for li in li_elements:
            title = li.select_one("h2").get_text()

            key = str(li.select_one("a.thumbnail").get("href", "none"))
            key = key.strip("/").replace(".html", "").replace("/", "-")

            thumb_url = li.select_one("img").get("src", None)
            if thumb_url is not None:
                thumb_url = "https://dandanzan.org/" + str(thumb_url)

            header = li.select("div.countrie span")
            year = int(header[0].get_text())
            country = header[1].get_text()

            results.append(
                SearchResult(
                    title=title,
                    key=key,
                    thumb_url=thumb_url,
                    country=country,
                    year=year,
                )
            )

        return results

    @classmethod
    @override
    def detail(cls, key: str) -> Media:
        category, item_id = key.split("-")
        url = f"https://dandanzan.org/{category}/{item_id}.html"
        soup = BeautifulSoup(cls._get_http(url), "html.parser")

        title = soup.select_one("h1.product-title").get_text(strip=True)

        year_text = soup.select("header.product-header>span")[0].get_text()
        year = re.findall(r"\d+", year_text)[0]

        thumb_url = "https://dandanzan.org" + str(
            soup.select_one("header.product-header img").get("src")
        )

        detail = soup.select("div.product-excerpt span")
        director = [a.get_text() for a in detail[0].select("a")]
        cast = [a.get_text() for a in detail[1].select("a")]
        genres = [a.get_text() for a in detail[2].select("a")]
        country = "/".join([a.get_text() for a in detail[3].select("a")])
        aka = "/".join([a.get_text() for a in detail[4].select("a")])
        summary = detail[5].get_text(strip=True)

        eps = [
            Episode(id=str(li.get("ep_slug")), title=li.get_text())
            for li in soup.select("ul#eps-ul li")
        ]

        return Media(
            title=title,
            country=country,
            year=year,
            thumb_url=thumb_url,
            director=director,
            cast=cast,
            genres=genres,
            aka=aka,
            summary=summary,
            episodes=eps,
        )

    @classmethod
    @override
    def sources(cls, key: str, ep_id: str) -> list[Source]:
        _, item_id = key.split("-")
        url = f"https://dandanzan.org/fetch_plays/{item_id}/{ep_id}"

        data = json.loads(cls._get_http(url))
        return [
            Source(title=item["src_site"], url=item["play_data"])
            for item in data["video_plays"]
        ]
