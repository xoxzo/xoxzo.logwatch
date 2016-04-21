# xoxzo.logwatch

Monitor log files for certain pattern and send email notification if matched.
`logwatch` is written using Python 3.4.x.

`logwatch` basically is a Python script that takes 4 required parameters:

1. List of files to monitor (comma separated)
2. Pattern to match
3. List of emails to send notification (comma separated)
4. From sender email address

And two optional argument:

1. Timezone - specify timezone (default: UTC). Example:
   - Asia/Tokyo
   - Europe/Amsterdam
   
   For a complete timezone list, please visit [pytz](https://pypi.python.org/pypi/pytz/) homepage.
2. Count interval (in minutes) - look for message within last t minutes
   (default: 5 minutes)

# Setup

Setup:

```
$ pip3 install setuptools -U --user
```

Run:

```
$ python3 setup.py develop --user
```

You can now run `logwatch` command:

```
$ which logwatch
```

# Example

Example how to execute `logwatch`:

```
$ /home/user/.local/bin/logwatch /var/log/local1,/var/log/local2 "ERROR" one@email.com,two@email.com no-reply@email.com --timezone=Asia/Tokyo --interval=10
```

Above command is trying to find `ERROR` log at `/var/log/local1` and
`/var/log/local2` and if it's found (match), it will send the result to
`one@email.com` and `two@email.com` email addresses from `no-reply@email.com`
using Tokyo timezone.

## Set as cron job

To make sure you'll get notified via email when something wrong happened,
you can run `logwatch` as cron job.

Set `logwatch` using UTC timezone and run every 5 minutes.

```
$ crontab -e
```

```
5 * * * * /home/user/.local/bin/logwatch /var/log/local1 "ERROR" one@email.com no-reply@email.com
```

# Credits

Credits to the Engineering Team at <a href="https://info.xoxzo.com/">Xoxzo Inc.</a> for `logwatch`
