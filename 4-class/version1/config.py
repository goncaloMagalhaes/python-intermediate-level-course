# 10. -> create file, configparser, then configs.conf, then listener configs, then 11. (Listener.get_command_from_file())
# 12. -> tire configs, then 13. (create monitor.py)

import configparser


config_file = 'configs.conf'
config = configparser.ConfigParser()
config.read(config_file)

COMMAND_FILE = config['Listener']['CommandFile']
SECONDS_PER_FILE_READ = float(config['Listener']['SecondsPerFileRead'])

TIRE_INITIAL_LIFE_PERCENTAGE = float(config['Tire']['InitialLifePercentage'])
TIRE_RADIUS_METERS = float(config['Tire']['RadiusMeters'])
TIRE_CYCLES_PER_1PERCENT_DISCOUNT = int(
    config['Tire']['CyclesPer1PercentDiscount'])

CONTROLLER_SECONDS_PER_CYCLE = float(config['Controller']['SecondsPerCycle'])

GRAPH_MIN_X = int(config['Monitor']['GraphMinX'])
GRAPH_MAX_X = int(config['Monitor']['GraphMaxX'])
GRAPH_MIN_Y = int(config['Monitor']['GraphMinY'])
GRAPH_MAX_Y = int(config['Monitor']['GraphMaxY'])
X_PER_SPACE = int(config['Monitor']['XPerSpace'])
Y_PER_LINE = int(config['Monitor']['YPerLine'])
