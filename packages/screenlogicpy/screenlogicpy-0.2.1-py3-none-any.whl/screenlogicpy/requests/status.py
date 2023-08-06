# import json
import struct
from .utility import sendRecieveMessage, getSome
from ..const import code, BODY_TYPE, DEVICE_TYPE, UNIT


def request_pool_status(gateway_socket, data):
    response = sendRecieveMessage(
        gateway_socket, code.POOLSTATUS_QUERY, struct.pack("<I", 0)
    )
    decode_pool_status(response, data)


# pylint: disable=unused-variable
def decode_pool_status(buff, data):
    # print(buff)

    if "config" not in data:
        data["config"] = {}

    config = data["config"]

    ok, offset = getSome("I", buff, 0)
    config["ok"] = {"name": "OK Check", "value": ok}

    freezeMode, offset = getSome("B", buff, offset)
    config["freeze_mode"] = {"name": "Freeze Mode", "value": freezeMode}

    remotes, offset = getSome("B", buff, offset)
    config["remotes"] = {"name": "Remotes", "value": remotes}

    poolDelay, offset = getSome("B", buff, offset)
    config["pool_delay"] = {"name": "Pool Delay", "value": poolDelay}

    spaDelay, offset = getSome("B", buff, offset)
    config["spa_delay"] = {"name": "Spa Delay", "value": spaDelay}

    cleanerDelay, offset = getSome("B", buff, offset)
    config["cleaner_delay"] = {"name": "Cleaner Delay", "value": cleanerDelay}

    # fast forward 3 bytes. Unknown data.
    ff1, offset = getSome("B", buff, offset)
    ff2, offset = getSome("B", buff, offset)
    ff3, offset = getSome("B", buff, offset)

    unittxt = (
        UNIT.CELSIUS
        if "is_celcius" in config and config["is_celcius"]["value"]
        else UNIT.FAHRENHEIHT
    )

    if "sensors" not in data:
        data["sensors"] = {}

    sensors = data["sensors"]

    airTemp, offset = getSome("i", buff, offset)
    sensors["air_temperature"] = {
        "name": "Air Temperature",
        "value": airTemp,
        "unit": unittxt,
        "device_type": DEVICE_TYPE.TEMPERATURE,
    }

    bodiesCount, offset = getSome("I", buff, offset)
    # Should this default to 2?
    bodiesCount = min(bodiesCount, 2)

    if "bodies" not in data:
        data["bodies"] = {}

    bodies = data["bodies"]

    for i in range(bodiesCount):
        bodyType, offset = getSome("I", buff, offset)
        if bodyType not in range(2):
            bodyType = 0

        if i not in bodies:
            bodies[i] = {}

        currentBody = bodies[i]

        if "min_set_point" not in currentBody:
            currentBody["min_set_point"] = {}

        currentBody["min_set_point"]["unit"] = unittxt

        if "max_set_point" not in currentBody:
            currentBody["max_set_point"] = {}

        currentBody["max_set_point"]["unit"] = unittxt

        currentBody["body_type"] = {"name": "Type of body of water", "value": bodyType}

        lastTemp, offset = getSome("i", buff, offset)
        bodyName = "Last {} Temperature".format(BODY_TYPE.NAME_FOR_NUM[bodyType])
        currentBody["last_temperature"] = {
            "name": bodyName,
            "value": lastTemp,
            "unit": unittxt,
            "device_type": DEVICE_TYPE.TEMPERATURE,
        }

        heatStatus, offset = getSome("i", buff, offset)
        heaterName = "{} Heat".format(BODY_TYPE.NAME_FOR_NUM[bodyType])
        currentBody["heat_status"] = {"name": heaterName, "value": heatStatus}

        heatSetPoint, offset = getSome("i", buff, offset)
        hspName = "{} Heat Set Point".format(BODY_TYPE.NAME_FOR_NUM[bodyType])
        currentBody["heat_set_point"] = {
            "name": hspName,
            "value": heatSetPoint,
            "unit": unittxt,
            "device_type": DEVICE_TYPE.TEMPERATURE,
        }

        coolSetPoint, offset = getSome("i", buff, offset)
        cspName = "{} Cool Set Point".format(BODY_TYPE.NAME_FOR_NUM[bodyType])
        currentBody["cool_set_point"] = {
            "name": cspName,
            "value": coolSetPoint,
            "unit": unittxt,
        }

        heatMode, offset = getSome("i", buff, offset)
        hmName = "{} Heat Mode".format(BODY_TYPE.NAME_FOR_NUM[bodyType])
        currentBody["heat_mode"] = {"name": hmName, "value": heatMode}

    circuitCount, offset = getSome("I", buff, offset)

    if "circuits" not in data:
        data["circuits"] = {}

    circuits = data["circuits"]

    for i in range(circuitCount):
        circuitID, offset = getSome("I", buff, offset)

        if circuitID not in circuits:
            circuits[circuitID] = {}

        currentCircuit = circuits[circuitID]

        if "id" not in currentCircuit:
            currentCircuit["id"] = circuitID

        circuitstate, offset = getSome("I", buff, offset)
        currentCircuit["value"] = circuitstate

        cColorSet, offset = getSome("B", buff, offset)
        currentCircuit["color_set"] = cColorSet

        cColorPos, offset = getSome("B", buff, offset)
        currentCircuit["color_position"] = cColorPos

        cColorStagger, offset = getSome("B", buff, offset)
        currentCircuit["color_stagger"] = cColorStagger

        circuitDelay, offset = getSome("B", buff, offset)
        currentCircuit["delay"] = circuitDelay

    pH, offset = getSome("i", buff, offset)
    sensors["ph"] = {"name": "pH", "value": (pH / 100), "unit": "pH"}

    orp, offset = getSome("i", buff, offset)
    sensors["orp"] = {"name": "ORP", "value": orp, "unit": "mV"}

    saturation, offset = getSome("i", buff, offset)
    sensors["saturation"] = {
        "name": "Saturation Index",
        "value": (saturation / 100),
        "unit": "lsi",
    }

    saltPPM, offset = getSome("i", buff, offset)
    sensors["salt_ppm"] = {"name": "Salt", "value": (saltPPM * 50), "unit": "ppm"}

    pHTank, offset = getSome("i", buff, offset)
    sensors["ph_supply_level"] = {"name": "pH Supply Level", "value": pHTank}

    orpTank, offset = getSome("i", buff, offset)
    sensors["orp_supply_level"] = {"name": "ORP Supply Level", "value": orpTank}

    alarm, offset = getSome("i", buff, offset)
    sensors["chem_alarm"] = {
        "name": "Chemistry Alarm",
        "value": alarm,
        "device_type": DEVICE_TYPE.ALARM,
    }
    # print(json.dumps(data, indent=4))
