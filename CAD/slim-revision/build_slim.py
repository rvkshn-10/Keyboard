"""Slim Keyboard61 prototype; mm. Downloaded models are explicitly proxies."""
from pathlib import Path
import cadquery as cq,json,re,math
CADROOT=Path(__file__).resolve().parent.parent
ROOT=CADROOT.parent
OUT=Path(__file__).resolve().parent; MODELS=OUT/'vendor-models';OUT.mkdir(exist_ok=True)
geo=json.loads((CADROOT/'geometry.json').read_text())
W,D=356.,112.;BOTTOM=10.5;TOP=12.1;PB=15.6;PT=1.5
TFT_X,TFT_Y=302.,4.
TFT_BOARD_BOTTOM,TFT_BOARD_T,TFT_FACE_TOP=11.3,1.6,16.9
TFT_HOLES=[(305.,9.),(349.,9.),(305.,85.),(349.,85.)]
MX_CROSS,MX_ARM,MX_DEPTH=4.1,1.17,3.8
MX_CLEARANCE=.10
def box(x,y,z,a,b,c):return cq.Workplane('XY').box(a,b,c,centered=(False,False,False)).translate((x,y,z))
def cyl(x,y,z,r,h):return cq.Workplane('XY').circle(r).extrude(h).translate((x,y,z))
def export(obj,name,stl=False):
 assert obj.val().isValid(),name
 cq.exporters.export(obj,str(OUT/(name+'.step')))
 if stl:cq.exporters.export(obj,str(OUT/(name+'.stl')),tolerance=.08,angularTolerance=.15)
base=box(0,0,0,W,D,PB).edges('|Z').fillet(3).cut(box(2.5,2.5,2,W-5,D-5,PB+1))
for x,y in TFT_HOLES:
 base=base.union(cyl(x,y,2,3.,TFT_BOARD_BOTTOM-2)).cut(cyl(x,y,2,1.1,TFT_BOARD_BOTTOM-1.8))
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
# AA317 portrait module from its dimension drawing: 50x86 PCB, 44x76 hole pitch,
# 14-pin display header at the lower edge. Display face is set 0.2mm below plate top.
plate=plate.cut(box(304.6,17.2,PB-1,44.8,59.2,PT+2))
for x,y in TFT_HOLES:
 plate=plate.cut(cyl(x,y,PB-0.9,1.6,PT+1)).cut(cyl(x,y,PB+PT-0.9,2.75,.95))
export(plate,'07-tft-fit');export(plate,'switch-plate',True)
pcb=cq.importers.importStep(str(CADROOT/'pcb-reference.step')).translate((-41.5,216.5,BOTTOM))
export(pcb,'pcb-installed')
switch=cq.importers.importStep(str(MODELS/'mx-switch-acheron.step')).rotate((0,0,0),(1,0,0),90).translate((-7.35,-7.35,4.7))
switches=cq.Assembly(name='mx-compatible-switch-proxies')
for k in geo['keys']:switches.add(switch,name=k['reference'],loc=cq.Location(cq.Vector(k['x'],k['y'],TOP)),color=cq.Color(.65,.65,.65))
switches.save(str(OUT/'08-switches-installed.step'))
# Printable MX-compatible keycaps: engraved legends, internal hollow, central MX socket,
# and two stabilizer sockets where the keyboard layout uses stabilizers.
pcbtext=(ROOT/'keyboard61.kicad_pcb').read_text();labels={}
for block in pcbtext.split('\n\t(footprint ')[1:]:
 ref=re.search(r'\(property "Reference" "([^"]+)"',block);val=re.search(r'\(property "Value" "([^"]+)"',block)
 if ref and val:labels[ref[1]]=val[1]
units={'Backspace':2,'Tab':1.5,'Backslash':1.5,'Caps':1.75,'Enter':2.25,'LShift':2.25,'RShift':2.75,'Space':6.25,'LCtrl':1.25,'LWin':1.25,'LAlt':1.25,'RAlt':1.25,'Fn':1.25,'Menu':1.25,'RCtrl':1.25}
legendmap={'Backspace':'BACK','Backslash':'\\','Caps':'CAPS','LShift':'SHIFT','RShift':'SHIFT','LCtrl':'CTRL','RCtrl':'CTRL','LAlt':'ALT','RAlt':'ALT','LWin':'WIN','Space':'SPACE','Esc':'ESC','Tab':'TAB','Enter':'ENTER','Menu':'MENU','Fn':'FN'}
def cross_cut(x,y,z,depth,clearance):
 total=MX_CROSS+2*clearance; arm=MX_ARM+2*clearance
 a=box(x-total/2,y-arm/2,z,total,arm,depth)
 b=box(x-arm/2,y-total/2,z,arm,total,depth)
 return a.union(b)
stabilizer_pairs={}
for sx,sy in geo['stabilizers']:
 stabilizer_pairs.setdefault(round(sy,3),[]).append((sx,sy))
