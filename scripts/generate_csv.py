"""Read result files from result folder and save them to res.csv file."""
import os
import json


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

# inputs as key and possible values
inputs = (
    {'id': 1, "name": "FloorCount", "min": 1, "max": 4, "from": 1, "step": 4},
    {'id':2, "name": "Area", "min": 1250, "max": 5000, "from": 1250, "step": 3750},
    {'id': 3, "name": "Aspect_Ratio", "min": 1, "max": 1.5, "from": 1, "step": .5},
    {'id': 4, "name": "Offset", "min": 4, "max": 4, "from": 4, "step": 0},
    {'id': 5, "name": "Orientation", "min": 0, "max": 0, "from": 0, "step": 0},
    {'id': 6, "name": "Height", "min": 4, "max": 4, "from": 4, "step": 4},
    {'id': 7, "name": "Window_Wall_Ratio", "min": 30, "max": 50, "from": 30, "step": 20},
    {'id': 8, "name": "Window_Height", "min": 2, "max": 2, "from": 2, "step": 0},
    {'id': 9, "name": "Sill_Height", "min": 0.7, "max": 0.7, "from": 0.7, "step": 0},
    {'id': 10, "name": "Infiltration", "min": 0.0001, "max": 0.0004, "from": 0.0001, "step": 0.0001}, #max is actually 0.0003
    {'id': 11, "name": "R_value_Wall", "min": 2.6, "max": 7, "from": 2.6, "step": 4.4},
    {'id': 12, "name": "R_value_Roof", "min": 3.5, "max": 7, "from": 3.5, "step": 3.5},
    {'id': 13, "name": "Glazing_Type", "min": 0, "max": 1, "from": 0, "step": 1},
    {'id': 14, "name": "Shading_depth", "min": 0, "max": 1, "from": 1, "step": 1},
    {'id': 15, "name": "Outside_Air_Core", "min": 0.06, "max": 0.06, "from": 0.06, "step": 0},
    {'id': 16, "name": "Outside_Air_Perimeter", "min": 0.06, "max": 0.3, "from": 0.06, "step": 0.24},
    {'id': 17, "name": "Internal_Load_Core", "min": 1, "max": 1, "from": 1, "step": 1},
    {'id': 18, "name": "Internal_Load_Perimeter", "min": 1, "max": 1, "from": 1, "step": 0},
    {'id': 18, "name": "Comfort_Range", "min": 0.06, "max": 0.06, "from": 0.06, "step": 0},
    {'id': 20, "name": "HVAC_Systems", "min": 0, "max": 3, "from": 0, "step": 1}
)

outputs = (u'unmet_cooling_hours', u'eui', u'lighting_power_density',
           u'daylight_factor', u'heating', u'unmet_heating_hours', u'cooling')

content = [','.join('in:%s' % inp['name'] for inp in inputs) + ',' + \
         ','.join('out:%s' % out for out in outputs)]

for inp in inputs:
    inp['values'] = frange(inp['min'], inp['max'] + inp['step'], inp['step'])

def get_input_values(inp, index):
    try:
        return str(inp['values'][int(index)])
    except IndexError:
        print 'Bug: ', index, inp['name'], inp['values']
        return str(inp['values'][-1])

for f in os.listdir('../res'):
    # find input values based on file name
    v = ','.join(get_input_values(inp, f[count]) for count, inp in enumerate(inputs))

    with open(os.path.join('../res', f)) as jf:
        d = json.load(jf)
        o = ','.join(str(d[ot]) for ot in outputs)

    content.append(','.join((v, o)))

# # write the results as a csv file
with open('results.csv', 'wb') as csvfile:
    csvfile.write('\n'.join(content))
