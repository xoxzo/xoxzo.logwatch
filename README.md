# xoxzo.logwatch

Monitor log files for certain pattern and send email notification if matched.
`logwatch` is written using Python 3.4.x.

`logwatch` basically is a Python script that takes 4 required arguments:

1. List of files to monitor (comma separated)
2. Pattern to match
3. List of emails to send notification (comma separated)
4. From sender email address

And three optional arguments:

1. Time pattern - the timestamp pattern in the log. By default is using:
   - `%Y-%m-%d %H:%M` which interpreted as `2016-11-08 06:00`

   You can define your own timestamp pattern to match the one in the log you
   want to watch. You may have a look [strftime.org](strftime.org) to see a
   complete list of Python's strftime directives.

2. Timezone - specify timezone (default: UTC). Example:
   - Asia/Tokyo
   - Europe/Amsterdam
   
   For a complete timezone list, please visit
   [pytz](https://pypi.python.org/pypi/pytz/) homepage.

3. Count interval (in minutes) - look for message within last t minutes
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
$ /home/user/.local/bin/logwatch /var/log/local1,/var/log/local2 "ERROR" one@email.com,two@email.com no-reply@email.com --timepattern='%b %-d %H:%M' --timezone=Asia/Tokyo --interval=10
```

Above command is trying to find `ERROR` log at `/var/log/local1` and
`/var/log/local2` using `%b %-d %H:%M` timepattern and if it's found (match),
it will send the result to `one@email.com` and `two@email.com` email addresses
from `no-reply@email.com` using Tokyo timezone.

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
