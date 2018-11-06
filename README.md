```
pipenv install
pipenv run python3 app.py
curl -v -X POST http://localhost:8080/v1/foo -H 'Content-Type: application/json' -d '{"name": "asdf", "id": "asdf"}'
```

This curl responds with:

```
HTTP/1.1 400 Bad Request
{"type": "about:blank", "title": "Bad Request", "detail": "None is not of type 'object'", "status": 400}
```

It should respond with 501 Not Implemented. If you remove the log_middleware on line 50 of app.py the request will work as expected. 
