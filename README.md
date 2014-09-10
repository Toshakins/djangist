Install requirements:
```
pip install Django Celery
```

Run worker as:
```
celery -A dj_start worker -l info  -Q task -I firewall.views
```