import simplejson as json


class JSONEncoder(json.JSONEncoder):
    def default(self, z):
        try:
            if "to_json" in dir(z):
                return z.to_json()
            else:
                return super(JSONEncoder, self).default(z)
        except Exception as e:
            print(e)
