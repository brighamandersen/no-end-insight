# No End Insight

An online social media platform for sharing uplifting insights! Only the front-end (HTML and Bootstrap CSS) was completed for school, and I've since hooked it up with a back-end with live data as a fun side project!

### Installation

```
touch .env
```

### Usage locally

```
python app.py
```

### Usage with gunicorn

`python3 -m gunicorn -w 1 --bind 0.0.0.0:5000 wsgi:app --daemon`

Just 1 worker process because I only have 1 CPU on the virtual server

The `--daemon` starts it in the background
