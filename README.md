# Работа с виртуальной средой и серверлес

## Включение виртуальной среды

```bash
virtualenv venv -p python3.12
source venv/bin/activate
# Для выхода из виртуальной среды
 deactivate
```

## Развертывание

```bash
# For development
serverless deploy --stage dev --verbose

# For production
serverless deploy --stage prod --verbose

```
## Откатываем неудачное развертывание
```bash
serverless deploy list
serverless rollback --timestamp <timestamp>
```

## Тестирование

```bash
serverless invoke -f numpy --log
```

---

## Источники

- [R2D2Lambda GitHub](https://github.com/viktor-makarov/R2D2Lambda/edit/master/README.md)
- [Serverless Framework GitHub](https://github.com/serverless/serverless)
- [Serverless Documentation](https://www.serverless.com/framework/docs)

