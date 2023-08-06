# 0.1.2a
##################################################################################
#   MIT License
#
#   Copyright (c) [2021] [René Horn]
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to deal
#   in the Software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in all
#   copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#   SOFTWARE.
###################################################################################
import concurrent
import configparser
import http
import io
import json
import os
import queue
import random
import signal
import sys
import threading
from concurrent.futures._base import as_completed
from time import sleep, strftime, time
from concurrent.futures import ThreadPoolExecutor, wait
import urllib.request
import urllib.parse
from urllib.error import URLError, HTTPError
import urllib3
##############
import getpass
import shutil
import stat
import urllib.parse
import http.server
import socketserver

import logging

# logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s',)
# logging.basicConfig(level=logging.INFO, format='[%(levelname)s] (%(threadName)-10s) %(message)s',)

# Could anyone please explain ... what it does?
# Well, this SCRIPT reads the data stream from a radio station into separate files.
# The data stream is SPLIT INTO PIECES, mostly "ARTIST - Title.MP3" style. Plus ".m3u" and ".pls" play list support.
# 'This' world is tumbling down. Record it with     !!! Ghetto RECORDER !!!
# Be brave, be curious!                                 rene_horn@gmx.net


# Usage:
# Runs on Python 3.5: R E A D --> (Windows 'pip'/Linux 'pip3, python3')
# Go to the next free internet WLAN.
# Windows Store/Linux package manager, install latest Python3 version.
# 'pip install ghettorecorder' - with a normal user account!
# 'pip show ghettorecorder' to find the install Location: site-packages/ghettorecorder /
# 'python - m ghettorecorder.run' will run the recorder from anywhere on your computer.
# GhettoRecorder is uninstalled by 'pip uninstall gettorecorder'. Recorded mp3 files not.
#  Copy 'run.py' and 'settings.ini' files wherever you want to have your record repository.
#  Windows let's you double click 'run.py'. Can run from desktop.
# Magic number 42 is used to connect to all radios found in 'settings.ini'.

print('0.7.1 now a real Ghetto Blaster with radio')  # ###################### version ##################################

# - added radio, http server redirects to local port
# - fixed copy file with wrong name
# - fixed printing match search every time

proxy_support = urllib.request.ProxyHandler({})
opener = urllib.request.build_opener(proxy_support)
urllib.request.install_opener(opener)

os.chdir(os.path.dirname(os.path.abspath(__file__)))  # go to .py script folder
username = getpass.getuser()
# print(username)
exit_app = False
urllib3.disable_warnings()


# print(sys.version)


def switch_dst_dir(container):  # if app runs in a container

    global username
    print('Hello, ' + username)
    if container == 'SNAP':
        ghetto_folder = '//home//' + username + '//GhettoRecorder'
    else:
        ghetto_folder = '//tmp//GhettoRecorder'  # DOCKER

    # set new radio_base_dir class attribute
    GBase.radio_base_dir = ghetto_folder

    source_ini = os.path.dirname(os.path.abspath(__file__)) + '//settings.ini'
    dst_ini = ghetto_folder + '//settings.ini'

    access_rights = 0o755
    try:
        os.mkdir(ghetto_folder, access_rights)
    except FileExistsError:
        pass

    try:
        if not os.path.exists(dst_ini):
            shutil.copyfile(source_ini, dst_ini)
    except FileExistsError:
        pass


def signal_handler(sig, frame):
    global exit_app
    print(' Signal stop recording ...')
    exit_app = True
    GBase.exit_app = True
    # sleep(3)  # give thread def: time for clean exit -
    sys.exit()


class GBase:
    # class attribute
    exit_app = False
    sleeper = 2  # for exit of all threads
    pool = ThreadPoolExecutor(200)
    radio_base_dir = os.path.dirname(os.path.abspath(__file__)) + '//radiostations'  # if not set set_radio_base_dir()
    settings_path = os.path.dirname(os.path.abspath(__file__)) + '//settings.ini'  # if not set in set_settings_path()
    path = os.getcwd()
    path_to = path + '//'
    timer = 0

    def __init__(self, radio_base_dir=None, settings_path=None):
        self.instance_attr_time = 0
        self.trigger = False
        self.radio_base_dir = radio_base_dir
        self.settings_path = settings_path

    @staticmethod
    def make_directory(str_path):
        access_rights = 0o755
        try:
            os.mkdir(str_path, access_rights)
        except FileExistsError:
            pass
            # print(' Folder exists: ' + str_path)
            return False
        else:
            print('Successfully created the directory: ' + str_path)
            return True

    @staticmethod
    def remove_special_chars(str_name):
        # cleanup for writing files and folders

        # my_str = "hey th~!ere. /\ coolleagues?! Straße"
        ret_value = str_name.translate({ord(string): "" for string in '"!@#$%^*()[]{};:,./<>?\|`~=+"""'})
        return ret_value

    @staticmethod
    def this_time():
        time = strftime("%Y-%m-%d %H:%M:%S")
        return time

    def countdown(self, instance_attr_time):
        t = 0
        while not t == instance_attr_time:
            sleep(1)
            self.timer = t
            print(self.timer)
            t += 1
            if t == 0:
                self.trigger = True
        print(f' done {instance_attr_time} {self.trigger}')
        return self.trigger


