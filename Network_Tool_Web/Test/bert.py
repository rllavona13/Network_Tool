import paramiko
import getpass
import web
from time import sleep
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from multiprocessing import Process, Manager

# host='10.255.3.251'
junname = 'script_bot'
junpass = 'm$Mwk)6P5u'
urls = ('/doBert/(.*)/port/(.*)/period/(.*)', 'do_bert',
        '/stopBert/(.*)/port/(.*)', 'stop_bert',
        '/getBertRes/(.*)/port/(.*)', 'get_bert',
        '/getBertStat/(.*)/port/(.*)', 'get_bert_stat',
        '/coloList/', 'coloList',
        '/portList/(.*)', 'portList',
        '/setPeriod/(.*)/port/(.*)/period(.*)', 'set_period',
        '/check_procs/', 'procheck',
        '/portStat/(.*)/port/(.*)', 'get_port',
        '/whatamidoinghere/', 'guide')

app = web.application(urls, globals())
# dict structure:
# 'ip port':'process'
proc_dict = Manager().dict()


def sleeper_enabler(ip, port, period, proc_dict):
    # web.debug('sleep entered D:')
    sleep(int(period) + 3)
    if proc_dict['%s %s' % (port, ip)][1]:
        # web.debug('bringing back up interface: %s on ip: %s' % (port,ip))
        (ec, msg) = juner().enable_iface(ip, port)
        # web.debug('sleeper command: ec=%s, msg=%s' % (ec,msg))
    # else:
    # web.debug('Iface enable interrupted. Should be already UP')
    del (proc_dict['%s %s' % (port, ip)])


def check_port(ip, port):
    output = juner().cmd(ip, 'show interfaces terse media')
    portlist = ''
    for i in output:
        portlist += i.strip().split()[0]
    if port in portlist:
        output = True
    else:
        output = False
    return output


class juner:
    def cmd(self, ip, cmd):
        try:
            m = paramiko.SSHClient()
            m.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            m.connect(ip, username=junname, password=junpass, allow_agent=False, look_for_keys=False)
            (stdin, stdout, stderr) = m.exec_command(cmd)
            output = stdout.readlines()
            m.close()
        except Exception as ex:
            output = "[Error: %s]" % ex
        return output

    def conn(self, ip):
        try:
            m = paramiko.SSHClient()
            m.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            m.connect(ip, username=junname, password=junpass, allow_agent=False, look_for_keys=False)
            return m
        except Exception as ex:
            output = "[Error: %s]" % ex
            return output

    def disable_iface(self, ip, interface):
        try:
            dev = Device(user=junname, password=junpass, host=ip, port=22)
            dev.open()
            with Config(dev, mode='private') as cfg:
                cfg.load('set interfaces %s disable' % interface, format='set')
                cfg.commit()
            return True, ''
        except Exception as ex:
            output = "[Error: %s]" % ex
            return False, output

    def enable_iface(self, ip, interface):
        # web.debug('gonna enable')
        try:
            dev = Device(user=junname, password=junpass, host=ip, port=22)
            dev.open()
            with Config(dev, mode='private') as cfg:
                cfg.load('set interfaces %s enable' % interface, format='set')
                cfg.commit()
            # web.debug('iface enabled')
            return True, ''
        except Exception as ex:
            output = "[Error: %s]" % ex
            # web.debug('iface not enabled :(')
            return False, output

    def set_period(self, ip, interface, period):
        try:
            dev = Device(user=junname, password=junpass, host=ip, port=22)
            dev.open()
            with Config(dev, mode='private') as cfg:
                cfg.load('set interfaces %s t1-options bert-period %s' % (interface, period))
                cfg.commit()
            return True, ''
        except Exception as ex:
            output = "[Error: %s]" % ex
            return False, output


class procheck:
    def GET(self):
        web.debug(proc_dict.items())
        for i in proc_dict.keys():
            print proc_dict[i]
        # web.debug(pid)
        # for i in proc_dict:
        #    print i
        # print "[ %s ] - [ Alive?: %s ]\n" % (proc_dict.keys()[test.values().index(i)],i.is_alive())


