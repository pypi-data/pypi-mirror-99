from aishu import setting
from aishu.datafaker.profession.entity import name, switch, ip, timestamp, ml, kai, objectManager, index, agent ,id ,port
from aishu.datafaker.profession.entity import zx


def filed(key,inquire=[]):
    """
    :param key:
    :return:
    """
    SERVICE_KPI_ = {
        'AnyRobotNameID': name.date().getName,
        'AnyRobotOtherNameID': name.date().getName,
        'Closed': switch.date().getSwClosed,
        'Open': switch.date().getSwOpen,
        'UUid': id.date().getUUid,
        'IpVR': ip.date().getIpVR,
        'IPError': ip.date().getIpError,
        'startTime': timestamp.date().getStartTime,
        'endTime': timestamp.date().getEndTime,
        'lastHourTime': timestamp.date().getLastHourTime,
        'lastTime':timestamp.date().getLastTime,
        'getEtlPortOld': port.date().getEtlPortOld,
        'getEtlPortNew': port.date().getEtlPortNew,
        'getEtlPortIll': port.date().getEtlPortIll,
        'enity': ml.machine(inquire).inquire,
        'entityHost': kai.machine(inquire).inquireEntity,
        'serviceKpiId': kai.machine(inquire).inquireServiceKpi,
        'businessKpiIdAndServiceId':kai.machine(inquire).inquireBusinessKPIAndServiceId,
        'pensInfo':kai.machine(inquire).inquirePens,
        'testHostIP':ip.date().getTestHostIP,
        'rarserRuleName': objectManager.date().getRuleNameId,
        'dashboardId': objectManager.date().getDashboardId,
        'searchId': objectManager.date().getSearchId,
        'visualizationId': objectManager.date().getVisualizationId,
        'indexId':index.date().getIndexId,
        'indexList':index.date().getIndexName,
        'indexList_as':index.date().getIndexTypeAs,
        'DateTime':timestamp.date().getDateTime,
        'agentPort': agent.machine(inquire).getAgentPort,
        'intPort':agent.machine(inquire).getIntPort,
        'adminID':id.date().getAdminID,
        'DefaultLogGroupID':id.date().getDefaultLogGroupID,
        'asLogWareID':id.date().getAsLogWareID,
        'httpUrl':kai.machine(inquire).getAlertHttpUrl,
        'lastFiveYearTime':timestamp.date().getLastFiveYearTime,
        's_id': zx.search().createSearchId
    }

    switcher = SERVICE_KPI_
    if switcher.get(key) is not None:
        return switcher[key]()
    else:
        return False

if __name__ == '__main__':
    setting.host = "192.168.84.35"
    setting.database = 'AnyRobot'
    setting.password = 'eisoo.com'
    setting.port = 30006
    setting.user = 'root'
    date = filed("s_id")
    print(date)