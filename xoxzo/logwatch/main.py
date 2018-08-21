#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""[xoxzo.logwatch: Python3 script to monitor log files]"""

import logging
import os
import pytz
import socket
import smtplib
import sys

from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from subprocess import Popen, PIPE

import baker

logger = logging.getLogger(__name__)


def localtime(timezone):
    """
    Returns local time based on specified timezone
    """
    start_utc = datetime.now(pytz.utc)

    try:
        local = pytz.timezone(timezone)
    except pytz.exceptions.UnknownTimeZoneError as e:
        sys.exit("UnknownTimeZoneError: %s" % e)

    start_local = start_utc.astimezone(local)
    return start_local


def within(timezone, timepattern, interval):
    """
    Returns timestamps within interval in minutes
    """
    since = localtime(timezone)

    s_format = timepattern
    timestamps = []

    for i in list(reversed(range(interval))):
        delta = timedelta(minutes=i+1)
        last = since - delta
        timestamps.append(str(last.strftime(s_format)))

    return timestamps


def lookfor(file, pattern, timepattern, timezone, interval):
    """
    Look for a pattern in given files within interval
    """
    message = ''
    timestamps = within(timezone, timepattern, interval)
    since = localtime(timezone).strftime("%H:%M")
    abspath = os.path.abspath(file)
    heading = ("### Looking for %s log in %s "
               "the last %d minutes since %s %s ###\n" %
               (pattern, abspath, interval, since, timezone))
    message = message + heading

    for timestamp in timestamps:
        # add `:` so it will match `HH:MM:`
        # not `HH:MM` which can be mislead to `MM:SS`
        patterns = timestamp + ':' + '.*' + pattern
        stdout, stderr = Popen(['grep', patterns, file],
                               stdout=PIPE).communicate()
        gotcha = stdout.decode("utf-8")

        if gotcha == '':
            print("### Can't find any %s log at %s %s in %s ###" %
                  (pattern, timestamp, timezone, file))
        else:
            print("##### Found matching %s log at %s %s in %s #####" %
                  (pattern, timestamp, timezone, file))
            message = message + gotcha + "\n"

    return message


def send_smtp(file, message, pattern, emails, email_from):
    """
    Send it to email via SMTP
    """
    hostname = socket.gethostname()
    abspath = os.path.abspath(file)
    email_subject = ('[xoxzo.logwatch][%s] %s REPORT at %s' %
                     (hostname, pattern, abspath))

    email_to = []
    for email in emails.strip().split(","):
        email_to.append(email)

    msg = MIMEMultipart('alternative')
    msg['Subject'] = email_subject
    msg['From'] = email_from
    msg['To'] = emails

    body = MIMEText(message, 'plain', 'utf-8')
    msg.attach(body)

    server = smtplib.SMTP('localhost')
    server.sendmail(email_from, email_to, msg.as_string())
    server.set_debuglevel(2)
    server.quit()


def send_django(file, message, pattern, emails, email_from):
    """
    Send it to email via django send_mail() function
    """
    from django.core.mail import send_mail

    hostname = socket.gethostname()
    abspath = os.path.abspath(file)
    email_subject = ("[xoxzo.logwatch][%s] %s REPORT at %s" %
                     (hostname, pattern, abspath))

    email_to = []
    for email in emails.strip().split(","):
        email_to.append(email)

    send_mail(email_subject, message, email_from, email_to)


@baker.command(default=True)
def run(files, pattern, emails, email_from,
        timepattern="%Y-%m-%d %H:%M",
        timezone="UTC",
        interval=5):
    """
    logwatch:
    grep log messages based on pattern within certain
    period of time (default 5 minutes) then send it via email
    """
    since = localtime(timezone).strftime("%H:%M")

    for file in files.strip().split(","):
        message = lookfor(file, pattern, timepattern, timezone, interval)
        suffix = "since %s %s ###\n" % (since, timezone)

        if not message.endswith(suffix):
            try:
                import django
            except ImportError:
                send_smtp(file, message, pattern, emails, email_from)
                print("### An email has been sent to %s via SMTP ###" % emails)
                logger.info("### An email has been sent to %s via SMTP ###" %
                            emails)
            else:
                django_version = django.get_version()
                send_django(file, message, pattern, emails, email_from)
                print("### An email has been sent to %s via Django %s ###" %
                      (emails, django_version))
                logger.info("### An email has been sent to %s "
                            "via Django %s ###" % (emails, django_version))
        else:
            print("### No email has been sent to %s ###" % emails)
            logger.info("### No email has been sent to %s ###" % emails)


def main():
    if len(sys.argv) == 1:
        baker.usage("run")
    baker.run()
