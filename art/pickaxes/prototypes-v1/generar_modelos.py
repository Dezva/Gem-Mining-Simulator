"""Prototipos 3D originales de cuatro picos para Gem Mining Simulator.
Generados con trimesh: geometría procedural; no modifica .rbxm.
X horizontal, Y vertical, Z profundidad.
"""
import json, math
from pathlib import Path
import numpy as np
import trimesh
from shapely.geometry import Polygon
from shapely.ops import triangulate
from trimesh.visual.material import PBRMaterial
from trimesh.visual import TextureVisuals

DIR=Path(__file__).resolve().parent
PALETTES={
 'legendary': {'shaft':(39,32,43), 'grip':(90,54,48), 'metal':(227,159,53), 'rim':(255,216,116), 'edge':(255,245,170), 'gem':(252,124,36), 'glow':(255,181,50), 'dark':(75,44,52)},
 'celestial': {'shaft':(24,34,67), 'grip':(49,67,111), 'metal':(144,163,213), 'rim':(228,237,255), 'edge':(192,238,255), 'gem':(68,172,255), 'glow':(123,204,255), 'dark':(38,56,104)},
 'supreme': {'shaft':(25,47,54), 'grip':(35,91,80), 'metal':(212,156,60), 'rim':(255,219,118), 'edge':(187,255,206), 'gem':(40,221,187), 'glow':(79,255,203), 'dark':(29,69,64)},
 'mythic': {'shaft':(31,23,48), 'grip':(73,36,99), 'metal':(104,64,155), 'rim':(189,115,244), 'edge':(255,137,243), 'gem':(147,56,246), 'glow':(238,72,230), 'dark':(50,20,86)},
}
class Build:
 def __init__(self,theme):
  self.theme=theme;self.p=PALETTES[theme];self.scene=trimesh.Scene();self.id=0;self.metadata=[]
 def add(self,mesh,name,kind,emission=False):
  col=self.p[kind];self.id+=1
  mat=PBRMaterial(name=f'{self.theme}_{kind}',baseColorFactor=[*col,255],metallicFactor=0.8 if kind in ['metal','rim','edge'] else 0.25,roughnessFactor=0.22 if kind in ['gem','glow','edge'] else 0.4,emissiveFactor=([c/255*.55 for c in col] if emission else [0,0,0]))
  mesh.visual=TextureVisuals(material=mat)
  self.scene.add_geometry(mesh,geom_name=f'{name}_{self.id}',node_name=f'{name}_{self.id}')
  self.metadata.append({'name':name,'kind':kind,'triangles':len(mesh.faces)})
 def rod(self,name,start,end,r,kind,segments=12):
  a=np.array(start,dtype=float);b=np.array(end,dtype=float);d=b-a
  if np.linalg.norm(d)<1e-4:return
  mesh=trimesh.creation.cylinder(radius=r,height=np.linalg.norm(d),sections=segments)
  mat=trimesh.geometry.align_vectors([0,0,1],d/np.linalg.norm(d))
  mesh.apply_transform(mat);mesh.apply_translation((a+b)*.5);self.add(mesh,name,kind)
 def ico(self,name,pos,r,kind,sub=1,emission=False):
  m=trimesh.creation.icosphere(subdivisions=sub,radius=r);m.apply_translation(pos);self.add(m,name,kind,emission)
 def shard(self,name,x,y,z,w,h,kind,emission=False):
  verts=np.array([[x,y+h*.56,z],[x+w*.65,y,z],[x,y,z+w*.55],[x-w*.65,y,z],[x,y,z-w*.55],[x,y-h*.56,z]])
  faces=np.array([[0,1,2],[0,2,3],[0,3,4],[0,4,1],[5,2,1],[5,3,2],[5,4,3],[5,1,4]])
  self.add(trimesh.Trimesh(vertices=verts,faces=faces,process=True),name,kind,emission)
 def wing(self,name,points,thick,kind):
  p=np.asarray(points,dtype=float);cen=p.mean(axis=0)
  layers=[(0.72,-thick*.55),(1.,-thick*.3),(0.84,thick*.40),(0.65,thick*.65)]
  verts=[]
  for s,z in layers:verts.extend([(cen[0]+(x-cen[0])*s,cen[1]+(y-cen[1])*s,z) for x,y in p])
  n=len(p);faces=[]
  for j in range(len(layers)-1):
   for k in range(n):
    a=j*n+k;b=j*n+(k+1)%n;c=(j+1)*n+k;d=(j+1)*n+(k+1)%n
    faces.extend([[a,b,c],[b,d,c]])
  for j,flip in [(0,True),(len(layers)-1,False)]:
   scale,z=layers[j];q=[(cen[0]+(x-cen[0])*scale,cen[1]+(y-cen[1])*scale) for x,y in p]
   poly=Polygon(q)
   for tri in triangulate(poly):
    if not poly.covers(tri.representative_point()):continue
    ii=[]
    for xx,yy in list(tri.exterior.coords)[:3]:
     try:idx=next(k for k,(px,py) in enumerate(q) if abs(px-xx)<1e-6 and abs(py-yy)<1e-6)
     except StopIteration:
      idx=len(verts);verts.append((xx,yy,z));ii.append(idx);continue
     ii.append(j*n+idx)
    faces.append(ii[::-1] if flip else ii)
  self.add(trimesh.Trimesh(vertices=np.array(verts),faces=np.array(faces),process=True),name,kind)
 def wing_symmetric(self,name,pts,kind,thick=.28):
  self.wing(f'{name}_right',pts,thick,kind)
  self.wing(f'{name}_left',[(-x,y) for x,y in reversed(pts)],thick,kind)
 def frame(self):
  self.rod('ForgedHandle',(0,-2.05,0),(0,1.66,0),.185,'shaft',18)
  for y in [-1.86,-1.62,-1.38,-1.14,-.9]:self.rod(f'GripWrap_{y}',(0,y-.085,0),(0,y+.085,0),.205,'grip',14)
  for y in [-2.01,-.73,.92,1.25,1.52]:self.rod('MetalCollar',(0,y-.08,0),(0,y+.08,0),.235,'rim',12)
  self.shard('PommelGem',0,-2.15,0,.36,.39,'gem',True)
  self.rod('CrossHeadBridge',(-.63,1.57,0),(.63,1.57,0),.32,'metal',14)
  self.ico('GemHousing',(0,1.72,0),.43,'rim',1)
  self.shard('CentralCore',0,1.72,-.2,.43,.66,'gem',True)
 def build_legendary(self):
  self.frame()
  pts=[(.27,1.66),(.62,2.06),(1.05,2.10),(1.5,2.49),(1.94,2.57),(1.71,2.16),(2.05,1.83),(1.52,1.91),(1.17,1.5),(.71,1.4)]
  self.wing_symmetric('RoyalSunblade',pts,'metal',.42)
  self.wing_symmetric('GoldenInnerEdge',[(.60,1.77),(1.12,2.05),(1.79,2.34),(1.45,2.19),(1.10,1.82)],'rim',.47)
  self.shard('AmberHeart',0,1.98,-.27,.54,.85,'gem',True)
  for x in [-1.75,1.75]:self.shard('AmberPoint',x,2.28,0,.17,.35,'glow',True)
  self.rod('CrownFinial',(0,2.13,0),(0,2.70,0),.11,'rim',8)
  self.shard('SolarFinial',0,2.77,0,.27,.45,'edge',True)
 def build_celestial(self):
  self.frame()
  pts=[(.30,1.65),(.62,2.24),(.97,2.70),(1.26,2.35),(1.81,2.44),(2.13,2.08),(1.76,1.85),(1.56,1.48),(1.00,1.80)]
  self.wing_symmetric('AstralSilverWing',pts,'metal',.35)
  self.wing_symmetric('AuroraEdge',[(.90,2.42),(1.2,2.58),(1.39,2.28),(1.91,2.23),(1.59,2.06),(1.16,2.10)],'edge',.39)
  self.shard('BlueStar',0,1.92,-.3,.52,.9,'gem',True)
  for x,y in [(-1.40,2.72),(1.40,2.72),(-2.05,2.38),(2.05,2.38)]:self.shard('StarSparks',x,y,0,.13,.25,'glow',True)
  for i in range(24):
   a=2*math.pi*i/24;b=2*math.pi*(i+1)/24
   self.rod('CelestialOrbit',(1.65*math.cos(a),1.85+1.04*math.sin(a),.40),(1.65*math.cos(b),1.85+1.04*math.sin(b),.40),.042,'rim',6)
 def build_supreme(self):
  self.frame()
  pts=[(.3,1.65),(.65,2.34),(1.02,2.43),(1.34,2.91),(1.57,2.48),(2.04,2.62),(2.24,2.37),(1.93,2.14),(2.44,1.90),(1.74,1.83),(1.42,1.45),(.86,1.67)]
  self.wing_symmetric('CrownedJadeBlade',pts,'metal',.40)
  self.wing_symmetric('AuricBladeTrim',[(.75,2.1),(1.36,2.68),(1.64,2.34),(2.10,2.38),(1.73,2.17),(2.12,1.99),(1.28,1.92)],'rim',.46)
  self.wing_symmetric('SovereignJadeCore',[(.8,2.08),(1.22,2.55),(1.39,2.27),(1.88,2.26),(1.52,2.05),(1.84,1.95),(1.17,1.82)],'gem',.49)
  self.shard('HeartOfTheSovereign',0,1.99,-.34,.52,.94,'gem',True)
  self.shard('RoyalTopGem',0,2.78,-.14,.26,.5,'glow',True)
  for x in [-2.36,2.36]:self.shard('FloatingJade',x,2.37,0,.18,.37,'edge',True)
  for i in range(6):
   y=-.57+i*.39
   self.rod('RunicGripBand',(-.15,y,-.04),(.15,y,.04),.044,'rim',7)
 def build_mythic(self):
  self.frame()
  pts=[(.25,1.69),(.54,2.14),(1.02,2.4),(1.59,2.95),(2.21,3.08),(1.93,2.66),(2.45,2.16),(2.34,1.71),(1.96,1.88),(1.43,1.52),(.81,1.48)]
  self.wing_symmetric('AbyssalScythe',pts,'dark',.50)
  self.wing_symmetric('VioletEdge',[(.86,2.15),(1.58,2.69),(2.14,2.89),(1.80,2.56),(2.27,2.03),(1.68,1.94),(1.17,1.71)],'rim',.48)
  self.wing_symmetric('ArcaneBlade',[(1.09,2.16),(1.63,2.64),(2.0,2.78),(1.71,2.40),(2.16,2.05),(1.62,2.02)],'gem',.51)
  self.shard('AbyssalCore',0,1.96,-.35,.58,1.13,'glow',True)
  for x,y in [(-2.53,2.58),(2.53,2.58),(-1.9,3.12),(1.9,3.12)]:self.shard('ArcaneOrbit',x,y,.05,.16,.3,'edge',True)
  for i in range(15):
   a=math.pi*.05+math.pi*.9*i/15;b=math.pi*.05+math.pi*.9*(i+1)/15
   self.rod('RunicHalfRing',(1.22*math.cos(a),1.65+1.52*math.sin(a),.35),(1.22*math.cos(b),1.65+1.52*math.sin(b),.35),.042,'glow',6)
 def save(self):
  fn=DIR/f'pick_{self.theme}_concept_v1.glb'
  fn.write_bytes(self.scene.export(file_type='glb'))
  bounds=self.scene.bounds
  return {'file':fn.name,'part_count':len(self.metadata),'triangles':sum(x['triangles'] for x in self.metadata),'bounds':np.round(bounds,4).tolist(),'coordinates':'X horizontal, Y vertical, Z depth','GripPoint':[0,-1.2,0],'StrikeTip':[2.0,2.25,0],'prototype':True}

if __name__=='__main__':
 out=[]
 for name in PALETTES:
  m=Build(name);getattr(m,'build_'+name)();item=m.save();out.append(item);print(name,item)
 (DIR/'modelo_manifest.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf8')
