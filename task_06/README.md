## Тестирование приложения

- Настройки `pytest`: https://docs.pytest.org/en/latest/reference/customize.html
- Плагин `pytest-asyncio` для асинхронных тестов https://github.com/pytest-dev/pytest-asyncio
- Пригодится пакет `pytest-aiohttp` https://pypi.org/project/pytest-aiohttp/
- Как тестировать aiohttp server https://docs.aiohttp.org/en/stable/testing.html
- Для замены ответов aiohttp client подойдёт пакет [`aresponses`](https://github.com/aresponses/aresponses)
- Может пригодиться фикстура `tmp_path`: https://docs.pytest.org/en/stable/how-to/tmp_path.html
- Для отчёта по покрытию воспользуйтесь плагином https://pypi.org/project/pytest-cov/
- Исключение строк из отчета покрытия https://coverage.readthedocs.io/en/latest/excluding.html

### Подсказки

Запуск тестов с покрытием и генерация отчёта:
- Запуск pytest с отчётом о покрытии: `pytest --cov`
- Создание HTML отчёта для удобного просмотра в браузере: `coverage html`

Либо всё в одной команде:
```shell
pytest --cov --cov-report=html
```
