from pathlib import Path
import cadquery as cq,json,re
R=Path(__file__).resolve().parents[2];O=R/'outputs/CAD/keycap-references';O.mkdir(exist_ok=True)
geo=json.loads((R/'outputs/CAD/geometry.json').read_text())
text=(R/'work/github-keyboard/keyboard61.kicad_pcb').read_text()
labels={}
for block in text.split('\n\t(footprint ')[1:]:
 ref=re.search(r'\(property "Reference" "([^"]+)"',block)
 val=re.search(r'\(property "Value" "([^"]+)"',block)
 if ref and val:labels[ref[1]]=val[1]
units={'Backspace':2,'Tab':1.5,'Backslash':1.5,'Caps':1.75,'Enter':2.25,'LShift':2.25,'RShift':2.75,'Space':6.25,'LCtrl':1.25,'LWin':1.25,'LAlt':1.25,'RAlt':1.25,'Fn':1.25,'Menu':1.25,'RCtrl':1.25}
def cap(u):
 w=u*19.05-1.05
 outer=cq.Workplane('XY').rect(w,18).workplane(offset=8).rect(w-3,15).loft()
 inner=cq.Workplane('XY').rect(w-2.4,15.6).workplane(offset=6.5).rect(w-5.4,12.6).loft()
 return outer.cut(inner)
one=cap(1);space=cap(6.25)
for name,obj in [('1u-keycap-envelope',one),('625u-spacebar-envelope',space)]:
 assert obj.val().isValid();cq.exporters.export(obj,str(O/(name+'.step')))
spacekey=next(k for k in geo['keys'] if labels.get(k['reference'])=='Space')
a=cq.Assembly(name='spacebar-stabilizer-reference');a.add(space.translate((spacekey['x'],spacekey['y'],33)),name='spacebar-envelope')
for i,dx in enumerate([-50,0,50]):
 # Simple indicators only; no verified sockets, switch travel or stabilizer mechanism.
 obj=cq.Workplane('XY').box(5,5,5).translate((spacekey['x']+dx,spacekey['y'],30.5))
 a.add(obj,name=['left-stabilizer-reference','switch-stem-reference','right-stabilizer-reference'][i])
a.save(str(O/'spacebar-stabilizer-reference.step'))
layout=cq.Assembly(name='keycaps-fit-reference')
for k in geo['keys']:
 label=labels[k['reference']];obj=cap(units.get(label,1)).translate((k['x'],k['y'],33))
 layout.add(obj,name=k['reference']+'-keycap-envelope',color=cq.Color(.82,.85,.89))
layout.save(str(O/'keycaps-layout-reference.step'))
(O/'reference-notes.txt').write_text('Simplified generic keycap envelopes generated with CadQuery, not manufacturer models.\n1U: 18x18mm base, 15x15mm top, 8mm high. 6.25U: 118.0125mm base width.\nNo MX cross sockets, row-specific profiles, legends or verified switch travel. Do not print these as functional keycaps.\nSpacebar support markers are nominal +/-50mm references, not actual stabilizer mechanisms.\nLayout uses actual PCB switch centers. Physical cap/stabilizer fit remains untested.\n')
print('Generated 61 keycap envelopes and spacebar references')
