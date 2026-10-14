"""Slim Keyboard61 prototype; mm. Downloaded models are explicitly proxies."""
from pathlib import Path
import cadquery as cq,json,re
CADROOT=Path(__file__).resolve().parent.parent
ROOT=CADROOT.parent
OUT=Path(__file__).resolve().parent; MODELS=OUT/'vendor-models';OUT.mkdir(exist_ok=True)
geo=json.loads((CADROOT/'geometry.json').read_text())
W,D=356.,112.;BOTTOM=10.5;TOP=12.1;PB=15.6;PT=1.5
def box(x,y,z,a,b,c):return cq.Workplane('XY').box(a,b,c,centered=(False,False,False)).translate((x,y,z))
def cyl(x,y,z,r,h):return cq.Workplane('XY').circle(r).extrude(h).translate((x,y,z))
def export(obj,name,stl=False):
 assert obj.val().isValid(),name
 cq.exporters.export(obj,str(OUT/(name+'.step')))
 if stl:cq.exporters.export(obj,str(OUT/(name+'.stl')),tolerance=.08,angularTolerance=.15)
base=box(0,0,0,W,D,PB).edges('|Z').fillet(3).cut(box(2.5,2.5,2,W-5,D-5,PB+1))
export(base,'02-thin-shell')
for x,y in geo['holes']:base=base.union(cyl(x,y,2,3.7,BOTTOM-2)).cut(cyl(x,y,3,1.35,BOTTOM+2))
export(base,'03-mounting-bosses')
base=base.cut(box(52,62,-1,42,24,4)).cut(box(84,76,-1,12,32,9))
base=base.cut(box(28,68,-1,20,20,4)).cut(cyl(293.5,36.5,-1,4,4))
export(base,'04-usb-access');export(base,'base',True)
plate=box(0,0,PB,W,D,PT).edges('|Z').fillet(3)
for k in geo['keys']:plate=plate.cut(box(k['x']-7.05,k['y']-7.05,PB-1,14.1,14.1,PT+2))
for x,y in geo['stabilizers']:plate=plate.cut(box(x-3.6,y-8.2,PB-1,7.2,16.4,PT+2))
for x,y in geo['holes']:plate=plate.cut(cyl(x,y,PB-1,1.65,PT+2))
export(plate,'05-switch-openings')
plate=plate.cut(cyl(327,99,PB-1,3.6,PT+2))
for x in [318,334.5]:plate=plate.union(box(x,91.8,PB-8,1.5,14.4,8))
export(plate,'06-encoder-mount')
# Portrait 2.8-inch TFT. Generic 50x86mm module envelope, verify purchased unit.
plate=plate.cut(box(304.6,17.2,PB-1,44.8,59.2,PT+2))
for x,y in [(301,6),(353,6),(301,87),(353,87)]:
 plate=plate.union(cyl(x,y,PB-5,2.1,5)).cut(cyl(x,y,PB-5.5,1.0,6))
export(plate,'07-oled-window');export(plate,'switch-plate',True)
pcb=cq.importers.importStep(str(CADROOT/'pcb-reference.step')).translate((-41.5,216.5,BOTTOM))
export(pcb,'pcb-installed')
switch=cq.importers.importStep(str(MODELS/'mx-switch-acheron.step')).rotate((0,0,0),(1,0,0),90).translate((-7.35,-7.35,4.7))
switches=cq.Assembly(name='mx-compatible-switch-proxies')
for k in geo['keys']:switches.add(switch,name=k['reference'],loc=cq.Location(cq.Vector(k['x'],k['y'],TOP)),color=cq.Color(.65,.65,.65))
switches.save(str(OUT/'08-switches-installed.step'))
# Actual recessed legends on generic keycap CAD. Purchased keycaps remain unchanged.
pcbtext=(ROOT/'keyboard61.kicad_pcb').read_text();labels={}
for block in pcbtext.split('\n\t(footprint ')[1:]:
 ref=re.search(r'\(property "Reference" "([^"]+)"',block);val=re.search(r'\(property "Value" "([^"]+)"',block)
 if ref and val:labels[ref[1]]=val[1]
