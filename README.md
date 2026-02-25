# Media Library Source for Bunga Player

This project provides the media library sources for [**Bunga Player**](https://github.com/joodo/bunga_player).

## Contributing

To contribute a new source, please follow these steps:

1. **Add a Linker**: Create a new linker file under the `src` directory.
2. **Inherit**: Your class must inherit from the `BungaLinker` base class.
3. **Implement**: Implement all required virtual methods defined in the base class.
4. **Export**: Add you new linker to `src/__init__.py`.

---

### Implementation Example

```python
from typing import override
from .bunga_link import *

class MyNewLinker(BungaLinker):
    @classmethod
    @override
    def info(cls) -> LinkerInfo:
        """Return metadata about this linker, including a URL regex for matching."""
        return LinkerInfo(
            id="unique_provider_id",
            name="Display Name",
            url="https://example.com",
        )

    @classmethod
    @override
    def search(cls, keyword: str) -> list[SearchResult]:
        """Search the source for a keyword and return a list of brief results."""
        # Use cls._get_http(url) to fetch HTML/JSON safely
        return [
            SearchResult(title="Example Movie", key="/v/123", thumb_url=None, year=2024, country="US")
        ]

    @classmethod
    @override
    def detail(cls, key: str) -> Media:
        """Fetch full details and the episode list for a specific media key."""
        return Media(
            title="Example Movie",
            thumb_url="https://example.com/poster.jpg",
            year=2024,
            country="US",
            director=["Director Name"],
            cast=["Actor A", "Actor B"],
            genres=["Sci-Fi"],
            aka="Alternative Title",
            summary="A brief description of the media.",
            episodes=[Episode(id="1", title="Chapter 1")]
        )

    @classmethod
    @override
    def sources(cls, key: str, ep_id: str) -> list[Source]:
        """Return the actual playable video stream URLs for a specific episode."""
        return [
            Source(title="High Quality", url="https://cdn.example.com/video.m3u8")
        ]
```