class GIni(GBase):
    ini_keys = {}  # cls attribute to store selections from ini file, works because of key[key] = value, else not
    srv_param_dict = {}  # all ini keys plus short url, suffix, server type stuff
    start_stop_recording = {}  # ini key: 'start' , 'stop'; while loop check start, working check stop go upper while
    # ini_key + '_single_title', ini_key + '_rec_from_here'
    cost_current_ini = ''  # ini key for cost_dict calc / should be a dict
    cost_dict = {}  # stores len of received headers to calc amount of data searching strings per day
    fail_meta_dict = {}  # can not read metadata from stream, no data
    # list of search strings delimiter blank, first key is named 'STRINGS': Britney Phantom ไม่เคยจะจำ Elton Jim techno
    search_dict = {'STRINGS': 'Britney Spears ไม่เคยจะจำ Elton AC/DC techno Band feat. mix'}  # only show it is working
    list_items = []
    search_title_keys_list = []  # radio short keys, not start recording all streams, only searched titles
    content_type = {}  # header info audio/mpeg

    def __init__(self):
        super().__init__()

    @staticmethod
    def show_items_ini_file():

        config = configparser.ConfigParser()  # imported library to wok with .ini files
        try:
            config.read_file(open(GBase.settings_path))
        except FileNotFoundError as ex:
            print(ex)
            sys.exit()
        else:

            i = 0

            print('\t  _______       __  __       ___                      __       ')
            print('\t / ___/ /  ___ / /_/ /____  / _ \___ _______  _______/ /__ ____')
            print('\t/ (_ / _ \/ -_) __/ __/ _ \/ , _/ -_) __/ _ \/ __/ _  / -_) __/')
            print('\t\___/_//_/\__/\__/\__/\___/_/|_|\__/\__/\___/_/  \_,_/\__/_/   ')
            print('                                                       Elvis lebt')
            for _ in dict(config.items('STATIONS')):
                GIni.list_items.append(_)
            for _ in GIni.list_items:
                print('\t>> %-20s <<' % _)

            print(' \n Radio stations in your list. ')
            print(' Please use "Ctrl + C" to stop. ')
        return

    @staticmethod
    def find_ini_file(key_name):
        config = configparser.ConfigParser()  # imported library to work with .ini files
        try:
            config.read_file(open(GBase.settings_path))
        except FileNotFoundError as ex:
            print(ex)
            sys.exit()
        else:

            station_value = 'False'  # init var for return value
            stations = config['STATIONS']

            try:
                station_value = stations[key_name]  # if all ok get a valid string of value -> True
            except KeyError as ex:
                print(ex)
                print(' ??? radio station, input was ->>> ' + key_name)

        return station_value  # single value

    @staticmethod
    def find_all_in_stations():

        config = configparser.ConfigParser()  # imported library to work with .ini files
        try:
            config.read_file(open(GBase.settings_path))
        except FileNotFoundError as ex:
            print(ex)
            sys.exit()
        else:
            stations = config['STATIONS']

        return stations  # list of values

    @staticmethod
    def parse_url_simple_url(radio_url):
        url = radio_url  # whole url is used for connection to radio server

        # 'http:' is first [0], 'ip:port/xxx/yyy' second item [1] in list_url_protocol
        list_url_protocol = url.split("//")
        list_url_ip_port = list_url_protocol[1].split("/")  # 'ip:port' is first item in list_url_ip_port
        radio_simple_url = list_url_protocol[0] + '//' + list_url_ip_port[0]
        return radio_simple_url


