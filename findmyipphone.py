from flask import Flask, request, render_template, Response
import urllib
from bs4 import BeautifulSoup
import re
import syslog

# findmyipphone.py Aug 2018 rassiej
# (but hf0002 did the hard work)
# Backend for a Cisco IP Phone app that provides utilities to determine a
# phone's switchport, uniquely identify a phone, and log a physical
# location during deployment.

#################
### Configuration

log_ident    = "findmyipphone"
log_facility = syslog.LOG_LOCAL6
# Syslog tag and facility

debug_ip     = '146.229.2.137'
debug_port   = 8080
# Address and port for Flask debug server

### End configuration
#####################

syslog.openlog(ident=log_ident, logoption=syslog.LOG_PID, facility=log_facility)
syslog.syslog("Started")

app = Flask(__name__)

def getUpstreamSwitchInfo(ip_address):
  phone = {}
  phone['ip'] = ip_address
  phone['switch_name'] = 'Unknown'
  phone['switch_ip'] = 'Unknown'
  phone['switch_port'] = 'Unknown'

  try:
    try:
      # First let's try the line that works on the good phones.
      with urllib.request.urlopen("http://" + ip_address + "/CGI/Java/Serviceability?adapter=device.statistics.port.network") as fp:
        html = fp.read()
    except http.client.BadStatusLine:
      # This happens when we try to hit a non-Java phone with that URL. So let's try the correct URL for a non-Java phone.
      with urllib.request.urlopen("http://" + ip_address + "/Network.html") as fp:
        html = fp.read()

    # We can only hope we have something resembling html at this point
    soup = BeautifulSoup(html, "html.parser")
    tags = soup.find_all("b")               #list of tags
    tags = [tag.get_text() for tag in tags] #list of strings (which are the contents of the tags)

    for index, tag in enumerate(tags):
      # Yes we have to lowercase everything, because different phones have different cases.
      if "neighbor device id" in tag.lower() and tags[index+1] != "":
          phone['switch_name'] = tags[index+1]
          #print("Found switch name = {}".format(phone['switch_name']))
      elif "neighbor ip address" in tag.lower() and tags[index+1] != "":
          phone['switch_ip'] = tags[index+1]
          #print("Found switch ip   = {}".format(phone['switch_ip']))
      # Why don't we retrieve the switch port information?
      # On terrible phones like the CP-3905, the switchport information can come in corrupt.
      # I think this is some disagreement beween the CDP implementation on the phone and on the switch.
      # However, those phones are too terrible to run apps, so we can safely read that data in this context.
      elif "lldp neighbor port" in tag.lower() and tags[index+1] != "":
        phone['switch_port'] = tags[index+1]
        #print("Found switch port = {}".format(phone['switch_port']))

    return phone

  except Exception as e:
    print("ERROR: Problem querying", ip_address, "-", e)
    return phone
    #raise

@app.route('/')
def find():
  remote = request.remote_addr
  phone = getUpstreamSwitchInfo(remote)
  stripped_port = re.sub("[^0-9\/]", "", phone['switch_port'])

  out_text = "This phone is plugged into switch {} port {}".format(phone['switch_name'], stripped_port)

  result = render_template('menu.j2', text=out_text, title='Find My IP Phone')
  return Response(result,mimetype='text/xml')

@app.route('/flare')
def flare():
  devicename = request.args.get('device', default = 'Unknown', type = str)
  phone = getUpstreamSwitchInfo(request.remote_addr)
  stripped_port = re.sub("[^0-9\/]", "", phone['switch_port'])
  result = render_template('text.j2', text='You have successfully sent a support flare from {}'.format(devicename), title='Thanks!')
  print("Flare from {}".format(devicename))
  syslog.syslog("Flare from {} on {} port {}".format(devicename, phone['switch_name'], stripped_port))
  return Response(result,mimetype='text/xml')

@app.route('/iamhere')
def locupdate():
  devicename = request.args.get('device', default = 'Unknown', type = str)
  roomnum = request.args.get('room', default = '000', type = str)
  roomletter = request.args.get('roomletter', default='', type = str)
  phone = getUpstreamSwitchInfo(request.remote_addr)
  stripped_port = re.sub("[^0-9\/]", "", phone['switch_port'])
  result = render_template('text.j2', text='Location update: {} in room {}{} on {} port {}'.format(devicename, roomnum, roomletter, phone['switch_name'], stripped_port), title='Thanks!')
  print("Phone location update: {} in room {}{} on {} port {}".format(devicename, roomnum, roomletter, phone['switch_name'], stripped_port))
  syslog.syslog("Phone location update: {} in room {}{} on {} port {}".format(devicename, roomnum, roomletter, phone['switch_name'], stripped_port))
  return Response(result,mimetype='text/xml')

if __name__ == '__main__':
  app.run(host=debug_ip, port=debug_port)
