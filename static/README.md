# UI Styling Notes

The application UI is styled through `static/css/app.css`.

## Areas Improved

- Shared application layout and navigation.
- Dashboard cards and quick actions.
- Certificate list and form screens.
- Login and delete confirmation screens.
- Public verification form.
- Verification result states for Valid, Tampered, and Not Found.
- Generated certificate PDF layout.

## Responsive Behavior

The stylesheet includes mobile rules for:

- stacked page headers
- full-width primary actions
- responsive certificate table controls
- tighter page spacing

## Interaction Polish

Buttons, nav links, and cards use small transitions for hover and focus states. The UI keeps a restrained administrative style so repeated certificate management remains easy to scan.

## Manual Checks

Run the server and check:

```text
venv/bin/python manage.py runserver
```

Then visit:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/verify/
http://127.0.0.1:8000/login/
http://127.0.0.1:8000/dashboard/
http://127.0.0.1:8000/certificates/
```

Use a narrow browser viewport to confirm buttons and tables do not overlap.
