from .toolkits.endecode import short_decode, short_encode
from .toolkits.telegram import read_hema_bot, download_file_by_id, bot_messalert
from .network import Network, PapaPhone
from .simple_parser import SimpleParser
from .linuxtools import LinuxTools

msg = """VPS toolkits 😏
-m(--monitor) ip:port ::: Monitor ip:port proxy
-ma(--messalert) message ::: Bot MessAlert. 
-k(--kill) process ::: Kill linux process.
-p(--phone) ::: Papa phone monitor.
-socks [port] ::: Set up a socks5 proxy.
"""


def parse_arguments():
    sp = SimpleParser()
    sp.add_argument('-m', '--monitor')
    sp.add_argument('-ma', '--messalert')
    sp.add_argument('-k', '--kill')
    sp.add_argument('-p', '--phone')
    sp.add_argument('-t', '--test')
    sp.add_argument('-socks', '--socks')
    sp.parse_args()

    if sp.monitor:
        Network().monitor_proxy(sp.monitor.value)

    elif sp.messalert:
        bot_messalert(sp.messalert.value)

    elif sp.kill:
        LinuxTools().pskill(sp.kill.value)

    if sp.phone:
        PapaPhone().entry()
    elif sp.socks:
        port = sp.socks.value
        if port == 'PLACEHOLDER': port = 8888
        Network.setup_socks5_proxy(port)
    else:
        for l in msg.split("\n"):
            c, e = (l + " ::: ").split(':::')[:2]
            print("{:<70} {:<20}".format(c, e))
