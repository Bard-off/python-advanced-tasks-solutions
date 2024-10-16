import json
from datetime import date

from aiohttp import web
from core.currency_exists_check import check


UNKNOWN_CURRENCY_MESSAGE_TEMPLATE = (
    "Unknown currency {currency!r}, please try a different one."
)
INVALID_DATE_MESSAGE = "Provided date is not valid, please use ISO format."


async def validate_currency(currency: str) -> str:
    if await check.currency_exists(currency):
        return currency

    msg = UNKNOWN_CURRENCY_MESSAGE_TEMPLATE.format(currency=currency)
    raise web.HTTPNotFound(
        text=json.dumps({"message": msg}),
        reason=msg,
        content_type="application/json",
    )


def validate_provided_date(provided_date: str | None) -> date:
    selected_date = date.today()
    if provided_date is not None:
        try:
            selected_date = date.fromisoformat(provided_date)
        except ValueError:
            msg = INVALID_DATE_MESSAGE
            raise web.HTTPUnprocessableEntity(
                text=json.dumps({"message": msg}),
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
    selected_date: date = validate_provided_date(
        request.match_info.get("date"),
    )

    return currency, selected_date
