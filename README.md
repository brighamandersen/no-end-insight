# No End Insight

An online social media platform for sharing uplifting insights! Only the front-end (HTML and Bootstrap CSS) was completed for school, and I've since hooked it up with a back-end with live data as a fun side project!

![Feed Screenshot](./README-assets/README-feed-screenshot.png)

![New Post Screenshot](./README-assets/README-new-post-screenshot.png)

![Profile Screenshot](./README-assets/README-profile-screenshot.png)

![Login Screenshot](./README-assets/README-login-screenshot.png)

![Register Screenshot](./README-assets/README-register-screenshot.png)

### Installation

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
touch .env
```

Make sure to fill `.env` with correct contents (see [`.env.example`](/.env.example)).

### Virtual environment commands

Create virtual environment

```
python -m venv .venv
```

Activate virtual environment

```
source .venv/bin/activate
```

Deactivate virtual environment

```
deactivate
```

Update requirements.txt with currently installed dependencies

```
pip freeze > requirements.txt
```

Install dependencies listed in requirements.txt

```
pip install -r requirements.txt
```

### Usage locally

```
python app.py
```

### Usage/deployment to production

```bash
cd path/to/repo
./deploy/deploy.sh
```

### TODO

- [ ] Put auth behind middleware for better reuse and separation of concerns.
