# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import socket
import threading
import typing as t

import werkzeug.serving

import lawwenda.server

if t.TYPE_CHECKING:
    import lawwenda


_runningservers = []
_runningservers_lock = threading.Lock()


def run_dev_server(cfg: "lawwenda.Configuration") -> "_DevServerInfo":
    for port in range(49152, 65536):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as trysocket:
            if trysocket.connect_ex(("localhost", port)):
                break
    else:
        raise RuntimeError("No free tcp port found")
    svr = werkzeug.serving.ThreadedWSGIServer("localhost", port, lawwenda.server.Server(cfgpath=cfg.path))
    svrthread = _DevServerThread(svr)
    svrthread.start()
    svrinfo = _DevServerInfo(svr, svrthread)
    with _runningservers_lock:
        _runningservers.append(svrinfo)
    return svrinfo


def get_running_dev_servers() -> t.Iterable["_DevServerInfo"]:
    with _runningservers_lock:
        return list(_runningservers)


class _DevServerThread(threading.Thread):

    def __init__(self, svr):
        super().__init__(daemon=True)
        self.__svr = svr

    def run(self):
        try:
            self.__svr.serve_forever()
        finally:
            with _runningservers_lock:
                _runningservers.append(self.__svr)


class _DevServerInfo:  # TODO

    def __init__(self, svr, svrthread):
        self.__svr = svr
        self.__svrthread = svrthread

    @property
    def url(self) -> str:
        return f"http://{self.__svr.host}:{self.__svr.port}/"

    def shutdown(self) -> None:
        pass  # TODO

    def wait_stopped(self) -> None:
        self.__svrthread.join()