class GNet(GBase):
    is_shout_dict = {}
    is_ice_dict = {}
    is_ice_json_dict = {}
    is_unk_dict = {}
    is_no_meta_avail_dict = {}

    http_pool = urllib3.PoolManager(num_pools=200)
    request = ''
    user_agent = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko)'
                                ' Chrome/24.0.1312.27 Safari/537.17'}

    ctm_usr_agent = {'Icy-MetaData': '1', 'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                                                        "(KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36"}
    query_shoutcast = '/currentsong'

    def __init__(self):
        super().__init__()

    @staticmethod
    def load_url(url):
        # returns status code, if server is alive conn.getcode()
        # use urllib, urllib3 causes response to wait "forever" and timeout is not working either
        # print(f' load_url {url}')
        with urllib.request.urlopen(url, timeout=15) as response:
            return response.getcode()

    @staticmethod
    def is_server_alive(url, key):
        # don't delete - urllib3 timeout=5, placebo, retries=None or =2, screw yourself, since half of conn. die
        # we have here server up, but content not presented - zombie, requests are blocking calls, so start thread

        # use with statement, ensure threads are cleaned up promptly
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_url = executor.submit(GNet.load_url, url)

        try:
            status = future_to_url.result()
        except HTTPError:  # lots of strange configured web server
            # print(error)
            return True
        except URLError as error:  # <urlopen error timed out>
            del GIni.ini_keys[key]
            print(f' ---> {key} server failed: {error} (no recording) {url}')
            return False
        return True

    @staticmethod
    def connect_url(request, url, key, action):
        try:
            with urllib.request.urlopen(request) as response:
                if action == 'getcode':
                    response_content = response.getcode()
                if action == 'read':
                    response_content = response.read()
                if action == 'info':
                    response_content = response.info()
        except HTTPError:
            pass
        except URLError as error:
            print(f' ---> {key} server timeout: {error} {url}')
            return False

        return response_content

    @staticmethod
    def playlist_server(url):
        # not only string manipulation here, read from url
        play_list_server = ''
        if url[-5:] == '.m3u8' or url[-5:] == '.xspf':
            print(' .m3u8/.xspf play lists not yet supported')
            sys.exit()

        if url[-4:] == '.m3u' or url[-4:] == '.pls':  # or url[-5:] == '.m3u8' or url[-5:] == '.xspf':

            with urllib.request.urlopen(url, timeout=15) as response:
                html = response.read().decode('utf-8')

            print(' \n        --- | ---')
            # decode errors in malformed playlists
            try:
                print(html)
            except Exception as ex:
                print(ex)
            else:
                pass
            print(" \n        --- | ---")
            try:
                play_list_server = input('copy and paste a server from above, here ->: ')
            except Exception as ex:
                print(ex)
                print(' exception: input error ')
                return False
        else:
            return False

        return play_list_server.strip()

    @staticmethod
    def is_server_shoutcast(server_name, key):

        try:
            request = GNet.http_pool.request('GET', server_name, preload_content=False, retries=10)  # winamp
            if not request.headers['icy-notice1'].find('http://www.winamp.com') == -1:  # find() -1 fail
                GNet.is_shout_dict[key] = True
                # GIni.cost_dict[GIni.cost_current_ini] = len(request.headers)
        except KeyError:
            # print(repr(ex))
            # print(' no Shoutcast stream')
            return False
        else:
            return True

    @staticmethod
    def is_server_icecast_url(url, key):
        # caller is_shout_ice_unknown_server print(f' is server icecast  ')
        headers = GNet.user_agent
        req = urllib.request.Request(url, headers=headers)

        try:

            with urllib.request.urlopen(req) as response:
                headers = response.getheader('server').lower().find("icecast")
            if not headers == -1:  # -1 false from find()
                GNet.is_ice_dict[key] = True
                return True
            else:
                print(f' {key} server type: {headers}')
        except Exception as ex:
            pass
            # print(repr(ex))
            return False
        return True

    @staticmethod
    def is_server_icecast(server_name, key):

        try:
            request = GNet.http_pool.request('GET', server_name, preload_content=False)  # 'server'
            substr_start_num = request.headers['server'].lower().find("icecast")
            if not substr_start_num == -1:  # -1 false from find()
                GNet.is_ice_dict[key] = True
                return True
            else:
                print(f' {key} server type: {request.headers["server"]}')
        except KeyError:
            # print(repr(ex))
            # print(' Exception in is_server_icecast ')
            return False

    @staticmethod
    def ice_status_json(request):
        data_stats_source_title = False
        source = request.read()
        data = json.loads(source)

        data_stats = data.get('icestats')
        data_stats_source = data_stats.get('source')
        try:
            data_stats_source_title = data_stats_source.get('title')
        except AttributeError:
            # print(repr(e))
            data_stats_source = data_stats.get('source')
            data_stats_source_title = data_stats_source[0]['title']

        GIni.cost_dict[GIni.cost_current_ini] = len(source)
        return data_stats_source_title

    @staticmethod
    def is_server_icecast_status_json(server_name, full_url, key):

        try:
            request = GNet.http_pool.request('GET', server_name + '/status-json.xsl', preload_content=False)
            song_title = GNet.ice_status_json(request)

        except Exception as ex:
            print(ex)
            print(f' {key} got no readable json file \n will read title from data stream \n')
            return False

        return song_title

    @staticmethod
    def stream_filetype_url(url, key):
        try:
            with urllib.request.urlopen(url, timeout=15) as response:
                headers = response.getheader('Content-Type')
        except Exception as ex:
            print(ex)
            return False

        content_type = ''
        if headers == 'audio/aacp' or headers == 'application/aacp':
            content_type = '.aacp'
        if headers == 'audio/aac':
            content_type = '.aac'
        if headers == 'audio/ogg' or headers == 'application/ogg':
            content_type = '.ogg'
        if headers == 'audio/mpeg':
            content_type = '.mp3'
        if headers == 'audio/x-mpegurl' or headers == 'text/html':
            content_type = '.m3u'
        # application/x-winamp-playlist , audio/scpls , audio/x-scpls ,  audio/x-mpegurl

        try:
            GIni.content_type[key] = headers
            if len(headers) <= 5:
                GIni.content_type[key] = 'audio/mpeg'
            print(f' stream_filetype_url {GIni.content_type[key]}')
        except Exception as e:
            print(e)
            pass

        return content_type

    @staticmethod
    def is_shout_ice_unknown_server(server_port, full_url, key):
        # called from test_stream_server()
        response = GNet.is_server_alive(server_port, key)
        if not response:
            # print(f' ---> is_shout_ice_unknown_server: {key} {server_port} {full_url}')
            return False
        else:
            # got response
            GNet.is_server_shoutcast(server_port, key)
            if not GNet.is_shout_dict[key]:
                GNet.is_server_icecast_url(server_port, key)
                if GNet.is_ice_dict[key]:
                    if GNet.is_server_icecast_status_json(server_port, full_url, key):
                        # http://stream.dancewave.online:8080/retrodance.mp3/status-json.xsl full url
                        GNet.is_ice_json_dict[key] = True

            if not GNet.is_ice_json_dict[key]:
                if not GNet.is_shout_dict[key]:
                    GNet.is_unk_dict[key] = True

                    try:
                        req = GNet.http_pool.request('GET', full_url, headers={'Icy-MetaData': '1'},
                                                     preload_content=False)
                        GNet.icy_metadata = int(req.headers['icy-metaint'])
                        print(f' chunk size {GNet.icy_metadata} {key}')
                        # GIni.cost_dict[GIni.cost_current_ini] = GNet.icy_metadata
                        # chunk size, calculate request one day (title search)
                        # write in dict for no metadata = true
                    except Exception as ex:
                        print(ex)
                        print(f' ---> {key}: no html title-info, no stream metadata, must be deleted; no record')
                        GNet.is_no_meta_avail_dict[key] = True

            return True


class GRecorder:
    stream_song_name = '_no-name-record_no_split_'
    path_to_song_dict = {}  # {station : file path}
    current_song_dict = {}  # each thread writes the new title to the station key name {station : title}
    write_command = {}  # recorder head thread set command to copy first file
    search_pattern_found = {}
    http_server_port_number = {}  # {key: number}

    @staticmethod  # copy keep-alive timeout=3000
    def ghetto_recorder_display_titel(url, ini_key):
        # print(f' ghetto_recorder_display_titel: {ini_key}')
        update_terminal = ''.encode('utf-8')
        stream_song_name = GRecorder.current_song_dict[ini_key]
        GIni.fail_meta_dict[url] = 'False'  # message display or not
        GRecorder.search_pattern_found[ini_key] = False

        while not GBase.exit_app:

            if not len(stream_song_name) <= 2:
                #  GRecorder.current_song_dict[ini_key] = stream_song_name  # WRITE SONG NAME   # :DEACTIVATED:
                stream_song_name = GRecorder.current_song_dict[ini_key]  # :REVERSE:

                if not update_terminal == stream_song_name:
                    update_terminal = stream_song_name
                    try:
                        print(f'\t\t {GBase.this_time().split()[1]} title on {ini_key}: \t {update_terminal}')
                        # see what häppens, góod unìt têst case
                    except UnicodeEncodeError:
                        print('\t\t title on ' + ini_key + ':\t' + 'unicode error (check "$ localectl status")')
                        print('\t\t title on ' + ini_key + ':\t' + 'consider to add additional language support.')

                    except Exception as ex:
                        print('\t\t title on ' + ini_key + ':\t' + 'unknown error (print to your terminal)')
                        print(ex)
                    else:
                        pass
            # give recorder command to record, if we got a match from search gui
            #

            try:
                for _ in GIni.search_title_keys_list:
                    if _ == ini_key:
                        # search option was checked,
                        # call - def search_pattern_start_record, search string match?
                        got_it = GRecorder.search_pattern_start_record(stream_song_name, ini_key)
                        if got_it:
                            GIni.start_stop_recording[ini_key] = 'start'
                        else:
                            GIni.start_stop_recording[ini_key] = 'stop'
                            GRecorder.search_pattern_found[ini_key] = False

            except Exception as ex:
                print(ex)

            for sec in range(GBase.sleeper):
                sleep(1)
                if GBase.exit_app:
                    print(f' stop get title {ini_key}')
                    break
            # To Do: make (complete) fake headers to keep connection up
            #        sync sleep time with recorder
            #        one file record with name

    @staticmethod
    def search_pattern_start_record(title, ini_key):
        # search title for strings to see if we should start recording this
        search_list = []  # chop the string

        try:
            strings = GIni.search_dict[ini_key]  # dict with user search strings
            search_list = strings.encode('utf-8').lower().split(b' ')
        except KeyError as ex:
            pass

        for search_str in search_list:

            if not len(search_str) <= 1:  # b'' match problem

                if not title.encode('utf-8').lower().find(search_str) == -1:  # find() returns -1, if not found
                    if not GRecorder.search_pattern_found[ini_key]:
                        print(f'<<<< match station: {ini_key} phrase: {search_str}')
                        GRecorder.search_pattern_found[ini_key] = True
                    return True
        return False

    @staticmethod  # org
    def record_songs(url, directory_save, stream_suffix, radio_short_key, path_to_song_dict):

        # ORIGINAL
        print('record_songs')
        stream_request_size = io.DEFAULT_BUFFER_SIZE
        fresh_song = 'False'
        old_time = time()
        sleeper_recorder = False

        try:
            # only set in GUI
            if GIni.start_stop_recording[radio_short_key] == 'stop':
                sleeper_recorder = True
        except KeyError:
            pass

        sleep(GBase.sleeper + 1)
        stream_song_name_path = GRecorder.path_to_song_dict[radio_short_key]  # PATH to file

        try:
            request = GNet.http_pool.request('GET', url, preload_content=False, retries=10)
        except urllib3.exceptions.NewConnectionError:
            print('Connection failed. ' + url)
        except HTTPError:
            pass
        except URLError as error:
            print(f' ---> {radio_short_key} server timeout: {error} (no recording) {url}')
        else:
            # print(' \n Recording ... ')
            request.auto_close = False  # NOT DEL !!! :) , for continuous recording fine

            while not GBase.exit_app:
                while not GBase.exit_app:
                    if GIni.start_stop_recording[radio_short_key] == 'stop':
                        sleep(.1)
                    else:
                        # print(f'----> else {radio_short_key} sleeper_recorder {sleeper_recorder}'
                        #      f' dict {GIni.start_stop_recording[radio_short_key]}')
                        if sleeper_recorder:
                            print(f'----> start record: {radio_short_key}')
                            try:
                                # recorder def looses connect if too long idle
                                request = GNet.http_pool.request('GET', url, preload_content=False, retries=10)
                            except urllib3.exceptions.NewConnectionError:
                                pass
                        break
                i = 0
                while not GBase.exit_app:  # outer loop create empty new files

                    if GIni.start_stop_recording[radio_short_key] == 'stop':
                        print(f'----> stop record: {radio_short_key}')

                        break

                    if not fresh_song == stream_song_name_path:

                        fresh_song = stream_song_name_path  # check if it can be removed, we look in a dict now
                        clean_name = GBase.remove_special_chars(stream_song_name_path)

                        if clean_name == '_no-name-record_no_split_':  # init name of title on startup
                            clean_name = clean_name + GBase.this_time()
                            clean_name = GBase.remove_special_chars(clean_name)

                        fresh_file = directory_save + '//' + clean_name + stream_suffix
                        if i == 5:
                            print(f' \t\t\t\t\t\t(  (  ( (Ghetto Recorder) )  )  ) )')
                            i = 0
                        i += 1

                        with open(fresh_file, 'wb') as record_file:

                            while not GBase.exit_app:  # inner loop get the stream and write into file
                                print(f' rec. again')
                                for chunk in request.stream(stream_request_size):
                                    record_file.write(chunk)
                                    print('rec')
                                    # stream_song_name_path_new = GRecorder.path_to_song_dict[radio_short_key]

                                    # chunk = request.read(stream_request_size)  # wasting no space in cluster size
                                # record_file.write(chunk)
                                # this_chunk_len = int(len(chunk))
                                # result = result + this_chunk_len

                                if time() - old_time > 60:
                                    old_time = time()
                                    # print(f' {radio_short_key} mb/min: {round((result / 1024) / 1024, 2)} mb')
                                    # result = 0
                                if not chunk:
                                    record_file.flush()
                                    break

                                stream_song_name_path_new = GRecorder.path_to_song_dict[
                                    radio_short_key]  # look what's new

                                if not stream_song_name_path_new == '':  # some weired stations send this string
                                    stream_song_name_path = stream_song_name_path_new
                                if not fresh_song == stream_song_name_path:  # only here break, jump to outer loop
                                    record_file.flush()
                                    break

                            if GBase.exit_app:
                                print(f' exit record {radio_short_key}')
                                break
        return

    @staticmethod
    def ghetto_recorder_head(directory_save, stream_suffix, radio_short_key):
        # target: tail works without brain until brain call interrupt
        # print(f' ghetto_recorder_head -- {radio_short_key}')
        sleep(GBase.sleeper)
        # reader must work (conn. url) for writing the path from title name, can have a loop here
        fresh_song = 'False'
        first_record = True
        main_brake = False
        GRecorder.write_command[radio_short_key] = False

        stream_song_name = GRecorder.current_song_dict[radio_short_key]

        while not main_brake:
            i = 0
            while not GBase.exit_app:
                if not fresh_song == stream_song_name:

                    if i == 5:
                        print(f' \t\t\t\t\t\t(  (  ( (Ghetto Recorder) )  )  ) )')
                        i = 0
                    i += 1

                    fresh_song = stream_song_name  # check if it can be removed, we look in a dict now
                    clean_name = GBase.remove_special_chars(stream_song_name)
                    if clean_name == 'untitled_full_record_':  # init name of title on startup
                        clean_name = clean_name + radio_short_key + '_date_' + GBase.this_time()
                        clean_name = GBase.remove_special_chars(clean_name)

                    if first_record:
                        fresh_file_path = directory_save + '//' + '_incomplete_' + clean_name + stream_suffix
                        main_brake = True
                        GRecorder.path_to_song_dict[radio_short_key] = fresh_file_path
                        GRecorder.write_command[radio_short_key] = True

                        first_record = False
                    else:
                        fresh_file_path = directory_save + '//' + clean_name + stream_suffix
                        GRecorder.path_to_song_dict[radio_short_key] = fresh_file_path  # NEW PATH ... ... ...

                    if GBase.exit_app:
                        print(f' exit head {radio_short_key}')
                        break

                    while not GBase.exit_app:

                        stream_song_name = GRecorder.current_song_dict[radio_short_key]
                        if not fresh_song == stream_song_name:
                            break

                        for sec in range(5):
                            if GBase.exit_app:
                                fresh_file_path = directory_save + '//' + '_incomplete_' + clean_name + stream_suffix
                                GRecorder.path_to_song_dict[radio_short_key] = fresh_file_path
                                print(f' head_ {radio_short_key}')
                                break
                            sleep(1)

    @staticmethod  # org
    def ghetto_recorder_tail(url, key, path_to_save, port_number):
        # shall be as dump as possible
        while not GBase.exit_app:
            try:
                if GRecorder.write_command[key]:
                    break
            except KeyError:
                pass
            else:
                sleep(.1)

        stream_request_size = io.DEFAULT_BUFFER_SIZE
        old_time = time()
        must_run = False
        brake_loop = False
        request = ''
        rand_short = random.randrange(4, 13, 3)
        rand_long = random.randrange(61, 90, 1)

        ghetto_recorder = path_to_save + '//__ghetto_recorder' + GIni.srv_param_dict[key + '_file']
        ghetto_copy = GRecorder.path_to_song_dict[key]  # that's why we have a write command, tail in sync with head

        handler_http_srv_object = MyHttpRequestHandler
        if port_number:
            # Create http server thread for local listening from record stream on port: number
            port = port_number  # dict for {key: port}
            # handler_http_srv_object = MyHttpRequestHandler
            my_server = socketserver.TCPServer(("", port), handler_http_srv_object)
            threading.Thread(target=my_server.serve_forever, name=key, daemon=True).start()
            handler_http_srv_object.content_type = GIni.content_type[key]  # set type for browser to play

        while not GBase.exit_app:
            # ################################# seek
            while not GBase.exit_app:
                if GIni.start_stop_recording[key] == 'stop':
                    brake_loop = False
                    must_run = True
                    sleep(.1)
                else:
                    if must_run:
                        print(f'----> start record: {key}')
                    break
                    # #########################
            try:
                request = GNet.http_pool.request('GET', url,
                                                 headers={'Connection': 'keep-alive'},
                                                 timeout=3000,
                                                 preload_content=False)
            except:
                pass

            while not GBase.exit_app:
                with open(ghetto_recorder, 'wb') as record_file:
                    if brake_loop:  # start_stop_recording stop, can change again to start at run.
                        break

                    for chunk in request.stream(stream_request_size):  # chunks to file
                        # ################################### seek
                        if GIni.start_stop_recording[key] == 'stop':
                            must_run = False
                            brake_loop = True
                            try:
                                if os.path.exists(ghetto_copy):
                                    os.remove(ghetto_copy)
                                record_file.flush()
                                shutil.copyfile(ghetto_recorder, ghetto_copy)
                            except Exception as ex:
                                print(ex)
                            else:
                                pass
                            print(f'----> stop record: {key}')
                            break

                        # ################################### rec

                        if port_number:
                            handler_http_srv_object.fifo_http_chunk_queue.put(chunk)  # copy chunk to http server
                        record_file.write(chunk)  # start writing ...
                        if not ghetto_copy == GRecorder.path_to_song_dict[key]:

                            try:
                                if os.path.exists(ghetto_copy):
                                    os.remove(ghetto_copy)
                                record_file.flush()
                                shutil.copyfile(ghetto_recorder, ghetto_copy)
                            except Exception as ex:
                                print(ex)
                            else:
                                record_file.truncate()
                                record_file.seek(0)

                        ghetto_copy = GRecorder.path_to_song_dict[key]  # SET NEW PATH after copy
                        # #################################
                        if time() - old_time > rand_short:
                            old_time = time()
                            rh = request.headers
                            rand_short = random.randrange(4, 12, 2)

                        if time() - old_time > rand_long:
                            old_time = time()
                            try:
                                request = GNet.http_pool.request('GET', url,
                                                                 headers={'Connection': 'keep-alive'},
                                                                 timeout=3000,
                                                                 preload_content=False)
                            except:
                                pass
                            rand_long = random.randrange(61, 90, 1)
                            rand_short = random.randrange(4, 13, 3)
                        if not chunk:
                            request = GNet.http_pool.request('GET', url,
                                                             headers={'Connection': 'keep-alive'},
                                                             timeout=3000,
                                                             preload_content=False)
                            rh = request.headers  # into oblivion
                            break
                        if GBase.exit_app:
                            sleep(2)  # wait for last file name _incomplete_.....
                            try:
                                record_file.flush()
                                ghetto_copy = GRecorder.path_to_song_dict[key]
                                print(f' {key} copy last file to folder (marked: _incomplete_): '
                                      f'{GRecorder.current_song_dict[key]} ')
                                shutil.copyfile(ghetto_recorder, ghetto_copy)
                                record_file.close()

                                if os.path.exists(ghetto_recorder):
                                    os.remove(ghetto_recorder)
                            except UnicodeEncodeError:
                                print(f' {key} copy last file (marked: _incomplete_):')
                            except Exception as ex:
                                print(ex)
                            break
                if GBase.exit_app:
                    break
            if GBase.exit_app:
                print(f' exit record {key}')
                break

    @staticmethod
    def get_metadata_from_stream_loop(url, key):
        # urllib3 request.stream with headers={'Icy-MetaData': '1'} , keep open (mdr, swr, br5) test
        rh = ''
        response = ''
        request = ''
        old_time = time()
        rand_short = random.randrange(4, 12, 2)
        rand_long = random.randrange(50, 80, 1)

        while not GBase.exit_app:
            try:
                response = GNet.http_pool.request('GET', url,
                                                  headers={'Connection': 'keep-alive'},
                                                  timeout=3000, preload_content=False)
            except:
                pass

            while not GBase.exit_app:

                if time() - old_time > rand_short:
                    old_time = time()
                    rh = response.headers  # keep conn. alive
                    rand_short = random.randrange(4, 12, 2)
                    # print(response.headers)

                if time() - old_time > rand_long:  # new connection
                    old_time = time()
                    rand_long = random.randrange(50, 80, 1)
                    break
                try:
                    request = GNet.http_pool.request('GET', url,
                                                     headers={'Icy-MetaData': '1'},
                                                     preload_content=False)
                except:
                    pass

                try:
                    icy_metadata = request.headers['icy-metaint']
                    icy_metadata = int(icy_metadata)

                    request.read(icy_metadata)
                    chunk_1b = request.read(1)
                    chunk_1b = ord(chunk_1b)
                    read_bytes = chunk_1b * 16
                    read_bytes = int(read_bytes)
                    metadata_content = request.read(read_bytes)
                    metadata_content = metadata_content.decode('utf-8')
                    title_info = metadata_content.split(";")
                    title_info = title_info[0].split("=")
                    title_info = GBase.remove_special_chars(title_info[1])
                    request.release_conn()  # REQUEST not response, a one shot anyway
                    # print(f' -> {key} + {title_info}')
                except Exception as ex:
                    print(ex)
                else:
                    # print(f' -> {key} + {title_info}')
                    try:
                        GRecorder.current_song_dict[key] = title_info

                    except KeyError:
                        pass
                    except:
                        pass
                    else:
                        for sec in range(rand_short):
                            if GBase.exit_app:
                                print(f' out {key} reader')
                                break
                            sleep(1)

    @staticmethod
    def fire_get_metadata(url, key):

        meta_queue = queue.Queue()
        thread1 = threading.Thread(name="thread_meta_daemon",
                                   target=GRecorder.get_metadata_from_stream_url,  # change def here (url, stream)
                                   args=(url, key, meta_queue))
        thread1.setDaemon(True)
        thread1.start()
        # ret = thread1.join()
        thread1.join()
        print(thread1.getName())
        # while not meta_queue.empty():
        meta_value = meta_queue.get()
        print(f' back fire {meta_value}')
        return ' fire thread1'

    @staticmethod
    def record_songs_stream(url, directory_save, stream_suffix, radio_short_key, path_to_song_dict):
        # COPY

        print('record_songs_stream')
        fresh_song = 'False'
        old_time = time()
        sleeper_recorder = False
        flag_red = False
        try:
            if GIni.start_stop_recording[radio_short_key] == 'stop':  # only set in GUI
                sleeper_recorder = True
        except Exception as ex:
            print(ex)
            pass
        else:

            sleep(GBase.sleeper + 1)
            stream_song_name_path = GRecorder.path_to_song_dict[radio_short_key]

            while not GBase.exit_app:
                while not GBase.exit_app:
                    if GIni.start_stop_recording[radio_short_key] == 'stop':
                        sleep(.1)
                i = 0
                print(f' \t\t\t\t\t\t(  (  ( (Ghetto Recorder) )  )  ) )')
                while not GBase.exit_app:  # outer loop create empty new files

                    if GIni.start_stop_recording[radio_short_key] == 'stop':
                        print(f'----> stop record: {radio_short_key}')

                        break

                    if not fresh_song == stream_song_name_path:

                        fresh_song = stream_song_name_path  # check if it can be removed, we look in a dict now
                        clean_name = GBase.remove_special_chars(stream_song_name_path)

                        if clean_name == '_no-name-record_no_split_':  # init name of title on startup
                            clean_name = clean_name + GBase.this_time()

                        if i == 5:
                            print(f' \t\t\t\t\t\t(  (  ( (Ghetto Recorder) )  )  ) )')
                            i = 0
                        i += 1

                        fresh_file = directory_save + '//' + clean_name + stream_suffix
                        GRecorder.path_to_song_dict[radio_short_key] = fresh_file  # new file  with PATH!!!
                        # print(f'GRecorder.current_song_dict  {GRecorder.current_song_dict[radio_short_key]}')
                        while not GBase.exit_app:  # inner loop get the stream and write into file

                            stream_song_name_path_new = GRecorder.path_to_song_dict[radio_short_key]  # look what's new
                            if not stream_song_name_path_new == '':  # some weired stations send this string
                                stream_song_name_path = stream_song_name_path_new  # set old one again
                            if not fresh_song == stream_song_name_path:  # only here break, jump to outer loop
                                break

                            sleep(.1)

                        if GBase.exit_app:
                            break
        return

    @staticmethod
    def get_metadata_from_stream_url(url, key, meta_queue):
        # COPY
        # print('get_metadata_from_stream_url')
        headers = {'Icy-MetaData': '1'}
        request = urllib.request.Request(url, headers=headers)

        try:
            with urllib.request.urlopen(request) as response:
                # response = GNet.connect_url(request, url, key, 'icy-metaint')  # one time shot
                response_content = response.getheader('icy-metaint')
                icy_metadata = response_content
                icy_metadata = int(icy_metadata)
        except KeyError as ke:
            print(ke)
            print('Connection failed miserable in get_metadata_from_stream reader: ' + url)
            GIni.fail_meta_dict[url] = 'True'
        else:
            with urllib.request.urlopen(request) as response:  # with urllib ... keeps conn. open
                response.read(icy_metadata)
                chunk_1b = response.read(1)
                chunk_1b = ord(chunk_1b)
                read_bytes = chunk_1b * 16
                read_bytes = int(read_bytes)
                metadata_content = response.read(read_bytes)
                metadata_content = metadata_content.decode('utf-8')
                title_info = metadata_content.split(";")
                title_info = title_info[0].split("=")
                title_info = GBase.remove_special_chars(title_info[1])
                return meta_queue.put(title_info)

    @staticmethod  # org
    def get_metadata_from_stream(url, key):
        # urllib3 request.stream with headers={'Icy-MetaData': '1'} , keep open (mdr, swr, br5) test
        # all 71 sec. extra icy request
        # print(' get_metadata_from_stream')
        try:
            request = GNet.http_pool.request('GET', url, headers={'Icy-MetaData': '1'}, preload_content=False)

            icy_metadata = request.headers['icy-metaint']
            icy_metadata = int(icy_metadata)
        except KeyError as ke:
            print(ke)
            print('Connection failed miserable in get_metadata_from_stream reader: ' + url)
            GIni.fail_meta_dict[url] = 'True'
        else:
            request.read(icy_metadata)
            chunk_1b = request.read(1)
            chunk_1b = ord(chunk_1b)
            # \x03 hex value, was div. by 4; hex C (12d) * hex 4 = 30 48d; hex 3 (3d) * 16d = 48d;
            read_bytes = chunk_1b * 16
            read_bytes = int(read_bytes)
            metadata_content = request.read(read_bytes)
            metadata_content = metadata_content.decode('utf-8')
            title_info = metadata_content.split(";")
            title_info = title_info[0].split("=")
            title_info = GBase.remove_special_chars(title_info[1])
            request.release_conn()
            # print(f' -> {key} + title_info')
            return title_info

    @staticmethod
    def playlist_m3u(url, key):
        # returns the first server of the playlist (not only m3u)
        try:
            read_url = GNet.http_pool.request('GET', url, preload_content=False)
        except Exception as ex:
            print(ex)
        else:
            file = read_url.read().decode('utf-8')

            m3u_lines = file.split("\n")
            # print(' \n    m3u_lines    ' + file)
            m3u_lines = list(filter(None, m3u_lines))  # remove empty rows
            m3u_streams = []
            for row_url in m3u_lines:
                if row_url[0:4].lower() == 'http'.lower():
                    m3u_streams.append(row_url)  # not to lower :)
                    # print(len(m3u_streams))

            if len(m3u_streams) > 1:
                print(f' {key} Have more than one server in playlist_m3u. !!! Take first stream available.')
                play_server = m3u_streams[0]
                return play_server
            if len(m3u_streams) == 1:
                # print(' One server found in playlist_m3u')
                play_server = m3u_streams[0]
                return play_server
            if len(m3u_streams) == 0:
                # print(' No http ... server found in playlist_m3u !!! -EXIT-')
                return False


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):

    fifo_http_chunk_queue = queue.Queue(maxsize=10)  # (buffer) we are 10 chunks behind record thread
    content_type = "audio/mpeg"  # instance, will be overwritten
    # port 1242 - 1270 free

    def do_GET(self):

        self.send_response(200)
        self.send_header("Content-type", self.content_type)
        self.send_header("Cache-Control", "no-cache,no-store")
        self.send_header("Connection", "keep-alive")
        self.end_headers()
        print(f'\t In the moment, only the FIRST radio can be listened to on local IP.')
        print(f'\t Only one browser.')
        print(f"\t Sound file: {self.content_type}, some browser don't play and try to download. "
              f"(high quality .aacp)")
        while not GBase.exit_app:
            try:
                self.wfile.write(self.fifo_http_chunk_queue.get())
            except ConnectionAbortedError:
                print(' local IP connection aborted')
                self.close_connection = True
                break
            except Exception as e:
                print(e)
                self.close_connection = True
                break
            else:
                pass


