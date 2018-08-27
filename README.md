# findmyipphone
A Cisco IP Phone app that provides utilities to determine a phone's switchport, uniquely identify a phone, and quickly note its physical location during deployment.

## Dependencies
- Flask
- Jinja2
- MarkupSafe
- Werkzeug
- beautifulsoup4
- bs4
- click
- itsdangerous

## Configuration
Configuration options mostly reside within findmyipphone.py. An example WSGI configuration file is included, but your environment may require something vastly different.

## Files
| Filename                  | Purpose                                        |
| ------------------------- | ---------------------------------------------- |
| findmyipphone.py          | Main Flask script                              |
| apache-findmyipphone.conf | Example mod_wsgi configuration file for apache |
| findmyipphone.wsgi        | Example WSGI configuration                     |
| location-input.xml        | Static file with input fields for location     |
| templates/*.j2            | Jinja2 templates for phone display output      |


