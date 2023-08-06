"""
Copyright 2021-2021 The jdh99 Authors. All rights reserved.
申请父路由
Authors: jdh99 <jdh821@163.com>
"""

import tziot.config as config
import tziot.standardlayer as standardlayer
import tziot.fpipe as fpipe
import tziot.fdcom as fdcom

import dcompy as dcom
import lagan
import utzpy as utz
import knocky as knock
import socket
import threading
import time


class ParentInfo:
    """父路由信息"""

    def __init__(self):
        self.ia = 0
        self.pipe = 0
        self.cost = 0
        self.is_conn = False
        self.timestamp = 0


parent = ParentInfo()


def init():
    knock.register(utz.HEADER_CMP, utz.CMP_MSG_TYPE_ASSIGN_SLAVE_ROUTER, deal_assign_slave_router)
    threading.Thread(target=_apply_thread).start()


def deal_assign_slave_router(req: bytearray, *args) -> (bytearray, bool):
    """处理分配从机帧.返回值是应答数据和应答标志.应答标志为false表示不需要应答"""
    global parent

    if len(req) == 0:
        lagan.warn(config.TAG, "deal apply failed.payload len is wrong:%d", len(req))
        return None, False

    j = 0
    if req[j] != 0:
        lagan.warn(config.TAG, "deal apply failed.error code:%d", req[j])
        return None, False
    j += 1

    if len(req) != 16:
        lagan.warn(config.TAG, "deal apply failed.payload len is wrong:%d", len(req))
        return None, False

    parent.ia = utz.bytes_to_ia(req[j:j + utz.IA_LEN])
    j += utz.IA_LEN

    ip = socket.inet_ntoa(req[j:j + 4])
    j += 4
    port = (req[j] << 8) + req[j + 1]
    j += 2
    parent.pipe = dcom.addr_to_pipe(ip, port)

    lagan.info(config.TAG, "apply success.parent ia:0x%x ip:%s port:%d cost:%d", parent.ia, ip, port, req[j])
    return None, False


def _apply_thread():
    while True:
        # 如果网络通道不开启则无需申请
        if not fpipe.pipe_is_allow_send(fpipe.PIPE_NET):
            time.sleep(1)
            continue

        if fdcom.is_dcom_init and parent.ia == utz.IA_INVALID:
            lagan.info(config.TAG, "send apply frame")
            _send_apply_frame()

        if fdcom.is_dcom_init:
            time.sleep(10)
        else:
            time.sleep(1)


def _send_apply_frame():
    security_header = utz.SimpleSecurityHeader()
    security_header.next_head = utz.HEADER_CMP
    security_header.pwd = config.local_pwd
    payload = utz.simple_security_header_to_bytes(security_header)

    body = bytearray()
    body.append(utz.CMP_MSG_TYPE_REQUEST_SLAVE_ROUTER)
    body += utz.ia_to_bytes(parent.ia)
    body = utz.bytes_to_flp_frame(body, True, 0)

    payload += body

    header = utz.StandardHeader()
    header.version = utz.PROTOCOL_VERSION
    header.frame_index = utz.generate_frame_index()
    header.payload_len = len(payload)
    header.next_head = utz.HEADER_SIMPLE_SECURITY
    header.hops_limit = 0xff
    header.src_ia = config.local_ia
    header.dst_ia = config.core_ia

    standardlayer.send(payload, header, config.core_pipe)
