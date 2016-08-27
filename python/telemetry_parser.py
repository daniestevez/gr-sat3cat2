#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This is free and unencumbered software released into the public domain.
# 
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
# 
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
# 
# For more information, please refer to <http://unlicense.org>
# 

import numpy
from gnuradio import gr
import pmt

class telemetry_parser(gr.basic_block):
    """
    docstring for block telemetry_parser
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="telemetry_parser",
            in_sig=[],
            out_sig=[])

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print "[ERROR] Received invalid message type. Expected u8vector"
            return
        packet = str(bytearray(pmt.u8vector_elements(msg)))

        try:
            data = packet[17:].split()
        
            status = {'1' : 'Survival', '2' : 'Sun-safe', '3' : 'Nominal',\
                    '4' : 'TX', '5' : 'RX', '6' : 'Payload', '7' : 'Payload' }
            adcs = {'0' : 'auto', '1' : 'manual'}
            if data[5] == '0':
                detumbling = 'Detumbling  ({},{},{})nT'.format(float(data[7]), float(data[8]), float(data[9]))
            else:
                detumbling = 'SS-nominal  Sun: ({:.2f},{:.2f},{:.2f})'.format(float(data[7]), float(data[8]), float(data[9]))
            string = status[data[0]] + '  {:.2f}V  {}mA'.format(int(data[1])/1000.0, int(data[2])) + \
            '  EPS: {}ºC   Ant: {}ºC'.format(data[3], data[4]) + \
            '  ADCS ' + adcs[data[6]] + '  ' + detumbling + \
            '  Control: ({:.1e},{:.1e},{:.1e})V'.format(float(data[10]), float(data[11]), float(data[12]))

            print(string)
        except IndexError, ValueError:
            print "Malformed beacon:"
            print packet[17:]