def step1_collect_stream_server():
    # collect the keys from settings.ini, test if server is alive
    # produce a dictionary with key: short name, value: url
    try:
        if os.environ["SNAP"]:
            print('GR in Ubuntu Snap Container')
            switch_dst_dir('SNAP')
    except KeyError:
        pass
    try:
        if os.environ["DOCKER"]:
            print('GR in Docker Container')  # set var in Dockerfile DOCKER=True
            switch_dst_dir('DOCKER')
    except KeyError:
        pass

    GIni.show_items_ini_file()  # print to terminal
    valid_input = False
    while True:  # collect a list of radio keys to work on
        ini_file_input = input('Copy/Paste a Radio >> settings.ini <<, Enter to record -->:')
        if ini_file_input == 42:
            valid_input = True
            # read all keys from ini file

        if ini_file_input == '':  # exit, or valid_input go next
            break
        else:
            valid_input = True
            print(f' Hit Enter <---| to RECORD, or paste next radio, paste 42 for ALL radios ')
            str_key = ini_file_input.strip()

            if str_key:
                str_val = GIni.find_ini_file(GBase.remove_special_chars(str_key))

                if str_key == '42':
                    # if 42, return gives a list instead of a value
                    str_list = GIni.find_all_in_stations()
                    for ini_key in str_list:
                        ini_row_value = str_list[ini_key]
                        add_server_to_data_base_auto(ini_key, ini_row_value)
                else:
                    add_server_to_data_base_auto(str_key, str_val)  # work with one value

    if valid_input:
        step2_test_stream_server(GIni.ini_keys)


