import json
import threading

lock = threading.Lock()

# Open the file in read-write mode with buffering disabled
with open("govdata.json", "r+") as stream:
    Data = json.load(stream)

queue = []

cship_status_active = 0
cship_status_revoked = 1

class Citizenship:
    def __init__(self, status: int) -> None:
        self.status = status
    def isActive(self) -> bool:
        return self.getStatus() == cship_status_active
    def getStatus(self) -> int:
        return self.status
    def json(self):
        return {
            'status': self.status
        }
    def revoke(self):
        self.status = cship_status_revoked
    def status_str(self) -> str:
        match (self.status):
            case (0):
                return "ACTIVE"
            case (1):
                return "REVOKED"
        return "UNKNOWN"
    @staticmethod
    def from_json(json: dict):
        status = json.get("status")
        if (status == None):
            status = 0
        return Citizenship(status)

class Offense:
    def __init__(self, type):
        self.type = type
    def json(self):
        return self.type.upper()
    @staticmethod
    def from_json(json: dict):
        type = json.get('type')
        return Offense(
            type = type
        )

class License:
    def __init__(self, license_type, active) -> None:
        self.license_type = license_type
        self.active = active
    def json(self):
        return {
            'type': self.license_type,
            'active': self.active
        }
    def is_active(self):
        return self.active
    @staticmethod
    def from_json(json: dict):
        type = json.get('type')
        active = json.get('active')
        return License(
            license_type = type,
            active = active
        )

class Citizen:
    def __init__(self, name, offenses, licenses, citizenship, day_registered) -> None:
        self.name = name
        self.offenses = offenses
        self.licenses = licenses
        self.citizenship = citizenship
        self.day_registered = day_registered
    def add_offense(self, offense: Offense):
        self.offenses.append(offense)
    def add_license(self, license: License):
        self.licenses.append(license)
    def get_name(self) -> str:
        return self.name
    def get_citizenship(self) -> Citizenship:
        return self.citizenship
    def revoke_citizenship(self):
        self.get_citizenship().revoke()
    def get_licenses(self) -> list[License]:
        return self.licenses
    def get_offenses(self) -> list[Offense]:
        return self.offenses
    def get_day_registered(self) -> int:
        return self.day_registered
    def json_licenses(self):
        o = self.get_licenses()
        ret = []
        for license in o:
            ret.append(license.json())
        return ret
    def json_offenses(self):
        o = self.get_offenses()
        ret = []
        for offense in o:
            ret.append(offense.json())
        return ret
    def json(self):
        return {
            'name': self.get_name(),
            'offenses': self.json_offenses(),
            'licenses': self.json_licenses(),
            'citizenship': self.get_citizenship().json(),
            'day_registered': self.get_day_registered()
        }
    def commit(self):
        SetCitizen(self.get_name(), self.json())
    @staticmethod
    def from_json(json: dict):
        name = json.get('name')
        offenses_json = json.get('offenses')
        licenses_json = json.get('licenses')
        citizenship_json = json.get('citizenship')
        day_registered = json.get('day_registered')

        if (citizenship_json == None):
            citizenship_json = Citizenship(cship_status_active).json()
        if (day_registered == None):
            day_registered = -1

        offenses = []
        licenses = []
        citizenship = Citizenship.from_json(citizenship_json)
        for offense_json in offenses_json:
            offense: Offense = Offense.from_json(offense_json)
            offenses.append(offense)
        for license_json in licenses_json:
            license: License = License.from_json(license_json)
            licenses.append(license)
        return Citizen(
            name = name,
            offenses = offenses,
            licenses = licenses,
            citizenship = citizenship,
            day_registered = day_registered
        )

def GetCitizenObj(name) -> Citizen:
    json_user = Data['citizens'].get(name)
    if json_user is not None:
        return Citizen.from_json(json_user)
    else:
        return None


# def WriteUser(name: str, key: str, value):
#     def operation():
#         global Data
#         with lock, open("govdata.json", "r+") as stream:
#             Data = json.load(stream)
#             logins = Data['logins']
#             user = logins.get(name)
#             if user:
#                 logins[name][key] = value
#             stream.seek(0)
#             content = json.dumps(Data, indent=4)
#             stream.write(content)
#             stream.truncate()
#     operation()
    # queue.append(operation)

def RefreshData():
    def operation():
        global Data
        with lock, open("govdata.json", "r") as stream:
            Data = json.load(stream)
    operation()

def SetUser(name: str, value):
    def operation():
        global Data
        with lock, open("govdata.json", "r+") as stream:
            Data = json.load(stream)
            logins = Data['users']
            logins[name] = value
            stream.seek(0)
            content = json.dumps(Data, indent=4)
            stream.write(content)
            stream.truncate()
    operation()

def SetCitizen(name: str, value):
    def operation():
        global Data
        with lock, open("govdata.json", "r+") as stream:
            Data = json.load(stream)
            citizens = Data['citizens']
            citizens[name] = value
            stream.seek(0)
            content = json.dumps(Data, indent=4)
            stream.write(content)
            stream.truncate()
    operation()
    # queue.append(operation)

def GetUser(name: str):
    return Data['users'].get(name)
