#!/usr/bin/env python
# encoding: utf-8

import sys
import argparse
import logging

from utils.daemon import Daemon
from mitmproxy import flow, proxy, controller, options
from mitmproxy.proxy.server import ProxyServer
from utils.parser import ResponseParser, save_cnf, read_cnf
from utils.handle import mingdao_proxy_request_handle, mingdao_proxy_response_handle

logging.basicConfig(
    level=logging.INFO,  # filename='/tmp/mingdaoproxy.log',
    format='%(asctime)s [%(levelname)s] %(message)s',
)


class mingdaoproxy(flow.FlowMaster):

    def __init__(self, opts, server, state):
        super(mingdaoproxy, self).__init__(opts, server, state)

    def run(self):
        try:
            logging.info("MingDao started successfully...")
            flow.FlowMaster.run(self)
        except KeyboardInterrupt:
            self.shutdown()
            logging.info("Ctrl C - stopping MingDao server")

    @controller.handler
    def request(self, f):
        mingdao_proxy_request_handle(f)

    @controller.handler
    def response(self, f):
        mingdao_proxy_response_handle(f)
        parser = ResponseParser(f)
        # print(parser.parser_data())

    # memory overfull bug
    # print(len(self.state.flows))
    # print(self.state.flow_count())
    # self.state.clear()


def start_server(proxy_port, proxy_mode):
    port = int(proxy_port) if proxy_port else 8080
    mode = proxy_mode if proxy_mode else 'regular'

    if proxy_mode == 'http':
        mode = 'regular'

    opts = options.Options(
        listen_port=port,
        mode=mode,
        cadir="/data/MingDao/ssl/",
    )

    config = proxy.ProxyConfig(opts)

    state = flow.State()
    server = ProxyServer(config)
    m = mingdaoproxy(opts, server, state)
    m.run()


class wyDaemon(Daemon):

    def __init__(self, pidfile, proxy_port=62000, proxy_mode='regular'):
        super(wyDaemon, self).__init__(pidfile)
        self.proxy_port = proxy_port
        self.proxy_mode = proxy_mode

    def run(self):
        logging.info("MingDao is starting...")
        logging.info("Listening: 0.0.0.0:{} {}".format(
            self.proxy_port, self.proxy_mode))
        start_server(self.proxy_port, self.proxy_mode)


def run(args):
    if args.restart:
        args.port = read_cnf().get('port')
        args.mode = read_cnf().get('mode')

    if not args.pidfile:
        args.pidfile = '/tmp/MingDao.pid'

    mingdaoproxy = wyDaemon(
        pidfile=args.pidfile,
        proxy_port=args.port,
        proxy_mode=args.mode)

    if args.daemon:
        save_cnf(args)
        mingdaoproxy.start()
    elif args.stop:
        mingdaoproxy.stop()
    elif args.restart:
        mingdaoproxy.restart()
    else:
        mingdaoproxy.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="MingDao v 1.0 ( Proxying And Recording HTTP/HTTPs and Socks5)")
    parser.add_argument("-d", "--daemon", action="store_true",
                        help="start MingDao with daemond")
    parser.add_argument("-stop", "--stop", action="store_true", required=False,
                        help="stop MingDao daemond")
    parser.add_argument("-restart", "--restart", action="store_true", required=False,
                        help="restart MingDao daemond")
    parser.add_argument("-pid", "--pidfile", metavar="",
                        help="MingDao daemond pidfile name")
    parser.add_argument("-p", "--port", metavar="", default="62000",
                        help="MingDao bind port")
    parser.add_argument("-m", "--mode", metavar="", choices=['http', 'socks5', 'transparent'], default="http",
                        help="MingDao mode (HTTP/HTTPS, Socks5, Transparent)")
    args = parser.parse_args()

    try:
        run(args)
    except KeyboardInterrupt:
        logging.info("Ctrl C - Stopping Client")
        sys.exit(1)
