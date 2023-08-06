from aishu import setting
def sql(key):
    """
    对应数据服务的sql语句注册
    :param key:
    :return:
    """
    switcher = {
        'UserID':{'sql':'select userId from User where loginName = "admin";','database':'AnyRobot'},
        'MLID': {'sql': "select id from MLJob ;", 'database': 'AnyRobotML'},
        'entityID': {'sql': "select id from KAIEntity;", 'database': 'AnyRobot'},
        'groupID': {'sql': "select id from KAIEntityGroup;", 'database': 'AnyRobot'},
        'AlertRuleID': {'sql': "select id from RuleEngineAlert;", 'database': 'AnyRobot'},
        'kpiID': {'sql': "select id from KAIKpi;", 'database': 'AnyRobot'},
        'LogTypeID': {'sql': "select dataType from LogWareHouse;", 'database': 'AnyRobot'},
        'AddEntityID': {'sql': "select entityId from KAIEntityCondition where conditionValues = '192.168.84.26' AND conditionKeys = 'host';",'database': 'AnyRobot'},
        'KpiTemplateID': {'sql': "select id from KAIKpiTemplate;", 'database': 'AnyRobot'},
        'KpiTemplateID1': {'sql': "select id from KAIKpiTemplate;", 'database': 'AnyRobot'},
        'KpiTemplateID2': {'sql': "select id from KAIKpiTemplate;", 'database': 'AnyRobot'},
        'LogwareHouse': {'sql': "SELECT id From LogWareHouse where LENGTH(id)!=8;", 'database': 'AnyRobot'},
        'dataType': {'sql': "SELECT dataType From LogWareHouse where LENGTH(id)!=8;", 'database': 'AnyRobot'},
        'indexID': {'sql': "SELECT id From IndexParams;", 'database': 'AnyRobot'},
        'indexName': {'sql': "SELECT indexName From IndexParams;", 'database': 'AnyRobot'},
        'StreamId': {'sql': "SELECT name From DataStream;", 'database': 'AnyRobot'},
        'LogGroupIdPare': {'sql': 'SELECT groupId From LogGroup where GroupName="所有日志";', 'database': 'AnyRobot'},
        'RoleId': {'sql': 'SELECT roleId From Role where roleName ="admin";', 'database': 'AnyRobot'},
        'tagGroupID': {'sql': "SELECT id From TagGroup;", 'database': 'AnyRobot'},
        'tagID': {'sql': "SELECT id From Tag;", 'database': 'AnyRobot'}

    }

    if switcher.get(key) is not None:
        if switcher[key].get('database') is not None:
            if len(switcher[key]['database']) == 0:
                setting.database = 'AnyRobot'
            else:
                setting.database = switcher[key]['database']

        return switcher[key]['sql']
    else:
        return False
