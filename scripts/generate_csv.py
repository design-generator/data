"""Read result files from result folder and save them to res.csv file."""
import os
import json

# inputs as key and possible values
inputs = (
    {"name": "Area", "min": 1250, "max": 5000, "from": 1250, "step": 3750},
    {"name": "Aspect_Ratio", "min": 1, "max": 1.5, "from": 1, "step": .5},
    {"name": "Height", "min": 4, "max": 4, "from": 4, "step": 4},
    {"name": "Offset", "min": 4, "max": 4, "from": 4, "step": 0},
    {"name": "FloorCount", "min": 1, "max": 4, "from": 1, "step": 4},
    {"name": "Orientation", "min": 0, "max": 0, "from": 0, "step": 0},
    {"name": "Window_Wall_Ratio", "min": 30, "max": 50, "from": 30, "step": 20},
    {"name": "Window_Height", "min": 2, "max": 2, "from": 2, "step": 0},
    {"name": "Sill_Height", "min": 0.7, "max": 0.7, "from": 0.7, "step": 0},
    {"name": "Shading_depth", "min": 0, "max": 1, "from": 1, "step": 1},
    {"name": "Infiltration", "min": 0.0001, "max": 0.0003, "from": 0.0001, "step": 0.0001},
    {"name": "R_value_Wall", "min": 2.6, "max": 7, "from": 2.6, "step": 4.4},
    {"name": "R_value_Roof", "min": 3.5, "max": 7, "from": 3.5, "step": 3.5},
    {"name": "Glazing_Type", "min": 0, "max": 1, "from": 0, "step": 1},
    {"name": "Outside_Air_Core", "min": 0.06, "max": 0.06, "from": 0.06, "step": 0},
    {"name": "Outside_Air_Perimeter", "min": 0.06, "max": 0.3, "from": 0.06, "step": 0.24},
    {"name": "Internal_Load_Core", "min": 1, "max": 1, "from": 1, "step": 1},
    {"name": "Internal_Load_Perimeter", "min": 1, "max": 1, "from": 1, "step": 0},
    {"name": "Comfort_Range", "min": 0.06, "max": 0.06, "from": 0.06, "step": 0},
    {"name": "HVAC_Systems", "min": 0, "max": 3, "from": 0, "step": 1}
)

outputs = (u'unmet_cooling_hours', u'eui', u'lighting_power_density', u'daylight_factor', u'heating', u'unmet_heating_hours', u'cooling')

def frange(start, stop, step):
    """Range function for float values."""
    if step == 0:
        return [start]

    if isinstance(step, int):
        return range(start, stop, step)

    v = start
    vs = []
    while v < stop:
        vs.append(v)
        v += step
    return vs

for i in inputs:
    print frange(i['min'], i['max'] + i['step'], i['step'])
# for f in os.listdir('../res'):
#     # find input values based on file name
#     for s in f:
#         print s
#
#     with open(os.path.join('../res', f)) as jf:
#         j = json.load(jf)
#         for o in outputs:
#             # read the output Value
#             print j[o]

# write the results as a csv file