def add_server_to_data_base_auto(str_key, str_val):
    # no screen to choose server from list, auto take first one, most of the time the best quality
    is_playlist_server = ''
    GIni.ini_keys[str_key] = str_val  # append url to dictionary as value for radio key name
    GBase.make_directory(GBase.radio_base_dir)
    GBase.make_directory(GBase.radio_base_dir + '//' + str_key)
    # is_playlist_server = GNet.playlist_server(GIni.ini_keys[str_key])  # look in file if suffix is m3u stuff

    # playlist url?
    if str_val[-4:] == '.m3u' or str_val[-4:] == '.pls':  # or url[-5:] == '.m3u8' or url[-5:] == '.xspf':
        # take first from the list
        is_playlist_server = GRecorder.playlist_m3u(str_val, str_key)

    if not is_playlist_server == '':  # update dictionary with url selected from playlist ON SERVER
        if GNet.is_server_alive(GIni.ini_keys[str_key], str_key):
            GIni.ini_keys[str_key] = is_playlist_server  # append dictionary of servers to conn.
        else:
            print('   --> playlist_server server failed, no recording')

    GNet.is_server_alive(GIni.ini_keys[str_key], str_key)


def add_server_to_data_base(str_key, str_val):
    # manual copy url on screen
    GIni.ini_keys[str_key] = str_val  # append url to dictionary as value for radio key name
    GBase.make_directory(GBase.radio_base_dir)
    GBase.make_directory(GBase.radio_base_dir + '//' + str_key)

    is_playlist_server = GNet.playlist_server(GIni.ini_keys[str_key])  # look in file if suffix is m3u stuff

    if is_playlist_server:  # update dictionary with url selected from playlist ON SERVER
        GIni.ini_keys[str_key] = is_playlist_server  # append dictionary, then test if it is alive
        if not GNet.is_server_alive(GIni.ini_keys[str_key], str_key):
            print('   --> playlist_server server failed, no recording')
            del GIni.ini_keys[str_key]  # exercise, no try since it is known