cap_solids=[]
socket_report=[]
for k in geo['keys']:
 label=labels[k['reference']];w=units.get(label,1)*19.05-1.05
 cap=cq.Workplane('XY').rect(w,18).workplane(offset=8).rect(w-3,15).loft()
 inner=cq.Workplane('XY').rect(w-2.4,15.6).workplane(offset=6.5).rect(w-5.4,12.6).loft()
 cap=cap.cut(inner)
 # 5.5mm boss carries the cross socket; keep 1.5mm continuous roof above it.
 cap=cap.union(cyl(0,0,2.7,2.75,3.8)).cut(cross_cut(0,0,2.7,3.8,MX_CLEARANCE))
 if units.get(label,1)>1.25:
  same_row=stabilizer_pairs.get(round(k['y']-.62,3),[])
  for sx,sy in same_row:
   if abs(((sx-k['x'])*2))<units.get(label,1)*19.05:
    dx,dy=sx-k['x'],sy-k['y']
    cap=cap.union(cyl(dx,dy,2.7,2.75,3.8)).cut(cross_cut(dx,dy,2.7,3.8,MX_CLEARANCE))
    socket_report.append({'key':label,'offset_mm':[round(dx,4),round(dy,4)]})
 cap=cap.translate((k['x'],k['y'],23.5))
 legend=legendmap.get(label,label.upper());size=3.4 if len(legend)==1 else 2.2
 engraving=cq.Workplane('XY').text(legend,size,.7,font='Arial',kind='bold',halign='center',valign='center').translate((k['x'],k['y'],31.15))
 cap=cap.cut(engraving);assert cap.val().isValid(),label
 cap_solids.append(cap.val())
caps=cq.Workplane('XY').newObject([cq.Compound.makeCompound(cap_solids)])
export(caps,'09-keycaps-installed')
# Printable tolerance coupon: three cross sockets allow a real switch to choose print clearance.
gauge=box(0,0,0,42,14,6)
for i,clearance in enumerate((0,.10,.20)):
 x=7.+i*14
 gauge=gauge.cut(cross_cut(x,7,2.2,3.8,clearance))
 text=cq.Workplane('XY').text(f'{clearance:.2f}',2.2,.5,font='Arial',kind='bold',halign='center',valign='center').translate((x,7,5.5))
 gauge=gauge.cut(text)
export(gauge,'mx-stem-fit-gauge',True)
# AA317 model assembled from its manufacturer drawing: board, front touch stack, active area,
# and 14-pin header protrusion. Header-tip clearance to the case floor is 2.12mm in this model.
board=box(TFT_X,TFT_Y,TFT_BOARD_BOTTOM,50,86,TFT_BOARD_T)
for x,y in TFT_HOLES: board=board.cut(cyl(x,y,TFT_BOARD_BOTTOM-.1,1.6,TFT_BOARD_T+.2))
panel_y=TFT_Y+(86-69.2)/2
panel=box(TFT_X,panel_y,TFT_BOARD_BOTTOM+TFT_BOARD_T,50,69.2,TFT_FACE_TOP-(TFT_BOARD_BOTTOM+TFT_BOARD_T))
active=box(TFT_X+3.4,panel_y+5.8,TFT_FACE_TOP,43.2,57.6,.05)
header=[]
for i in range(14):
 x=TFT_X+8.49+i*2.54
 header.append(box(x-.4,TFT_Y+1.3,4.12,.8,.8,TFT_BOARD_BOTTOM-4.12))
tft=board.union(panel).union(active)
for pin in header:tft=tft.union(pin)
export(tft,'TFT-module-envelope')
encoder=cq.importers.importStep(str(MODELS/'alps-ec11-proxy.stp')).rotate((0,0,0),(1,0,0),180).translate((327.21,98.821,-4.7))
encoder=encoder.newObject([encoder.val().fix()])
# Functional printed knob for the Adafruit 377 / Bourns PEC11 encoder. The
# shaft is a 6 mm D-shaft; this prototype socket uses a small FDM clearance.
# The knob sits just above the plate and has a 14.8 mm deep shaft socket,
# enough engagement to rotate and to follow the encoder shaft when pressed.
knob_z=PB+PT+0.8
knob=(cq.Workplane('XY').circle(9).extrude(1.35)
      .union(cq.Workplane('XY').workplane(offset=1.35).circle(8.2)
             .workplane(offset=15.65).circle(8.55).loft()))
# 24 short grip flutes, kept shallow to leave a durable wall around the socket.
for i in range(24):
    a=2*math.pi*i/24
    gx,gy=8.52*math.cos(a),8.52*math.sin(a)
    groove=cq.Workplane('XY').center(gx,gy).circle(.42).extrude(16.2).translate((0,0,.7))
    knob=knob.cut(groove)
