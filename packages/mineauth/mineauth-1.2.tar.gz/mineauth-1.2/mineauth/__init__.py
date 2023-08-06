__author__ = "Foster Reichert"
__version__ = 1.2
__license__ = "MIT"

import requests, json

class Profile:
    def __init__(self, name, id, raw):
        self.name = name
        self.id = id
        self._raw = raw

    def raw(self):
        return self._raw

class User:
    def __init__(self, email, password):
        self.email = email
        self.agent = {
            "name": "Minecraft",
            "version": 1
        }
        data = {
            "agent": self.agent,
            "username": self.email,
            "password": password,
        }
        data = json.dumps(data)
        headers = {
            "Content-Type": "application/json"
        }
        result = requests.post(
            "https://authserver.mojang.com/authenticate",
            data=data,
            headers=headers
        )
        self._raw = json.loads(result.text)
        try:
            self.client_token = self._raw["clientToken"]
            self.access_token = self._raw["accessToken"]
            self.selected_profile = Profile(
                self._raw["selectedProfile"]["name"],
                self._raw["selectedProfile"]["id"],
                self._raw["selectedProfile"]
            )
            self.available_profiles = []
            for profile in self._raw["availableProfiles"]:
                self.available_profiles.append(Profile(
                    profile["name"],
                    profile["id"],
                    profile
                ))
            self.authenticated = True
        except:
            self.authenticated = False
        
    def raw(self):
        return self._raw
