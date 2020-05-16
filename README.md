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

## Setup in Unified Communications Manager
To set up the app in Unified CM, go to Device, Device Settings, Phone Services. Set it up as follows:
- Service Name: Find My IP Phone (or whatever you want)
- Service URL: http://your-app-server.example.com/phonetools.xml
- Service Category: XML Service
- Service Type: Standard IP Phone Service
- Enterprise Subscription: Checked if you want every phone to immediately get the app the next time you Reset it from CM or it reboots