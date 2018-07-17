"""
This version need some fix, it need security, and the front end needs some style.

"""
__AUTHOR__ = 'Ramon Rivera Llavona'
__COPYRIGHTS__ = 'Ramon Rivera Llavona - rllavona13@me.com'

from flask import Flask, request, render_template
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
import config

app = Flask(__name__)


class JunosDevices:

    # this class is for opening the connection to the Junipers, we use the object in the main loop below.
    # it uses a custom module which have the credentials and the list of the MX960-1 and MX960-2

    def __init__(self):
        pass

    for hosts in config.devices:
        dev = Device(user=config.username, password=config.password, host=hosts, port=22)


# Main loop, it shows sipa_allowed.html, depends the form you use, pass the variable to de if. elif, else loop.
# If input and submit the commit it will commit the IP in sipa-allowed
# if input is in delete option it will delete the ip from sipa-allowed
# the search is tricky because the Junos PYEZ doesn't support | match, but it returns the config if match
# compares = [] is the equivalent to show|compare, which shows in the web the difference in configuration.
@app.route('/', methods=['GET', 'POST'])
def sipa_form():

    if "commit" in request.form:
        compares = []
        JunosDevices.dev.open()
        cfg = Config(JunosDevices.dev, mode='private')
        cfg.load('set policy-options prefix-list sipa-allowed ' + (request.form['sipa']), format='set')
        compares.append([JunosDevices.hosts, cfg.diff()])  # This function is the equivalent to "show|compare"
        cfg.commit()
        JunosDevices.dev.close()
        return render_template("sipa_allowed_commit.html", compares=compares)

    elif "delete" in request.form:

        compares = []
        JunosDevices.dev.open()
        cfg = Config(JunosDevices.dev, mode='private')
        cfg.load('delete policy-options prefix-list sipa-allowed ' + (request.form['sipa_delete']), format='set')
        compares.append([JunosDevices.hosts, cfg.diff()])
        cfg.commit()
        JunosDevices.dev.close()
        return render_template("sipa_allowed_commit.html", compares=compares)

    elif "search" in request.form:
        JunosDevices.dev.open()
        sipa_search = JunosDevices.dev.cli("show configuration | display set", warning=False)
        data = [i for i in sipa_search.splitlines() if request.form['sipa_search'] in i]
        JunosDevices.dev.close()
        return render_template("show_sipa.html", data=data)

    else:
        return render_template("sipa_allowed.html")


# After the commit in the above loop, it shows another HTML file with the new configuration and a back(HTML button)
# Here it shows the new configuration added and the option to go back to the main page.
# If not it goes to the main page anyway.
@app.route('/sipa_allowed_commit', methods=['GET', 'POST'])
def sipa_commit():

    if "back" in request.submit:
        return render_template('sipa_allowed.html')
    else:
        return render_template('sipa_allowed.html')


# we all know what this means, but for the rookies, it start the web server and run the app. http://localhost:5000
if __name__ == '__main__':

    app.run(port=5000, debug=True)
