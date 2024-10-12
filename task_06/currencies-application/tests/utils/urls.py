from urllib.parse import urlparse

from core.config import (
    CURRENCIES_LIST_API_URL,
    CURRENCY_API_URL,
)


def extract_host_and_path(url: str) -> tuple[str, str]:
    parsed_url = urlparse(url)
    return (
        parsed_url.hostname,
        parsed_url.path,
    )


if __name__ == "__main__":
    print(extract_host_and_path(CURRENCY_API_URL))
    print(extract_host_and_path(CURRENCIES_LIST_API_URL))
