import sys, json, time
from datetime import datetime

from flask import session
from flask_socketio import emit
from . import socketio

def get_server_data():
    data = {}
    data["version"] = sys.version
    data["time"] = datetime.now().strftime("%m/%d/%Y, %I:%M:%S%p")
    return data

def send_data():
    data = get_server_data()
    emit("update", json.dumps(data))

@socketio.on('connected')
def connection_handler(data):
    pong(data)

@socketio.on('ping')
def pong(data):
    send_data()
    check_services()
    update_client_data()
    time.sleep(1)
    emit("pong")


@socketio.on('setInterfaces')
def set_interface(data):
    from . import app_info
    app_info.sniff_iface = data["sniff_iface"]
    app_info.ap_iface = data["ap_iface"]
    response = {}
    response["success"] = True
    response["data"] = "Successfully set {} and {}".format(app_info.sniff_iface, app_info.ap_iface)
    emit("setInterface", json.dumps(response))

@socketio.on('setAccessPoint')
def set_access_point(data):
    from . import app_info
    response = {}
    response["ssid"] = data["ssid"]
    response["channel"] = data["channel"]
    if(app_info.setup_AP(data["ssid"], data["password"], data["channel"])):
        response["success"] = True
        response["data"] = "Successfully set Access Point {} on channel {}".format(data["ssid"], data["channel"])
    else:
        response["success"] = False
        response["data"] = "Failed to set Access Point {} on channel {}".format(data["ssid"], data["channel"])
    emit("setAccessPoint", json.dumps(response))

@socketio.on('checkServices')
def check_services():
    from . import services

    response = {}
    response["hostapd"] = (services.hostapd != None)
    response["dnsmasq"] = (services.dnsmasq != None)
    response["apssid"] = (services.hostapd != None)
    # print(response)
    emit("checkServices", json.dumps(response))

@socketio.on('checkLogFile')
def update_log_file():
    response = {}
    response["text"] = open("hostapd.log", "r").readlines()
    time.sleep(1)
    emit("updateLogFile", json.dumps(response))


@socketio.on('clientData')
def update_client_data():
    from . import app_info
    response = {}

    '''
    clients = app_info.get_clients(app_info.ap_iface) # TODO: convert to task and use app_info.clients
    response["apclients"] = clients
    emit("clientData", json.dumps(response))
    '''
