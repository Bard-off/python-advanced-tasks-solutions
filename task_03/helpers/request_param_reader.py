from datetime import date

from aiohttp import web


def get_currency_and_date_from_request(
    request: web.Request,
) -> tuple[str, date]:
    currency: str = request.match_info["currency"].lower()
    provided_date: str | None = request.match_info.get("date")
    selected_date = date.today()
    if provided_date is not None:
        try:
            selected_date = date.fromisoformat(provided_date)
        except ValueError:
            raise web.HTTPUnprocessableEntity(
                reason="Provided date is not valid, please use iso format."
            )

    return currency, selected_date
