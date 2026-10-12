"""Desktop software checks; no physical encoder or USB device is exercised."""
from pathlib import Path
import sys,types,ast,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'firmware'))
sys.modules['busio']=types.SimpleNamespace(I2C=type('I2C',(),{}))
sys.modules['digitalio']=types.SimpleNamespace(Pull=types.SimpleNamespace(UP=1,DOWN=2))
sys.modules['supervisor']=types.SimpleNamespace(ticks_ms=lambda:100)
sys.modules['kmk.utils']=types.SimpleNamespace(Debug=lambda name:lambda *args:None)
sys.modules['micropython']=types.SimpleNamespace(const=lambda x:x)
from kmk.modules.encoder import BaseEncoder
class Pin:
 def __init__(self):self.value=True
 def get_value(self):return self.value
class SimEncoder(BaseEncoder):
 def button_event(self):pass
def rotation(states):
 e=SimEncoder();e.pin_a=Pin();e.pin_b=Pin();e._state=e._start_state=(True,True);e.divisor=4;events=[];e.on_move_do=lambda s:events.append(s['direction'])
 for a,b in states:e.pin_a.value=a;e.pin_b.value=b;e.update_state()
 return events
assert rotation([(0,1),(0,0),(1,0),(1,1)])==[1]
assert rotation([(1,0),(0,0),(0,1),(1,1)])==[-1]
assert rotation([(0,1),(1,1)])==[]
code=(ROOT/'firmware/code.py').read_text();tree=ast.parse(code)
for filename in ['code.py','boot.py']:compile((ROOT/'firmware'/filename).read_text(),filename,'exec')
assert 'board.GP19, board.GP20, board.GP21' in code
assert code.count('((KC.VOLD, KC.VOLU, KC.MUTE),)')==2
assert 'usb_hid.Device.CONSUMER_CONTROL' in (ROOT/'firmware/boot.py').read_text()
class ConfigKeyboard:
 def __init__(self):self.modules=[];self.extensions=[]
sys.modules['kmk.kmk_keyboard']=types.SimpleNamespace(KMKKeyboard=ConfigKeyboard)
sys.modules['board']=types.SimpleNamespace(**{f'GP{i}':i for i in range(29)})
cfg={'__name__':'configuration_test'};exec(compile(code,'code.py','exec'),cfg)
assert cfg['keyboard'].modules[-1].pins==((19,20,21,False,4),)
assert [k.code for k in cfg['encoder_handler'].map[0][0]]==[0xEA,0xE9,0xE2]
print(json.dumps({'clockwise_transition_sequence':'pass','counterclockwise_transition_sequence':'pass','partial_detent_reversal':'pass','both_layer_volume_maps':'pass','consumer_control_enabled':'pass','hardware_tested':False},indent=2))
