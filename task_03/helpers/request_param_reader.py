import json
from datetime import date

from aiohttp import web
from core.currency_exists_check import check


async def validate_currency(currency: str) -> str:
    if await check.currency_exists(currency):
        return currency

    msg = f"Unknown currency {currency!r}, please try a different one."
    raise web.HTTPNotFound(
        body=json.dumps({"message": msg}),
        reason=msg,
        content_type="application/json",
    )


def validate_provided_date(provided_date: str | None) -> date:
    selected_date = date.today()
    if provided_date is not None:
        try:
            selected_date = date.fromisoformat(provided_date)
        except ValueError:
            msg = "Provided date is not valid, please use ISO format."
            raise web.HTTPUnprocessableEntity(
                body=json.dumps({"message": msg}),
                reason=msg,
                content_type="application/json",
            )
    return selected_date


async def get_currency_and_date_from_request(
    request: web.Request,
) -> tuple[str, date]:
    currency: str = await validate_currency(
        request.match_info["currency"].lower(),
    )
    selected_date = validate_provided_date(
        request.match_info.get("date"),
    )

    return currency, selected_date
