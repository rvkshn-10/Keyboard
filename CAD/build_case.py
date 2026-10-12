"""Keyboard61 case prototype, millimetres. Requires cadquery==2.8.0."""
from pathlib import Path
import cadquery as cq,json
HERE=Path(__file__).resolve().parent
OUT=HERE;OUT.mkdir(exist_ok=True)
geo=json.loads((HERE/'geometry.json').read_text())
W,D=333.0,107.0
FLOOR,WALL=3.0,3.0
PCB_BOTTOM=21.0
PLATE_BOTTOM,PLATE_THICK=26.1,1.5
KNOB_X,KNOB_Y=315.,91.
SPLIT=166.5
def box(x,y,z,dx,dy,dz):
 return cq.Workplane('XY').box(dx,dy,dz,centered=(False,False,False)).translate((x,y,z))
def cyl(x,y,z,r,h):
 return cq.Workplane('XY').circle(r).extrude(h).translate((x,y,z))
base=box(0,0,0,W,D,PLATE_BOTTOM).edges('|Z').fillet(3)
base=base.cut(box(WALL,WALL,FLOOR,W-2*WALL,D-2*WALL,PLATE_BOTTOM))
for x,y in geo['holes']:
 boss=cyl(x,y,FLOOR,3.7,PCB_BOTTOM-FLOOR)
 base=base.union(boss).cut(cyl(x,y,4,1.35,PCB_BOTTOM+1))
# Two floor straps join halves using four M3 through bolts and nuts.
for y in [10.,97.]:
 for x in [SPLIT-8,SPLIT+8]:base=base.cut(cyl(x,y,-1,1.65,6))
# Accessible underside Pico USB pocket and rear cable exit.
base=base.cut(box(52,62,-1,42,24,5))
base=base.cut(box(84,76,-1,12,32,16))
# Dedicated BOOTSEL and reset access apertures. These are prototype fit allowances.
base=base.cut(box(28,68,-1,20,20,5))
base=base.cut(cyl(293.5,36.5,-1,4,5))
plate=box(0,0,PLATE_BOTTOM,W,D,PLATE_THICK).edges('|Z').fillet(3)
for k in geo['keys']:
 plate=plate.cut(box(k['x']-7.05,k['y']-7.05,PLATE_BOTTOM-1,14.1,14.1,PLATE_THICK+2))
for x,y in geo['stabilizers']:
 plate=plate.cut(box(x-3.6,y-8.2,PLATE_BOTTOM-1,7.2,16.4,PLATE_THICK+2))
for x,y in geo['holes']:plate=plate.cut(cyl(x,y,PLATE_BOTTOM-1,1.65,PLATE_THICK+2))
plate=plate.cut(cyl(KNOB_X,KNOB_Y,PLATE_BOTTOM-1,3.6,PLATE_THICK+2))
# Encoder anti-rotation support walls extend from underside of plate.
for x in [KNOB_X-9,KNOB_X+7.5]:
 plate=plate.union(box(x,KNOB_Y-7.2,PLATE_BOTTOM-8,1.5,14.4,8))
strap=box(-14,-7,0,28,14,3)
for x in [-8,8]:strap=strap.cut(cyl(x,0,-1,1.65,5))
parts={'base':base,'switch-plate':plate,'join-strap':strap}
stats={}
for name,obj in parts.items():
 assert obj.val().isValid(),name
 assert len(obj.solids().vals())==1,(name,len(obj.solids().vals()))
 cq.exporters.export(obj,str(OUT/(name+'.step')))
 cq.exporters.export(obj.translate((0,0,-PLATE_BOTTOM if name=='switch-plate' else 0)),str(OUT/(name+'.stl')),tolerance=.08,angularTolerance=.1)
 stats[name]={'volume_mm3':obj.val().Volume(),'solid_count':len(obj.solids().vals())}
for name,obj in [('base',base),('switch-plate',plate)]:
 for side,x,dx in [('left',-1,SPLIT+1),('right',SPLIT,W-SPLIT+1)]:
  half=obj.intersect(box(x,-1,-1,dx,D+2,PLATE_BOTTOM+PLATE_THICK+3))
  assert half.val().isValid()
  cq.exporters.export(half.translate((-SPLIT if side=='right' else 0,0,-PLATE_BOTTOM if name=='switch-plate' else 0)),str(OUT/f'{name}-{side}.stl'),tolerance=.08,angularTolerance=.1)
# Spacer maintains 3.5mm gap from PCB top to switch-plate underside.
spacer=cyl(0,0,0,3,3.5).cut(cyl(0,0,-1,1.65,6))
cq.exporters.export(spacer,str(OUT/'plate-spacer.stl'))
knob_ref=cyl(KNOB_X,KNOB_Y,PLATE_BOTTOM+PLATE_THICK+2,9,13)
encoder_ref=box(KNOB_X-6.25,KNOB_Y-7,PLATE_BOTTOM-10,12.5,14,10).union(cyl(KNOB_X,KNOB_Y,PLATE_BOTTOM,3,15))
assy=cq.Assembly(name='Keyboard61-case-prototype')
assy.add(base,name='base',color=cq.Color(.15,.19,.23))
assy.add(plate,name='switch-plate',color=cq.Color(.28,.35,.4))
assy.add(knob_ref,name='knob-envelope-reference',color=cq.Color(.12,.12,.12))
assy.add(encoder_ref,name='encoder-envelope-reference',color=cq.Color(.7,.7,.7))
pcb_ref=box(3.5,3.5,21,295,100,1.6)
assy.add(pcb_ref,name='PCB-envelope-reference',color=cq.Color(.08,.45,.2))
assy.save(str(OUT/'keyboard61-enclosure.step'))
# Lightweight STL of case only for rendering. References are not print parts.
cq.exporters.export(cq.Compound.makeCompound([base.val(),plate.val(),knob_ref.val()]),str(OUT/'case-preview.stl'),tolerance=.1)
volume=base.val().Volume()+plate.val().Volume()+2*strap.val().Volume()+4*spacer.val().Volume()
stats.update({'case_dimensions_mm':[W,D,PLATE_BOTTOM+PLATE_THICK],'switch_openings':len(geo['keys']),'stabilizer_clearances':len(geo['stabilizers']),'pcb_bottom_z_mm':PCB_BOTTOM,'pcb_top_z_mm':22.6,'plate_bottom_z_mm':PLATE_BOTTOM,'panel_encoder_hole_diameter_mm':7.2,'printed_volume_mm3':volume,'solid_PLA_mass_g':volume/1000*1.24,'PLA_mass_with_15pct_allowance_g':volume/1000*1.24*1.15,'cost_at_20_USD_per_kg':volume/1000*1.24*1.15*.02,'cost_at_25_USD_per_kg':volume/1000*1.24*1.15*.025,'status':'Prototype: actual switch, stabilizer, encoder, plug, pin and print tolerances require fit checks. Reference bodies are envelopes, not manufacturer models.'})
(OUT/'model-checks.json').write_text(json.dumps(stats,indent=2))
print(json.dumps(stats,indent=2))