def step2_test_stream_server(ini_keys):
    # further update dictionary
    # calc_connection_cost()
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(test_stream_server, key) for key in ini_keys}

        for fut in as_completed(futures):
            pass
            # print(f"The outcome is {fut.result()} {fut.__dict__}")

    for radio in GNet.is_no_meta_avail_dict:
        print(f' {radio} \t\t url: {GIni.ini_keys[radio]}')
        radio_failed = GNet.is_no_meta_avail_dict[radio]
        if radio_failed:
            del GIni.ini_keys[radio]
            print(f' ---> {radio}: deleted from record list. Check, if server has multiple '
                  f'streams (quality or user limits) {GIni.srv_param_dict[radio]}')

    record(ini_keys, False)
    # record(ini_keys, GIni.srv_param_dict)  # this starts record threads and loops at end for shutdown signal


def init_dicts_srv_type(key):
    GNet.is_shout_dict[key] = False
    GNet.is_ice_dict[key] = False
    GNet.is_ice_json_dict[key] = False
    GNet.is_unk_dict[key] = False
    GNet.is_no_meta_avail_dict[key] = False


def calc_connection_cost():
    for item in GIni.cost_dict:
        print(f' key: {item} Bytes: {GIni.cost_dict[item]}, title search only - cost per/hour: '
              f'{round(((int(GIni.cost_dict[item]) * 30 * 60) / 1024) / 1024, 2)}mb')


