# Email Sender Service

This repository contains a simple `EmailSender` class and a small FastAPI service that exposes an endpoint to send emails from the configured sender to the configured recipient.

Required environment variables (e.g. in a `.env` file):

- `email` - sender email address (example: your Gmail address)
- `apppassword` - SMTP app password (for Gmail, generate an app password)
- `receipt_email` - recipient email address (where messages will be sent)

Optional environment variables for test script:

- `TEST_SUBJECT` - subject used by `test.py` if provided
- `TEST_CONTENT` - content used by `test.py` if provided

Install dependencies

It's recommended to use a virtual environment. Then:

```bash
pip install -r requirements.txt
```

Run the FastAPI service locally with uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Request example for `/send` (curl):

```bash
curl -X POST "http://localhost:8000/send" -H "Content-Type: application/json" -d '{"subject":"Hello","content":"This is a test"}'
```

Request example for `/send-custom` to a specific recipient (curl):

```bash
curl -X POST "http://localhost:8000/send-custom" -H "Content-Type: application/json" -d '{"target_email":"custom.recipient@example.com","subject":"Hello","content":"This is a test to a custom recipient"}'
```

Notes

- The service uses Gmail's SMTP by default (the existing `EmailSender` implementation). If you want to use a different SMTP provider, update `_send_email` in `email_sender.py`.
- For local development without sending real email, consider running a debug SMTP server or modifying `_send_email` to print the message when a `DRY_RUN` env var is set.

Docker
------

A simple Dockerfile is provided to containerize the service. It embeds the three environment values you requested directly into the image (`email`, `apppassword`, `receipt_email`). Embedding secrets in a Dockerfile is not generally recommended for production — see the security note below.

Build the image:

```bash
docker build -t email-service:latest .
```

Run the container (maps container port 9999 to host port 9999):

```bash
docker run -p 9999:9999 --rm email-service:latest
```

Then POST to the `/send` endpoint:

```bash
curl -X POST "http://localhost:9999/send" -H "Content-Type: application/json" -d '{"subject":"Hello","content":"This is a test"}'
```

Or POST to the `/send-custom` endpoint:

```bash
curl -X POST "http://localhost:9999/send-custom" -H "Content-Type: application/json" -d '{"target_email":"custom.recipient@example.com","subject":"Hello","content":"This is a test"}'
```

Security note
-------------

Storing secrets (email and app passwords) in a Dockerfile is insecure because the resulting image and layers can be inspected and shared. Safer alternatives:

- Use an external environment file (`--env-file .env`) or pass `-e` flags to `docker run` to inject secrets at runtime (do not commit `.env` to source control).
- Use Docker secrets or a secret manager when deploying to orchestration platforms.

