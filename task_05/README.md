

Подсказка:
```shell
poetry init --no-interaction
```

Подсказка, как использовать Poetry в режиме package-mode.
```toml
[tool.poetry]
package-mode = false
```

Как включить `strict` режим в mypy:
```toml
[tool.mypy]
strict = true
```

Расширенный конфиг:
```toml
[tool.mypy]
python_version = "3.12"
strict = true
warn_unreachable = true
warn_return_any = true
warn_unused_configs = true
```

Документация:
https://mypy.readthedocs.io/en/stable/config_file.html#example-pyproject-toml


mypy может запросить дополнительные типы, это делается командой:

```shell
mypy --install-types
```
