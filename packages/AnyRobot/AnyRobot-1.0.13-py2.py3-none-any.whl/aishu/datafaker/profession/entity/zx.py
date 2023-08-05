import jsonpath
import requests,json
from aishu import setting
from aishu.datafaker.profession.entity import id

class search(object):
    def createSearchId(self):
        url = "http://{ip}/v1/search/submit".format(ip=setting.host)
        logGroup = id.date().getDefaultLogGroupID()
        payload = [
            {
                "logGroup": logGroup,
                "query": "*",
                "sort": [
                    {
                        "@timestamp": "desc"
                    }
                ],
                "size": 10,
                "needFieldList": True,
                "filters": {
                    "must": [
                        {
                            "@timestamp": {
                                "from": 1441001644796,
                                "to": 1598854444796
                            }
                        }
                    ],
                    "must_not": []
                }
            }
        ]
        headers = setting.header

        rsp = requests.request("POST", url, headers=headers, data = json.dumps(payload))
        s_id = jsonpath.jsonpath(rsp.json(), '$..{name}'.format(name='id'))
        if isinstance(s_id,bool):
            return False
        else:
            return s_id[0]

if __name__ == '__main__':
    setting.host = "192.168.84.35"
    setting.database = 'AnyRobot'
    setting.password = 'eisoo.com'
    setting.port = 30006
    setting.user = 'root'
    date = search().createSearchId()
    print(date)