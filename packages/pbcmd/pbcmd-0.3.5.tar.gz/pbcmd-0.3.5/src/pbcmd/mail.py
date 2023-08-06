"""Send an email using a remote SMTP server."""

import sys
import ssl
import json
import smtplib

import click

from . import cli
from .obscure import text_unobscure


@cli.command()
@click.option("-a", "--auth-file", required=True, help="Authentication file.")
@click.option("-t", "--to", type=str, required=True, help="Recipient email address.")
@click.option("-s", "--subject", required=True, help="Subject of the email.")
@click.option(
    "-b", "--body-file", default=None, help="Text file containing body of the email."
)
def mail(auth_file, to, subject, body_file):
    """Send an email."""
    with open(auth_file, "rt") as fobj:
        auth = fobj.read()
        auth = text_unobscure(auth)
        auth = json.loads(auth)

    if body_file is None:
        body_text = sys.stdin.read()
    else:
        with open(body_file, "rt") as fobj:
            body_text = fobj.read()

    subject = subject.strip()
    body_text = body_text.strip()

    message = f"Subject: {subject}\nTo: {to}\n\n{body_text}"

    context = ssl.create_default_context()
    with smtplib.SMTP(auth["server"], auth["port"]) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(auth["username"], auth["password"])
        server.sendmail(auth["sender_email"], [to], message)

    click.secho("Email sent successfully", fg="green")