class do_bert:
    def GET(self, ip, interface, period):
        # TODO: verify interface exists on that IP
        # ip,period = ip.split('/period/')[0],ip.split('/period/')[1]
        # print "ip = %s, interface = %s, period = %s " % (ip, interface,period)
        havePort = check_port(ip, interface)
        if havePort:
            try:
                # NOTE: following condition added only during app testing
                # if ip == '10.255.5.251' and interface == 't1-1/0/0:3:3':
                m = juner().conn(ip)
                send = m.exec_command
                if isinstance(m, paramiko.client.SSHClient):
                    bert_period = '10'
                    bert_algori = 'pseudo-2e15-o151'
                    (sin, sot, ser) = send('show interfaces %s detail|find bert|match period' % interface)
                    c_period = sot.readlines()[0].strip().split('period:')[1].split('seconds')[0].strip()
                    # in case we want custom period lengths:
                    if c_period != period:
                        # web.debug('c_period: %s, period: %s' % (c_period,period))
                        (ec, msg) = juner().set_period(ip, str(interface), int(period))
                        # web.debug('ec: %s, msg: %s' % (ec,msg))
                        # start_conf = send('configure private')
                        # set_period_cmd = send('set interfaces %s t1-options bert-period %s' % (interface,period))
                        # set_algori_cmd = send('set interfaces %s t1-options bert-algorithm %s' % (interface,bert_algori))
                        # commit_conf = send('commit')
                        # end_conf = send('exit')
                    # start_disable = send('configure private')
                    # disable_if = send('set interfaces %s disable' % interface)[1]
                    # commit = send('commit')[1]
                    # done = send('exit')
                    (ec, msg) = juner().disable_iface(ip, interface)
                    if ec != True:
                        raise RuntimeError('Could not disable interface, error: %s' % msg)
                    test_cmd = send('test interface %s t1-bert-start' % interface)[1]
                    # web.debug('Bert started')
                    # print test_cmd.readlines()
                    p = Process(target=sleeper_enabler, args=(ip, interface, period, proc_dict))
                    p.start()
                    proc_dict['%s %s' % (interface, ip)] = [p.pid, True]  # , p]
                    # web.debug(proc_dict['%s %s' % (interface,ip)])
                    verify = send('show interfaces %s detail |find bert' % interface)[1]
                    output = verify.readlines()
                    lines = len(output)
                    result = ''
                    m.close()
                    for i in output:
                        lines -= 1
                        result += '[' + i.strip() + ']'
                        if lines != 0:
                            result += ',\n'
                else:
                    raise RuntimeError('Cannot connect')
                    result = ["Error: Could not connect"]
                """else:
                    #ip == '10.255.5.251'
                    #interface == 't1-1/0/0:3:3'
                    bert_period='10'
                    bert_algori='pseudo-2e15-o151'        
                    set_period_cmd = 'set interfaces %s t1-options bert-period %s' % (interface,bert_period)
                    set_algori_cmd = 'set interfaces %s t1-options bert-algorithm %s' % (interface,bert_algori)
                    disable_if = 'set interfaces %s disable' % interface
                    enable_if = 'set interfaces %s enable' % interface
                    test_cmd = 'test interface %s t1-bert-start' % interface
                    stop_cmd = 'test interface %s t1-bert-stop' % interface
                    verify = 'show interfaces %s detail |find bert' % interface
                    output = juner().cmd(ip,verify)
                    result='[NO ACTUAL COMMANDS PERFORMED.],\n'
                    lines = len(output)
                    for i in output:
                        lines-=1
                        result += '['+i.strip()+']'
                        if lines !=0:
                            result+=',\n'
                """
            except Exception as ex:
                result = "[Error: %s]" % ex
        else:
            result = "[Error: Invalid Port Specified]"
        return result


class stop_bert:
    # TODO: make verifying the running test live instead of relying on a running process
    # (this will cover cases when the script dies while a test is being performed,
    # and thus the entry is not in proc_dict)
    def GET(self, ip, interface):
        try:
            if ('%s %s' % (interface, ip)) in proc_dict:
                pid = proc_dict['%s %s' % (interface, ip)][0]
                proc_dict['%s %s' % (interface, ip)] = [pid, False]
                # web.debug('This is pid %s, set in proc_dict to False' % pid)
                juner().cmd(ip, ('test interface %s t1-bert-stop' % interface))
                juner().enable_iface(ip, interface)
                return '[True]'
            else:
                return '[Error: no process running for that interface/ip]'
        except Exception as ex:
            return '[Error: major failure, exception: %s]' % ex


