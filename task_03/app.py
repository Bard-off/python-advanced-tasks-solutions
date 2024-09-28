__all__ = ("app",)

import logging

from aiohttp import web

from core.currency_rates_getter import CurrencyRatesGetter
from helpers.request_param_reader import get_currency_and_date_from_request

log = logging.getLogger(__name__)

routes = web.RouteTableDef()


@routes.get("/rates/{currency}")
@routes.get("/rates/{currency}/{date}")
async def get_currency_rates(request: web.Request):
    currency, selected_date = get_currency_and_date_from_request(request)
    log.info("Fetching %r rates for date = %s", currency, selected_date)
    getter = CurrencyRatesGetter(
        currency=currency,
        for_date=selected_date,
    )
    info_bytes = await getter.get_currency_info()
    log.info("Sending response for %r rates on date = %s", currency, selected_date)
    return web.json_response(body=info_bytes)


def create_app() -> web.Application:
    web_app = web.Application()
    web_app.add_routes(routes)
    return web_app


app = create_app()
