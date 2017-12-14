import soco

for zone in soco.discover():
    print('zone: {0} , ip: {1}'.format(zone.player_name, zone.ip_address))
