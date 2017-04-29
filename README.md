# deepsleep1

A simple django app with signup, account activation, login, change password, and user list.

Create a file keys.json in app/settings based on keys.json.sample. Replace all the fields with proper values.

Run the server with command:
```
python manage.py runserver --settings=settings.dev
```
(since there are no prod settings yet.)

API endpoints
signup
```
/api/v1/users/signup/
```
log in
```
/api/v1/users/login/
```
user list
```
/api/v1/users/
```
change password
```
/api/v1/users/change_password/
```
Account activation
```
/api/v1/users/<pk>/activate/
```
