""" Network related functions. 
"""
import os
import json
import socket

import dofast as df
from dofast.toolkits.telegram import YahooMail
from dofast.logger import Logger
from .toolkits.telegram import bot_say
from .toolkits.endecode import decode_with_keyfile as dkey
from .config import MESSALERT, AUTH, HTTP_PROXY, TELEGRAM_KEY, PhoneConfig, MailConfig

socket.setdefaulttimeout(30)

logger = Logger('/var/log/phone.log')


class PapaPhone:
    def __init__(self):
        pass

    def get_headers(self):
        h = {}
        h["Cookie"] = dkey(AUTH, PhoneConfig.CMCC_COOKIE)
        h['Authorization'] = dkey(AUTH, PhoneConfig.CMCC_AUTHORIZATION)
        h["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
        h["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        h['device'] = 'iPhone 7'
        h['Referer'] = 'https://h5.ha.chinamobile.com/hnmccClientWap/h5-rest/'
        return h

    def remain_flow(self) -> float:
        try:
            url = 'https://h5.ha.chinamobile.com/h5-rest/flow/data'
            params = {'channel': 2, 'version': '6.4.2'}
            res = df.client.get(url, data=params, headers=self.get_headers())
            json_res = json.loads(res.text)
            flow = float(json_res['data']['flowList'][0]['surplusFlow'])
            unit = json_res['data']['flowList'][0]['surplusFlowUnit']
            logger.info(f'Papa iPhone data flow remain {flow} GB.')
            return flow, unit
        except Exception as e:
            logger.error(f'Get data flow failed: {repr(e)}')
            return -1, 'MB'

    def entry(self, retry: int = 3) -> None:
        import time, random
        receiver = dkey(AUTH, MailConfig.FORMAX_USERNAME)
        if retry <= 0:
            YahooMail().send(receiver, '手机余量查询失败', '已经连续重试 3 次，全部失败。')
            return
        # time.sleep(random.randint(60, 600))
        flow, unit = self.remain_flow()
        if flow == -1:
            self.entry(retry - 1)
        elif flow < 1 or unit == 'MB':
            subject = 'Papa手机流量充值提醒'
            message = f'Papa 的手机流量还剩余 {flow} {unit}，可以充值了。'
            logger.info('\n'.join((receiver, subject, message)))
            YahooMail().send(receiver, subject, message)


class Network:
    """Network related functions"""
    @classmethod
    def is_good_proxy(cls, proxy: str, proxy_type: str = 'socks5') -> bool:
        """Check whether this proxy is valid or not
        :params proxy: str, e.g. tw.domain.com:12345
        :params type:, str, proxy type, either socks or http(c)
        """
        ctype = 'socks5' if proxy_type == 'socks5' else 'proxy'
        resp = df.shell(f'curl -s -m 3 --{ctype} {proxy} ipinfo.io')
        return resp != ''

    def monitor_proxy(self, proxy_str: str = dkey(AUTH, HTTP_PROXY)) -> None:
        local_file = '/tmp/proxy_monitor.json'
        if not os.path.exists(local_file):
            with open(local_file, 'w') as f:
                f.write('{}')
        _info = json.load(open(local_file, 'r'))

        proxy_type = 'http' if proxy_str.startswith('http') else 'socks5'
        if not Network.is_good_proxy(proxy_str, proxy_type):
            failed_count = _info.get(proxy_str, 0) + 1
            if failed_count >= 30:
                msg = str(_info)
                ym = YahooMail()
                ym.send(dkey(AUTH, MailConfig.FORMAX_USERNAME), '代理失效', msg)
                failed_count = -1410  # Check every minute, alert once per day.
            _info[proxy_str] = failed_count
        else:
            _info[proxy_str] = 0

        json.dump(_info, open(local_file, 'w'), indent=2)

    @staticmethod
    def setup_socks5_proxy(port:int=8888):
        ''' setup a socks5 proxy via SSH '''
        assert os.path.exists('/root/.ssh/id_rsa.pub'), 'ssh pub key not set yet.'
        sshpub = df.textread('/root/.ssh/id_rsa.pub')[0]
        authorized_keys = df.textread('/root/.ssh/authorized_keys')
        if sshpub not in authorized_keys:
            with open('/root/.ssh/authorized_keys', 'a+') as f:
                f.write(sshpub + '\n')
        
        df.shell(f'ssh -fND 0.0.0.0:{port} localhost &')
        logger.info(f"SSH proxy {port} setup completes.")        





