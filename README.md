# Public Service Desk

A mini eCitizen-style web app where citizens report public service problems (broken streetlights, water issues, uncollected garbage) and follow each request until it is resolved. Staff review the requests on an admin dashboard and update their status.

- **Live demo:** https://milashi254.pythonanywhere.com
- **Source code:** https://github.com/Milashi254/service-desk

## Try it: demo logins

| Role | Username | Password |
|---|---|---|
| Citizen | `Milka` | `Milka2026` |
| Admin (staff) | `admin` | `admin2026` |

Usernames are case-sensitive. You can also register a new citizen account with the **Register** button. The demo accounts hold made-up data only.

## Features

**Citizens**
- Public landing page with a problem search and one-click tiles that open the request form with the category preselected
- Register, log in and log out
- Submit a request with a category, location, description and an optional photo
- See their own requests with a colour-coded status (Pending, In Progress, Resolved)
- Open a request to see its full details and photo

**Admin (staff)**
- Dashboard listing every request, with status and category filters
- Open any request and change its status
- Analytics: total, open and resolved requests, resolution rate, and charts by status and by category

**Access control**
- Citizens can only see their own requests
- Staff accounts only use the dashboard and cannot submit requests
- Dashboard pages return 403 Forbidden to citizens

## Tech stack

- Python 3 and Django 6.1
- SQLite database
- Pillow (image uploads)
- Bootstrap 5, Bootstrap Icons and Chart.js, loaded from a CDN

## Project structure

```
service-desk/
├── config/                 # Django settings and root URLs
├── services/               # Main app
│   ├── management/commands/seed_demo.py   # Creates demo users and sample requests
│   ├── admin.py            # Registers requests in Django's built-in admin
│   ├── decorators.py       # staff_required and citizen_required
│   ├── forms.py            # Registration, request and status forms
│   ├── models.py           # ServiceRequest model
│   ├── stats.py            # Numbers and chart data for the dashboard
│   ├── urls.py             # URL routes
│   └── views.py            # Page logic
├── static/images/          # Landing page background photo
├── templates/              # Base layout, home page, registration, citizen and admin pages
├── requirements.txt
└── manage.py
```

## Run it locally (Windows PowerShell)

**Step 1: clone the project and open the folder.**

```
git clone https://github.com/Milashi254/service-desk.git
cd service-desk
```

**Step 2: create and activate a virtual environment.**

```
python -m venv venv
venv\Scripts\Activate.ps1
```

On macOS or Linux, use `source venv/bin/activate` instead. If PowerShell blocks the script, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once.

**Step 3: install the requirements and set up the database.**

```
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
```

`seed_demo` creates the two demo logins and six sample requests.

**Step 4: start the server and open http://127.0.0.1:8000.**

```
python manage.py runserver
```

Optional: run `python manage.py createsuperuser` with a different username (for example `owner`) to get a private login for Django's built-in admin area at `/admin/`.

## Deployment (PythonAnywhere, free plan)

1. Clone the repository in a Bash console and create a virtualenv with Python 3.13.
2. Run `pip install -r requirements.txt` and `python manage.py migrate`.
3. Run `python manage.py collectstatic --noinput` to gather the CSS, images and other static files.
4. Create a manual-configuration web app and point its source code, working directory and virtualenv at the project.
5. Edit the WSGI file so it sets `DJANGO_SETTINGS_MODULE` to `config.settings`.
6. On the Web tab, map `/static/` to the `staticfiles` folder and `/media/` to the `media` folder.
7. Add the site's address to `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` in `config/settings.py`.
8. Run `python manage.py seed_demo`, then click **Reload** on the Web tab.
9. Free web apps expire after one month, so click **Run until 1 month from today** on the Web tab to keep the site running.

## Known limitations

- SQLite and local file storage suit a demo, not heavy traffic
- No email notifications or password reset
- The demo accounts are public, so do not use them for real data

## Credits

- Landing page background photo by microdroneafrica on [Unsplash](https://unsplash.com), used under the [Unsplash License](https://unsplash.com/license)
- Styling and icons: Bootstrap 5 and Bootstrap Icons. Charts: Chart.js