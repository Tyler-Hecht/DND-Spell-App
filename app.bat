@echo off
echo Starting app
echo Connect to http://localhost:5000 or an address listed below
echo.
flask --app app run --port=5000 --host=0.0.0.0
