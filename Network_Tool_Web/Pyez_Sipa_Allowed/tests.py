from flask import Flask, request, render_template
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
import config

# Test File for Testing the test code for tests
app = Flask(__name__)


# Main loop, it shows sipa_allowed.html, depends the form you use, pass the variable to de if. elif, else loop.
@app.route('/', methods=['GET', 'POST'])
def sipa_form():
    # if commit(html button) is pressed it run the variable to the cfg.load()
    if "commit" in request.form:

        compares = []

        for hosts in config.devices:   # for every host in Config file, run the script and commit the cfg.load()
            dev = Device(user=config.username, password=config.password, host=hosts, port=22)
            dev.open()
            cfg = Config(dev, mode='private')
            cfg.load('set policy-options prefix-list sipa-allowed ' + (request.form['sipa']), format='set')
            compares.append([hosts, cfg.diff().strip()])
            cfg.commit()
            dev.close()
        return render_template("sipa_allowed_commit.html", compares=compares)  # After the loop it show the new config.
    # if delete(html button) is pressed it run the variable to the cfg.load() and run the delete set command
    elif "delete" in request.form:

        compares = []

        for hosts in config.devices:
            dev = Device(user=config.username, password=config.password, host=hosts, port=22)
            dev.open()
            cfg = Config(dev, mode='private')
            cfg.load('delete policy-options prefix-list sipa-allowed ' + (request.form['sipa_delete']), format='set')
            compares.append([hosts, cfg.diff().strip()])
            cfg.commit()
            dev.close()
        return render_template("sipa_allowed_commit.html", compares=compares)  # After the loop it show the new config.

    elif "show" in request.form:  # to be implemented, show the sipa-allow list in all IP in Config File.
        for hosts in config.devices:
            dev = Device(user=config.username, password=config.password, host=hosts, port=22)
            dev.open()
            dev.close()
        return render_template("show_sipa.html")

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