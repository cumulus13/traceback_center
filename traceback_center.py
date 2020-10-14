#!/usr/bin/env python
# -*- encoding: iso-8859-1 -*-

"""
Python traceback center client.

This code is placed in the public domain by the author.
Written by LD Hadi Cahyadi <cumulus13@gmail.com>

Note that if you intend to send messages to traceback center server, you must import traceback_center before
"""

from __future__ import print_function
import sys
import os
import traceback
import datetime
import re
import cmdw
import sqlalchemy
import inspect
if sys.platform == 'win32':
    import win32gui
try:
    from .xnotify import notify
except:
    from xnotify import notify
try:
    from . import ssyslog
except:
    import ssyslog
try:
    from make_colors import make_colors
except:
    def make_colors(text, fore = None, back = None, attr = None):
        return text
try:
    from configset import configset
except:
    print(make_colors("Please install configset before (pip) !", 'lw', 'lr', ['blink']))
    sys.exit()
    
SQLALCHEMY = False
PSYCOPG2 = False
try:
    import sqlalchemy
    SQLALCHEMY = True
    from sqlalchemy import create_engine, Column, Integer, String, Sequence
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
except:
    pass

try:
    import psycopg2
    PSYCOPG2 = True
except:
    pass

class TracebackCenter(object):

    LAST_TRACEBACK = None
    LAST_VALUE = None
    LAST_TYPE = None

    CONFIG_NAME = os.path.join(os.path.dirname(__file__), 'traceback.ini')
    CONFIG = configset(CONFIG_NAME)
    MESSAGES_MEM = []
    PRIVATE_SERVER = CONFIG.get_config('debug', 'private_server', 'True')
    TRACEBACK_GROWL = CONFIG.get_config('growl', 'active', 'False')
    TRACEBACK_SYSLOG = CONFIG.get_config('syslog', 'active', 'False')
    DEBUG_SERVER = CONFIG.get_config_as_list('debug', 'server', '127.0.0.1:50000')
    GROWL_HOST = CONFIG.get_config_as_list('growl', 'server', '127.0.0.1')
    SYSLOG_HOST = CONFIG.get_config_as_list('syslog', 'server', '127.0.0.1:514 192.168.43.2:514')
    SYSLOG_PORT = CONFIG.get_config_as_list('syslog', 'port', '514 517')
    GROWL_PORT = CONFIG.get_config_as_list('growl', 'port', '23053')
    HANDLE = None
    if sys.platform == 'win32':
        handle = win32gui.GetForegroundWindow()
        HANDLE = handle

    NOTIFY_ACTIVE = CONFIG.get_config('xnotify', 'active', '1')
    NOTIFY_TITLE = CONFIG.get_config('xnotify', 'title', 'traceback')
    NOTIFY_APP = CONFIG.get_config('xnotify', 'app', 'traceback')
    NOTIFY_EVENT = CONFIG.get_config('xnotify', 'event', 'log')
    NOTIFY_HOST = CONFIG.get_config('xnotify', 'host', " ".join(GROWL_HOST)) 
    NOTIFY_PORT = CONFIG.get_config('xnotify', 'port', str(GROWL_PORT)[1:-1])
    NOTIFY_TIMEOUT = CONFIG.get_config('xnotify', 'timeout', '1')
    NOTIFY_ICON = CONFIG.get_config('xnotify', 'icon'), 
    NOTIFY_ACTIVE_PUSHBULLET = CONFIG.get_config('xnotify', 'pushbullet', 'True')
    NOTIFY_ACTIVE_GROWL = CONFIG.get_config('xnotify', 'growl', TRACEBACK_GROWL)
    NOTIFY_ACTIVE_NMD = CONFIG.get_config('xnotify', 'nmd', 'true')
    NOTIFY_PUSHBULLET_API = CONFIG.get_config('xnotify', 'pushbullet_api')
    NOTIFY_NMD_API = CONFIG.get_config('xnotify', 'nmd_api')
    
    NOTIFY = notify(NOTIFY_TITLE, NOTIFY_APP, NOTIFY_EVENT, None, NOTIFY_HOST, NOTIFY_PORT, NOTIFY_TIMEOUT, NOTIFY_ICON, NOTIFY_ACTIVE_PUSHBULLET, NOTIFY_ACTIVE_GROWL, NOTIFY_ACTIVE_NMD, NOTIFY_PUSHBULLET_API, NOTIFY_NMD_API)
    
    DATABASE_TYPE = CONFIG.get_config('database', 'type', 'postgres')
    DATABASE_USER = CONFIG.get_config('database', 'username', 'traceback')
    DATABASE_PASS = CONFIG.get_config('database', 'password', '12345678')
    DATABASE_NAME = CONFIG.get_config('database', 'name', 'traceback')
    DATABASE_HOST = CONFIG.get_config('database', 'host', '127.0.0.1')
    DATABASE_PORT = CONFIG.get_config('database', 'port', '5432')
    
    def __init__(self):
        super(TracebackCenter, self)

    @classmethod
    def supports_color(cls):
        plat = sys.platform
        supported_platform = plat != 'Pocket PC' and (plat != 'win32' or 'ANSICON' in os.environ)
        # isatty is not always implemented, #6223.  
        is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
        return supported_platform and is_a_tty

    @classmethod
    def send_messages_mem(cls):
        if cls.MESSAGES_MEM:
            for i in cls.MESSAGES_MEM:
                # send
                cls.MESSAGES_MEM.remove(i)
            

    @classmethod
    def get_traceback(cls, exctype = None, value = None, tb = None):
        cls.ver_config()
        if exctype:
            cls.LAST_TYPE = exctype
        if value:
            cls.LAST_VALUE = value
        if tb:
            cls.LAST_TRACEBACK = tb
        else:
            if hasattr(sys, 'last_traceback'):
                cls.LAST_TRACEBACK = sys.last_traceback
            elif hasattr(sys, 'exc_traceback'):
                cls.LAST_TRACEBACK = sys.exc_traceback

            if hasattr(sys, 'last_value'):
                cls.LAST_VALUE = sys.last_value
            elif hasattr(sys, 'exc_value'):
                cls.LAST_VALUE = sys.exc_value

            if hasattr(sys, 'last_type'):
                cls.LAST_TYPE = sys.last_type
            elif hasattr(sys, 'exc_type'):
                cls.LAST_TYPE = sys.exc_type

        if cls.LAST_TRACEBACK:
            # print("cls.LAST_TRACEBACK =", cls.LAST_TRACEBACK)
            # print("cls.LAST_VALUE     =", cls.LAST_VALUE)
            # print("cls.LAST_TYPE      =", cls.LAST_TYPE)

            tblist = traceback.extract_tb(cls.LAST_TRACEBACK)[:1]
            tblist = traceback.format_list(tblist)
            tblist_color = []
            for i in tblist:
                if sys.platform == 'win32':
                    tblist_color.append(make_colors(i.split("\n")[0], 'lw', 'bl') + "\n")
                else:
                    tblist_color.append(make_colors(i.split("\n")[0], 'b', 'ly') + "\n")

            tblist.insert(0, "Traceback (most recent call last):\n")
            tblist_color.insert(0, make_colors("Traceback (most recent call last):", 'lr', 'lw') + "\n")
            tbadd = traceback.format_exception_only(cls.LAST_TYPE, cls.LAST_VALUE)
            tbadd_colors = []
            for i in tblist:
                tbadd_colors.append(make_colors(i.split("\n")[0], 'lw', 'lr') + "\n")

            tblist += tbadd
            tblist_color.append(make_colors("".join(tbadd)[:-1], 'lw', 'lr'))

            if cls.NOTIFY_ACTIVE or cls.CONFIG.get_config('xnotify', 'active'):
                cls.NOTIFY.notify("Traceback", "".join(tblist))
            if cls.TRACEBACK_SYSLOG or cls.CONFIG.get_config('syslog', 'active'):
                cls.sent_to_syslog("".join(tblist), "error", 'user')
            print("".join(tblist_color))
            cls.send_to_db(tblist)
            if cls.supports_color():
                return "".join(tblist_color)
            return tblist

        return ''

    def __str__(self):
        return "".join(TracebackCenter.get_traceback())

    def __repr__(self):
        return "".join(TracebackCenter.get_traceback())

    @classmethod
    def ver_config(cls):
        '''
        	Get config from os environment
        '''
        if os.getenv('PRIVATE_SERVER'):
            cls.PRIVATE_SERVER = os.getenv('PRIVATE_SERVER')
        if cls.PRIVATE_SERVER == '1' or cls.PRIVATE_SERVER == 1:
            cls.PRIVATE_SERVER = True
        if cls.PRIVATE_SERVER == "True" or cls.PRIVATE_SERVER == True:
            cls.PRIVATE_SERVER = True

        if os.getenv('TRACEBACK_GROWL'):
            if os.getenv('TRACEBACK_GROWL') == '1' or os.getenv('TRACEBACK_GROWL') == 'True':
                cls.TRACEBACK_GROWL = True

        if os.getenv('TRACEBACK_GROWL_SERVER'):    
            cls.GROWL_HOST = []
            for i in str(os.getenv("TRACEBACK_GROWL_SERVER")).split(";"):
                cls.GROWL_HOST.append(str(i).strip())

        if os.getenv('TRACEBACK_SYSLOG'):
            if os.getenv('TRACEBACK_SYSLOG') == '1' or os.getenv('TRACEBACK_SYSLOG') == 'True':
                cls.TRACEBACK_SYSLOG = True
        if os.getenv('TRACEBACK_SYSLOG_SERVER'):
            cls.SYSLOG_HOST = []
            for i in str(os.getenv('TRACEBACK_SYSLOG_SERVER')).split(";"):
                cls.SYSLOG_HOST.append(str(i).strip())

        if os.getenv('TRACEBACK_DEBUGGER_SERVER'):
            cls.DEBUG_SERVER = re.split(";|,", os.getenv('TRACEBACK_DEBUGGER_SERVER'))

    @classmethod
    def sent_to_syslog(cls, message, severity=None, facility=None, host = None, port=514):

        if severity == None:
            severity = 3
        if facility == None:
            facility = 3
        if host:
            cls.SYSLOG_HOST = host
        if port:
            cls.SYSLOG_PORT = port
        if isinstance(cls.SYSLOG_HOST, list):
            for i in cls.SYSLOG_HOST:
                if ":" in i:
                    HOST, PORT = str(i).split(":")
                    HOST = HOST.strip()
                    PORT = str(PORT).strip()
                    if not PORT:
                        PORT = 514
                    #print "sent to %s:%s" % (HOST, str(PORT))
                    ssyslog.syslog(message, severity, facility, HOST, int(PORT))
                else:
                    if len(cls.SYSLOG_PORT) == len(cls.SYSLOG_HOST):
                        ssyslog.syslog(message, severity, facility, i, int(cls.SYSLOG_PORT[cls.SYSLOG_HOST.index(i)]))
                    else:
                        if len(cls.SYSLOG_PORT) == 1:
                            ssyslog.syslog(message, severity, facility, i, int(cls.SYSLOG_PORT[0]))
                        else:
                            if not port:
                                port = 514
                            #print "host i =", i
                            #print "port   =", port
                            ssyslog.syslog(message, severity, facility, i, port)
        else:
            #print "SYSLOG_HOST 1:", SYSLOG_HOST
            if isinstance(cls.SYSLOG_PORT, list):
                for i in cls.SYSLOG_PORT:
                    ssyslog.syslog(message, severity, facility, cls.SYSLOG_HOST, int(i))
            else:
                ssyslog.syslog(message, severity, facility, cls.SYSLOG_HOST, cls.SYSLOG_PORT)

    @classmethod
    def writelog(cls, msg):
        timelog = datetime.datetime.strftime(datetime.datetime.now(), '%Y:%m:%d %H:%M:%S:%f')
        if not os.path.isfile(os.path.join(os.getcwd(), 'traceback.log')):
            with open(os.path.join(os.getcwd(), 'traceback.log'), 'wb') as log:
                log.write(timelog + " ~ " + msg + "\n")
            log.close()
        else:
            with open(os.path.join(os.getcwd(), 'traceback.log'), 'a') as log:
                log.write(timelog + " ~ " + msg + "\n")
            log.close()

    @classmethod
    def showme():
        if sys.platform == 'win32':
            import win32gui, win32con
            #print("HANDLE 0:", HANDLE)
            #win32gui.MessageBox(None, str(HANDLE), str(HANDLE), 0)
            handle = HANDLE
            if not handle:
                handle = win32gui.GetForegroundWindow()
            #handle1 = handle = win32gui.GetForegroundWindow()
            #print("HANDLE 1:", handle)
            win32gui.ShowWindow(handle, win32con.SW_RESTORE)
            #win32gui.SetWindowPos(handle, win32con.HWND_TOPMOST, 0, 0, 0, 0, 0)
            win32gui.SetForegroundWindow(handle)
            win32gui.BringWindowToTop(handle)
            #win32gui.SetForegroundWindow(handle)

            #win32gui.ShowWindow(handle1,9)
            #win32gui.SetForegroundWindow(handle1)
            #win32gui.SetWindowPos(handle, win32con.HWND_TOPMOST, None, None, None, None, 0)

    @classmethod
    def serve(cls,  host = '0.0.0.0', port = 50000, detach = True, width = 500, height = 500, x = 0, y = 0, center = False, buffer_column = 9000, buffer_row = 77, on_top = True):
        if detach and sys.platform == 'win32':
            from dcmd import dcmd
            setting = dcmd.dcmd()
            setting.setBuffer(buffer_row, buffer_column)
            screensize = setting.getScreenSize()
            x = screensize[0] - width
            setting.setSize(width, height, x, 50, center)
            if on_top:
                setting.setAlwaysOnTop(width, height, x, y, center)

        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.bind((host, int(port)))
            print(make_colors("BIND: ", 'white', 'green') + make_colors(host, 'white', 'red', attrs= ['bold']) + ":" + make_colors(str(port), 'white', 'yellow', attrs= ['bold']) + " " + make_colors("PID:", 'b', 'ly') + make_colors(str(
                os.getpid()), 'lw', 'm'))
            print("\n")
            while 1:
                MAX_WIDTH = cmdw.getWidth()
                msg, addr = s.recvfrom(65565)
                #msg = s.recv(65565)
                if msg:
                    if msg and msg == 'show':
                        #print(msg)
                        cls.showme()
                    else:
                        print(msg)
                        print("=" * (MAX_WIDTH - 1))
                else:
                    s.sendto('alive', addr)
        except:
            print(make_colors("Server has running !", 'lightwhite', 'lightred', ['blink']))
            
    @classmethod
    def send_to_db(cls, data, database_type = None, database_user = None, database_pass = None, database_name = None, database_host = None, database_port = None):
        if database_type:
            cls.DATABASE_TYPE = database_type
        if database_user:
            cls.DATABASE_USER = database_user
        if database_pass:
            cls.DATABASE_PASS = database_pass
        if database_name:
            cls.DATABASE_NAME = database_name
        if database_host:
            cls.DATABASE_HOST = database_host
        if database_port:
            cls.DATABASE_PORT = database_port
        global SQLALCHEMY
        if SQLALCHEMY:
            database_string_conn = "{}://{}:{}@{}:{}/{}".format(cls.DATABASE_TYPE, cls.DATABASE_USER, cls.DATABASE_PASS, cls.DATABASE_HOST, cls.DATABASE_PORT, cls.DATABASE_NAME)
            
            db = sqlalchemy.create_engine(database_string_conn)            
            base = declarative_base()
            
            class DB(base):
                __tablename__ = 'traceback'
                
                
                id = Column(Integer, Sequence('trackeback_id_seq'), primary_key = True)
                date = Column(String)
                host = Column(String)
                app = Column(String)
                tb = Column(String)
                tp = Column(String)
                vl = Column(String)
            
            if not cls.CONFIG.get_config('database', 'first'):
                base.metadata.create_all(db)
                cls.CONFIG.write_config('database', 'first', '1')
            
            Session = sessionmaker(db)
            session = Session()
            app = inspect.stack()[1][1]
            insert = DB(date = datetime.datetime.strftime(datetime.datetime.now(), '%Y/%m/%d %H:%M:%S:%f'), host = '127.0.0.1', app = app, tb = data[0], tp = data[1], vl = data[2])
            session.add(insert)
            session.commit()
            
        

    @classmethod	        
    def usage(cls):
        import argparse
        parser = argparse.ArgumentParser(description= 'run traceback as server receive debug text default port is 50000', version= "1.0", formatter_class= argparse.RawTextHelpFormatter)
        parser.add_argument('-b', '--host', action = 'store', help = 'Bind / listen ip address, default all network device: 0.0.0.0', default = '0.0.0.0', type = str)
        parser.add_argument('-p', '--port', action = 'store', help = 'Bind / listen port number, default is 50000', default = 50000, type = int)
        parser.add_argument('-d', '--detach', action = 'store_true', help = 'run standalone process server')
        parser.add_argument('-x', '--xpos', action = 'store', help = 'X positon', default = 0 ,type = int)
        parser.add_argument('-y', '--ypos', action = 'store', help = 'Y positon', default = 50 ,type = int)
        parser.add_argument('-W', '--width', action = 'store', help = 'Windows width', default = 500 ,type = int)
        parser.add_argument('-H', '--height', action = 'store', help = 'Windows height', default = 500 ,type = int)
        parser.add_argument('-c', '--center', action = 'store_true', help = 'Centering window')
        parser.add_argument('-bc', '--buffer-column', action = 'store', help = 'Number of columns buffer', default = 9000 ,type = int)
        parser.add_argument('-br', '--buffer-row', action = 'store', help = 'Number of rows buffer', default = 77 ,type = int)
        parser.add_argument('-a', '--always-top', action = 'store_true', help = 'Always On Top')

        #serve(host = '0.0.0.0', port = 50000, detach = True, width = 500, height = 500, x = 0, y = 0, center = False, buffer_column = 9000, buffer_row = 77, on_top = True):
        if len(sys.argv) == 1:
            print("\n")
            parser.print_help()

        try:
            args = parser.parse_args()
            cls.serve(args.host, args.port, args.detach, args.width, args.height, args.xpos, args.ypos, args.center, args.buffer_column, args.buffer_row, args.always_top)
        except KeyboardInterrupt:
            sys.exit()


if __name__ == '__main__':
    TracebackCenter.usage()