class get_bert:
    def GET(self, ip, interface):
        havePort = check_port(ip, interface)
        if havePort:
            try:
                verify = 'show interfaces %s detail |find bert' % interface
                output = juner().cmd(ip, verify)
                result = ''
                lines = len(output)
                for i in output:
                    lines -= 1
                    result += '[' + i.strip() + ']'
                    if lines != 0:
                        result += ',\n'
            except Exception as ex:
                result = "[Error: %s" % ex
        else:
            result = "[Error: Invalid Port Specified]"
        return result


class get_bert_stat:
    def GET(self, ip, interface):
        havePort = check_port(ip, interface)
        if havePort:
            try:
                verify = 'show interfaces %s detail |find bert' % interface
                output = juner().cmd(ip, verify)
                result = ''
                stat = [s for s in output if 'BERT time period' in s]
                period = stat[0].strip().split('period:')[1].split('seconds')[0].strip()
                elapsed = stat[0].strip().split('Elapsed:')[1].split('seconds')[0].strip()
                if 'completed' in stat[0]:
                    result = '[0, Complete, %s/%s]' % (elapsed, period)
                elif 'in progress' in stat[0]:
                    result = '[1, Running, %s/%s]' % (elapsed, period)
                else:
                    result = '[2, Unexpected error]'
            except Exception as ex:
                result = "[Error: %s]" % ex
        else:
            result = "[Error: Invalid Port Specified]"
        return result


class coloList:
    def GET(self):
        srx_list = open('srx_list.txt', 'r')
        out = '{'
        for i in srx_list:
            l = i.strip()
            out += '[%s:%s],' % (l.split(':')[0], l.split(':')[1])
        out = out.rstrip(',')
        out += '}'
        return out


class portList:
    def GET(self, ip):
        try:
            iface_list = 'show interfaces terse media|match t1'
            output = juner().cmd(ip, iface_list)
            lines = len(output)
            result = ''
            for i in output:
                lines -= 1
                result += '[' + i.strip() + ']'
                if lines != 0:
                    result += ",\n"
        except Exception as ex:
            result = "[Error: %s]" % ex
        return result


class get_port:
    def GET(self, ip, interface):
        try:
            iface_list = 'show interfaces terse media | match %s' % interface
            output = juner().cmd(ip, iface_list)
            lines = len(output)
            # web.debug("lines = %s" % lines)
            result = ''
            for i in output:
                lines -= 1
                result += '[' + i.strip() + ']'
                if lines != 0:
                    result += ",\n"
        except Exception as ex:
            result = "[Error: %s]" % ex
        return result


class guide:
    def GET(self):
        body = ('<html><head><title>What -are- you doing here?</title></head><body>'
                '<h1>Usage:</h1><br><table>'
                '<tr><th>Method</th><th>Syntax</th><th>What do?</th></tr>'
                '<tr><td>/coloList/</td><td>/coloList/</td><td>Returns a list of collocations and IPs where BERT tests can be performed.</td></tr>'
                '<tr><td>/portList/</td><td>/portList/<font color="red">&lt;ip&gt;</font></td><td>Returns all ports that can run a BERT test on specified device ip.</td></tr>'
                '<tr><td>/doBert/</td><td>/doBert/<font color="red">&lt;ip&gt;</font>/port/<font color="red">&lt;port&gt;</font>/period/<font color="red">&lt;period&gt;</font></td><td>Start BERT test on specified port and device and duration (in seconds).</td></tr>'
                '<tr><td>/getBertStat/</td><td>/getBertStat/<font color="red">&lt;ip&gt;</font>/port/<font color="red">&lt;port&gt;</font></td><td>Get BERT test status on specified port and device. Returns if test is running or completed.</td></tr>'
                '<tr><td>/stopBert/</td><td>/stopBert/<font color="red">&lt;ip&gt;</font>/port/<font color="red">&lt;port&gt;</font></td><td>Stop a currently running BERT test on specified port and device. Returns True if successful, Error on failure.</td></tr>'
                '<tr><td>/getBertRes/</td><td>/getBertRes/<font color="red">&lt;ip&gt;</font>/port/<font color="red">&lt;port&gt;</font></td><td>Get BERT test result on specified port and device.</td></tr>'
                '<tr><td>/portStat/</td><td>/portStat/<font color="red">&lt;ip&gt;</font>/port/<font color="red">&lt;port&gt;</font></td><td>Get status of specified port.</td></tr>'
                '<tr><td>/whatamidoinghere/</td><td>/whatamidoinghere/</td><td>This page.</td></tr>'
                '</table></body></html>')
        return body


if __name__ == "__main__":
    app.run()
