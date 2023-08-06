![Sqreen](https://sqreen-assets.s3-eu-west-1.amazonaws.com/logos/sqreen-logo-264-1.svg)

# [Sqreen](https://www.sqreen.com/)'s Application Security Management for Python

After performance monitoring (APM), error and log monitoring it’s time to add a
security component into your app. Sqreen’s microagent automatically monitors
sensitive app’s routines, blocks attacks and reports actionable infos to your
dashboard.

![Dashboard](https://sqreen-assets.s3-eu-west-1.amazonaws.com/miscellaneous/dashboard.gif)

Sqreen provides automatic defense against attacks:

- Protect with security modules: RASP (Runtime App Self-Protection), In-App WAF
  (Web Application Firewall), Account takeovers [and more](https://www.sqreen.com/modules).

- Sqreen’s modules adapt to your application stack with no need of
  configuration.

- Prevent attacks from the OWASP Top 10 (Injections, XSS and more), 0-days,
  Data Leaks, and more.

- Create security automation playbooks that automatically react against
  advanced business-logic threats.

For more details, visit [sqreen.com](https://www.sqreen.com/).

## Installation

1. Install Sqreen for Python using a recent version of `pip`:
   ```sh
   pip install sqreen
   ```

2. [Signup to Sqreen](https://my.sqreen.com/signup) to get a token for your
   application and write it in a configuration file called `sqreen.ini` in the
   root directory of your project:
   ```ini
   [sqreen]
   token: Your token
   app_name: My Application
   ```

3. Use our CLI (command-line) launcher to start your application with Sqreen:
   ```shell
   # Replace the application module by yours
   sqreen-start gunicorn YOUR_APP_MODULE.wsgi
   ```

   Alternatively, you can also import the `sqreen` module at the top of your
   application (usually the `app.py` or `wsgi.py` file):
   ```python
   import sqreen
   sqreen.start()
   ```

More information about installation are available on
[this page](https://docs.sqreen.com/python/installation/).

## Compatibility

The agent is compatible with Python 2.7, 3.4 and higher. It works
out-of-the-box with most versions of Flask, Django and Pyramid frameworks.

More details are available on
[this page](https://docs.sqreen.com/python/compatibility/).

## Release Notes

Releases announcements are available on
[this page](https://docs.sqreen.com/python/release-notes/).

## License

Sqreen for Python is free-to-use, proprietary software.
