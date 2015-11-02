from Products.DataCollector.plugins.CollectorPlugin import (SnmpPlugin, GetTableMap)

__doc__ = """ OceanStorControllerMap
Models controller details for Huawei OceanStor storage systems
"""

class OceanStorControllerMap(SnmpPlugin):
    relname = 'oceanStorControllers'
    modname = 'ZenPacks.community.HuaweiOceanStor.OceanStorController'

    snmpGetTableMaps = (
        GetTableMap(
            'hwInfoControllerTable', '.1.3.6.1.4.1.34774.4.1.23.5.2.1', {
                '.2':'hwInfoControllerHealthStatus',
                '.3':'hwInfoControllerRunningStatus',
                '.5':'hwInfoControllerLocation',
                '.6':'hwInfoControllerRole',
                '.7':'hwInfoControllerCacheCapacity',
                }
        ),
    )
     
    def process(self, device, results, log):
        log.info('processing %s for device %s', self.name(), device.id)
 
        controllerinfo = results[1].get('hwInfoControllerTable', {})

        rm = self.relMap()
        for snmpindex, row in controllerinfo.items():
            # do check for no data?
        
            name = row.get('hwInfoControllerLocation')
            log.info('Controller %s  %s', name, snmpindex)
            rm.append(self.objectMap({
                'id': self.prepId(name),
                'title': name,
                'snmpindex': snmpindex.strip('.'),
                'controllerhealth': row.get('hwInfoControllerHealthStatus'),  #convert to text?
                'controllerstatus': row.get('hwInfoControllerRunningStatus'),  #convert to text?
                'controllerrole': row.get('hwInfoControllerRole'), # Convert to text?
                'controllercache': row.get('hwInfoControllerCacheCapacity'),
                }))

            return rm