def print_stream_server():
    print(f'GIni.srv_param_dict {GIni.srv_param_dict}')


def record(ini_key_val, break_loop):
    # {blues_uk: http//......}
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    first_radio = True
    port_number = 1242  # 1242 - 1270 free ports

    for ini_key in ini_key_val:
        stream_suffix = '.mp3'  # fix for 50%, lol
        try:
            stream_suffix = GIni.srv_param_dict[ini_key + '_file']  # sometimes malformed content-type written?
        except KeyError:
            stream_suffix = '.mp3'
        except Exception as ex:
            pass

        GRecorder.current_song_dict[ini_key] = '_no-name-record_no_split_'  # init the dict for this thread
        GIni.start_stop_recording[ini_key] = 'start'
        # GIni.start_stop_recording[ini_key] = 'stop'            # init it here, should be set via user interface
        GIni.start_stop_recording[ini_key + '_adv'] = 'start_from_here'  # MUST be set or a key error in record def:

        url = GIni.ini_keys[ini_key]
        dir_save = GBase.radio_base_dir + '//' + ini_key

        GBase.pool.submit(GRecorder.ghetto_recorder_display_titel, url, ini_key)
        GBase.pool.submit(GRecorder.ghetto_recorder_head, dir_save, stream_suffix, ini_key)
        if first_radio:
            GBase.pool.submit(GRecorder.ghetto_recorder_tail, url, ini_key, dir_save, port_number)  # GUI!!
            print(f'{ini_key} >> listen << to your sound: http://127.0.0.1:{port_number}, redirected '
                  f'local to save bandwidth.')
            print(f'\t\t >>Bookmark<< in your Browser')
        else:
            GBase.pool.submit(GRecorder.ghetto_recorder_tail, url, ini_key, dir_save, False)
        GBase.pool.submit(GRecorder.get_metadata_from_stream_loop, url, ini_key)

        # GRecorder.http_server_port_number[ini_key] = port_number
        port_number += 10
        first_radio = False

    while not GBase.exit_app:
        if break_loop:
            break
        sleep(1)