# D socket: 6.2 mm round portion with the flat 2.3 mm from center.
# This matches the encoder's nominal 6 mm shaft while allowing print clearance.
d_bore=cq.Workplane('XY').circle(3.1).extrude(14.4)
d_cut=cq.Workplane('XY').box(20,10,14.4,centered=(True,False,False)).translate((0,2.3,0))
knob=knob.cut(d_bore.cut(d_cut))
# Recessed arrow on top marks the volume-up direction; button press is axial.
arrow=(cq.Workplane('XY').polyline([(-.42,1.2),(.42,1.2),(.42,5.1),(1.35,5.1),
                                    (0,7.0),(-1.35,5.1),(-.42,5.1)])
       .close().extrude(.45).translate((0,0,16.55)))
knob=knob.cut(arrow)
assert knob.val().isValid(), 'functional rotary knob'
export(knob,'functional-volume-knob',True)
knob=knob.translate((327,99,knob_z))
spacers=cq.Compound.makeCompound([cyl(x,y,TOP,3,3.5).cut(cyl(x,y,TOP-1,1.65,6)).val() for x,y in geo['holes']])
assembly=cq.Assembly(name='Keyboard61-slim-TFT-prototype')
for n,obj,c in [('base',base,(.12,.15,.18)),('plate',plate,(.18,.23,.27)),('pcb',pcb,(.1,.45,.2)),('keycaps',caps,(.83,.86,.88)),('TFT-AA317-envelope',tft,(.03,.06,.09)),('encoder-ALPS-proxy',encoder,(.65,.65,.65)),('functional-volume-knob',knob,(.1,.1,.1)),('plate-spacers',spacers,(.65,.65,.65))]:assembly.add(obj,name=n,color=cq.Color(*c))
assembly.add(switches)
assembly.save(str(OUT/'keyboard61-slim-assembly.step'))
export(tft,'tft-aa317-positioned');export(encoder,'encoder-positioned')
metrics={'old_case_height_mm':27.6,'new_case_height_mm':17.1,'reduction_percent':38.04,'outside_mm':[W,D,17.1],'keycap_reference_top_mm':31.5,'pcb_bottom_mm':10.5,'PCB_top_mm':12.1,'plate_bottom_mm':15.6,'floor_mm':2,'Pico_model_floor_clearance_mm':1.9555,'controller_mount':'Direct-solder existing Pico H headers; no 8.5mm female sockets. Trim exposed header tails flush after soldering; trial fit required.','display_candidate':'ShillehTek AA317 2.8-inch ILI9341 SPI TFT, $10.99 before tax/shipping, checked 2026-10-13.','display_board_mm':[50,86,1.6],'display_hole_pitch_mm':[44,76],'display_hole_centers_mm':TFT_HOLES,'display_face_top_mm':TFT_FACE_TOP,'display_header_tip_z_mm':4.12,'display_header_to_floor_clearance_mm':2.12,'display_window_mm':[44.8,59.2],'display_active_area_mm':[43.2,57.6],'display_window_bottom_buffer_mm':17.2,'display_window_knob_buffer_mm':13.6,'encoder_knob':{'shaft_type':'6 mm D-shaft, Adafruit 377 / Bourns PEC11','socket_diameter_mm':6.2,'socket_flat_offset_mm':2.3,'socket_depth_mm':14.4,'knob_bottom_gap_mm':0.8,'encoder_switch_travel_mm':0.5,'knob_max_diameter_mm':18,'knob_height_mm':17.0,'grip_flutes':24,'function':'turn volume; axial push engages encoder switch for mute','fit_status':'CAD designed to nominal shaft dimensions; print fit and button travel not physically verified'},'mx_socket_nominal_mm':{'cross':MX_CROSS,'arm_width':MX_ARM,'depth':MX_DEPTH,'fit_clearance_each_side':MX_CLEARANCE},'mx_stabilizer_socket_count':len(socket_report),'stabilizer_socket_positions':socket_report,'keycap_count':len(cap_solids),'prototype_limitations':['TFT model comes from manufacturer dimensional drawing, not delivered-part inspection','TFT header is modeled with a 2.12mm nominal floor gap; print tolerance and actual pin orientation unverified','MX sockets use nominal Cherry dimensions plus 0.10mm per-side print clearance; print the 3-size gauge and test actual Gateron switches','MX model is generic, not Gateron Milky Yellow Pro V2','Encoder model is ALPS EC11 proxy, not Adafruit 377','Knob socket uses nominal D-shaft dimensions and still needs a printed fit/button-travel test','Keycap outer envelopes remain generic and need shape/feel testing','WS stabilizer exact CAD unavailable; actual installed stabilizer compatibility unverified','Actual Tab/Q Pico-pin interference and switch travel unverified','Printing must be requoted; old $19.61 quote does not apply']}
(OUT/'model-checks.json').write_text(json.dumps(metrics,indent=2))
print(json.dumps(metrics,indent=2))
