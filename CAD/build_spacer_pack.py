"""Four plate spacers joined by sacrificial sprues for paid-service size limits."""
from pathlib import Path
import cadquery as cq
p=Path(__file__).resolve().parent
def box(x,y,dx,dy):return cq.Workplane('XY').box(dx,dy,1.2,centered=(False,False,False)).translate((x,y,0))
pack=None
for x,y in [(0,0),(12,0),(0,12),(12,12)]:
 ring=cq.Workplane('XY').circle(3).circle(1.65).extrude(3.5).translate((x,y,0))
 pack=ring if pack is None else pack.union(ring)
for y in [0,12]:pack=pack.union(box(2.8,y-.6,6.4,1.2))
for x in [0,12]:pack=pack.union(box(x-.6,2.8,1.2,6.4))
assert pack.val().isValid() and len(pack.solids().vals())==1
cq.exporters.export(pack,str(p/'plate-spacer-pack.stl'),tolerance=.08)
cq.exporters.export(pack,str(p/'plate-spacer-pack.step'))
print('18 x 18 x 3.5mm pack; four spacers; trim sacrificial sprues after printing.')