def test_stream_server(key):
    # srv_param_dict is a simulation of a db for collecting all bool vars, file types, short urls
    # to fire then the http connects and feed the title pull def with correct connection type: json, http, stream
    ini_keys = GIni.ini_keys  # for not twisting brain at end of def / the dict with the radio names
    # GIni.cost_current_ini = key  # for Byte cost calculation / should switch to dict

    # write next dictionary with connection parameters
    GIni.srv_param_dict[key] = GIni.ini_keys[key]
    # print(f'   GIni.srv_param_dict[key]   {GIni.srv_param_dict[key]}    {path_dict[key]}')

    GIni.srv_param_dict[ini_keys[key]] = GIni.parse_url_simple_url(GIni.srv_param_dict[key])  # http://ip:port

    # init the dicts with False, store server types
    init_dicts_srv_type(key)
    # server type, either read the title from http, json file or from http stream
    # each server type property has a dict, { radio name : False/True}, with a small db it would be much cleaner
    # GNet.is_shout_ice_unknown_server(server_port, full_url, key)
    if GNet.is_shout_ice_unknown_server(GIni.srv_param_dict[ini_keys[key]], GIni.srv_param_dict[key], key):
        # if this server is halfway a radio server

        # str_in is input, modify to get more dictionary keys; file type, is shout is ice ...
        ret = GNet.stream_filetype_url(GIni.srv_param_dict[key], key)
        if not ret:
            GIni.srv_param_dict[key + '_is_no_meta_data_avail'] = 'True'
        else:
            GIni.srv_param_dict[key + '_file'] = ret
            if ret is None or ret == '' or ret == ' ':
                GIni.srv_param_dict[key + '_file'] = '.mp3'

        if GNet.is_shout_dict[key]:
            GIni.srv_param_dict[key + '_is_shoutcast_server'] = 'True'
        else:
            GIni.srv_param_dict[key + '_is_shoutcast_server'] = 'False'
        if GNet.is_ice_dict[key]:
            GIni.srv_param_dict[key + '_is_icecast_server'] = 'True'
        else:
            GIni.srv_param_dict[key + '_is_icecast_server'] = 'False'
        if GNet.is_ice_json_dict[key]:
            GIni.srv_param_dict[key + '_is_icecast_json'] = 'True'
        else:
            GIni.srv_param_dict[key + '_is_icecast_json'] = 'False'
        if GNet.is_unk_dict[key]:
            GIni.srv_param_dict[key + '_is_unknown_server'] = 'True'
        else:
            GIni.srv_param_dict[key + '_is_unknown_server'] = 'False'
        if GNet.is_no_meta_avail_dict[key]:
            GIni.srv_param_dict[key + '_is_no_meta_data_avail'] = 'True'
        else:
            GIni.srv_param_dict[key + '_is_no_meta_data_avail'] = 'False'


def main():
    step1_collect_stream_server()


if __name__ == '__main__':
    main()