units={'Backspace':2,'Tab':1.5,'Backslash':1.5,'Caps':1.75,'Enter':2.25,'LShift':2.25,'RShift':2.75,'Space':6.25,'LCtrl':1.25,'LWin':1.25,'LAlt':1.25,'RAlt':1.25,'Fn':1.25,'Menu':1.25,'RCtrl':1.25}
legendmap={'Backspace':'BACK','Backslash':'\\','Caps':'CAPS','LShift':'SHIFT','RShift':'SHIFT','LCtrl':'CTRL','RCtrl':'CTRL','LAlt':'ALT','RAlt':'ALT','LWin':'WIN','Space':'SPACE','Esc':'ESC','Tab':'TAB','Enter':'ENTER','Menu':'MENU','Fn':'FN'}
cap_solids=[]
for k in geo['keys']:
 label=labels[k['reference']];w=units.get(label,1)*19.05-1.05
 cap=cq.Workplane('XY').rect(w,18).workplane(offset=8).rect(w-3,15).loft()
 inner=cq.Workplane('XY').rect(w-2.4,15.6).workplane(offset=6.5).rect(w-5.4,12.6).loft()
 cap=cap.cut(inner).translate((k['x'],k['y'],23.5))
 legend=legendmap.get(label,label.upper());size=3.4 if len(legend)==1 else 2.2
 engraving=cq.Workplane('XY').text(legend,size,.7,font='Arial',kind='bold',halign='center',valign='center').translate((k['x'],k['y'],31.15))
 cap=cap.cut(engraving);assert cap.val().isValid(),label
 cap_solids.append(cap.val())
caps=cq.Workplane('XY').newObject([cq.Compound.makeCompound(cap_solids)])
export(caps,'09-keycaps-installed')
oled=box(302,4,PB-5,50,86,1.6).union(box(304,9,PB-3.4,46,66,3.2))
export(oled,'TFT-module-envelope')
encoder=cq.importers.importStep(str(MODELS/'alps-ec11-proxy.stp')).rotate((0,0,0),(1,0,0),180).translate((327.21,98.821,-4.7))
encoder=encoder.newObject([encoder.val().fix()])
knob=cyl(327,99,PB+3,9,13.5)
spacers=cq.Compound.makeCompound([cyl(x,y,TOP,3,3.5).cut(cyl(x,y,TOP-1,1.65,6)).val() for x,y in geo['holes']])
assembly=cq.Assembly(name='Keyboard61-slim-OLED-prototype')
for n,obj,c in [('base',base,(.12,.15,.18)),('plate',plate,(.18,.23,.27)),('pcb',pcb,(.1,.45,.2)),('keycaps',caps,(.83,.86,.88)),('TFT-module-envelope',oled,(.03,.06,.09)),('encoder-ALPS-proxy',encoder,(.65,.65,.65)),('knob-reference',knob,(.1,.1,.1)),('plate-spacers',spacers,(.65,.65,.65))]:assembly.add(obj,name=n,color=cq.Color(*c))
assembly.add(switches)
assembly.save(str(OUT/'keyboard61-slim-assembly.step'))
export(oled,'oled-positioned');export(encoder,'encoder-positioned')
metrics={'old_case_height_mm':27.6,'new_case_height_mm':17.1,'reduction_percent':38.04,'outside_mm':[W,D,17.1],'keycap_reference_top_mm':31.5,'pcb_bottom_mm':10.5,'PCB_top_mm':12.1,'plate_bottom_mm':15.6,'floor_mm':2,'Pico_model_floor_clearance_mm':1.9555,'controller_mount':'Direct-solder existing Pico H headers; no 8.5mm female sockets. Trim exposed header tails flush after soldering; trial fit required.','display_candidate':'ShillehTek AA317 2.8-inch ILI9341 SPI TFT, $10.99 before tax/shipping, checked 2026-10-13. User relaxed original $8 cap.','display_window_mm':[44.8,59.2],'display_window_bottom_buffer_mm':17.2,'display_window_knob_buffer_mm':13.6,'prototype_limitations':['MX model is generic, not Gateron Milky Yellow Pro V2','TFT envelope is modeled from vendor dimensions, not downloaded exact CAD','Encoder model is ALPS EC11 proxy, not Adafruit 377','Keycaps are generic envelopes, not selected XVX OEM','WS stabilizer exact CAD unavailable; existing clearance references retained','Actual Tab/Q Pico-pin interference and switch travel unverified','Printing must be requoted; old $19.61 quote does not apply']}
(OUT/'model-checks.json').write_text(json.dumps(metrics,indent=2))
print(json.dumps(metrics,indent=2))
