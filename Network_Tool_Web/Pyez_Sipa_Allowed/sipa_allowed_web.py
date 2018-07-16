"""

By Ramon Rivera Llavona

"""
__VERSION__ = 'Beta 1.0.0'
__AUTHOR_ = 'Ramon Rivera rllavona13@me.com'

from flask import Flask, request, render_template
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
import config


app = Flask(__name__)


class JunosDevices:

    def __init__(self):
        pass

    for hosts in config.devices:  # for every host in Config file, run the script and commit the cfg.load()
        dev = Device(user=config.username, password=config.password, host=hosts, port=22)


# Main loop, it shows sipa_allowed.html, depends the form you use, pass the variable to de if. elif, else loop.
@app.route('/', methods=['GET', 'POST'])
def sipa_form():
    # if commit(html button) is pressed it run the variable to the cfg.load()
    if "commit" in request.form:

        compares = []
        JunosDevices.dev.open()  # call the object dev in class JunosDevices and open the connection
        cfg = Config(JunosDevices.dev, mode='private')
        cfg.load('set policy-options prefix-list sipa-allowed ' + (request.form['sipa']), format='set')
        compares.append([JunosDevices.hosts, cfg.diff()])
        cfg.commit()
        JunosDevices.dev.close()  # call the object dev in class JunosDevices and close the connection
        return render_template("sipa_allowed_commit.html", compares=compares)  # After the loop it show the new config.

    # if delete(html button) is pressed it run the variable to the cfg.load() and run the delete set command
    elif "delete" in request.form:

        compares = []
        JunosDevices.dev.open()  # call the object dev in class JunosDevices and open the connection
        cfg = Config(JunosDevices.dev, mode='private')
        cfg.load('delete policy-options prefix-list sipa-allowed ' + (request.form['sipa_delete']), format='set')
        compares.append([JunosDevices.hosts, cfg.diff()])
        cfg.commit()
        JunosDevices.dev.close()   # call the object dev in class JunosDevices and close the connection
        return render_template("sipa_allowed_commit.html", compares=compares)  # After the loop it show the new config.

    elif "search" in request.form:
        JunosDevices.dev.open()
        data = JunosDevices.dev.cli('show configuration | display set | match sipa-allowed | match '
                                    '' +
                                    (request.form['sipa_search']), format='set')
        JunosDevices.dev.close()
        return render_template("show_sipa.html", data=data)

    else:
        return render_template("sipa_allowed.html")  # if nothing was done it render the HTML again.


# After the commit in the above loop, it shows another HTML file with the new configuration and a back(HTML button)
@app.route('/sipa_allowed_commit', methods=['GET', 'POST'])
def sipa_commit():

    if "back" in request.submit:  # if press back(HTML button) redirect to the main HTML.
        return render_template('sipa_allowed.html')
    else:
        return render_template('sipa_allowed.html')


if __name__ == '__main__':

    app.run(port=5000, debug=True)
