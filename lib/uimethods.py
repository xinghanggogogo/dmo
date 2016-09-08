#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import xtea3
import base64
import qrcode
import hashlib

from decimal import Decimal
from datetime import datetime, date
from settings import OrderActionString

def datetime_str(handler, time_obj):
    return time_obj.strftime('%Y-%m-%d %H:%M:%S')

def json_format(handler, res):

    def _format(obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(obj, Decimal):
            return ('%.2f' % obj)
        if isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')

    return json.dumps(res, default=_format)

def order_action_to_text(handler, action):
    return OrderActionString.get(action, '不详')

def trim(handler, val, length, ellipsis='...', ret='before'):
    if val:
        if len(val) < length + 2:
            return val
        else:
            ellipsis = ellipsis if len(val) > length and ellipsis else ''
            split_str = val[:length] if ret == 'before' else val[length:]
            return split_str + ellipsis
    else:
        return ''

def qrcode_img(handler, mobile, ktv_id):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=8,
        border=0
    )
    data = {
        'mobile': mobile,
        'ktv_id': ktv_id
    }
    crypt = xtea3.new(b' ' * 16, mode=xtea3.MODE_OFB, IV=b'12345678')
    info = base64.urlsafe_b64encode(crypt.encrypt(str(data).encode())).decode()
    qr.add_data('http://erp.ktvsky.com?info=%s' % info)
    qr.make(fit=True)
    img = qr.make_image(image_factory=None, fill_color='transparent')

    filename = hashlib.md5(str(data).encode()).hexdigest() + '.jpg'
    filepath = handler.settings['static_path'] + '/data/' + filename

    if not os.path.exists(filepath):
        img.save(filepath, format='PNG')

    return handler.static_url('data/' + filename)

