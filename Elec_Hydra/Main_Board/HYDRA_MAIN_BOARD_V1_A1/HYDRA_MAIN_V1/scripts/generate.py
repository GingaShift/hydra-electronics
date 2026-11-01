from pathlib import Path
import sys,json,copy,math,uuid,shutil
import sexpdata as sx
from design import parts,P
S=sx.Symbol
def key(x):return str(x[0]) if isinstance(x,list) and x else ''
def find(x,k):return next((a for a in x if key(a)==k),None)
def U():return str(uuid.uuid4())
def out(x):return sx.dumps(x)
ROOT=P.parent/'tooling/root/usr/share/kicad'
if not ROOT.exists():ROOT=Path('/usr/share/kicad')
cache={};used={}
def load(libname):
 lib,name=libname.split(':');
 if lib=='HYDRA':
  pins=[(1,'IN','power_in',-10.16,2.54,0),(2,'GND','power_in',0,-10.16,90),(3,'OUT','power_out',10.16,2.54,180)]
  a=[S('symbol'),name,[S('pin_names'),[S('offset'),1.016]],[S('in_bom'),S('yes')],[S('on_board'),S('yes')]]
  for i,(k,v) in enumerate([('Reference','U'),('Value',name)]):a.append([S('property'),k,v,[S('id'),i],[S('at'),0,10-i*2.54,0],[S('effects'),[S('font'),[S('size'),1.27,1.27]]]])
  g=[S('symbol'),name+'_0_1',[S('rectangle'),[S('start'),-7.62,7.62],[S('end'),7.62,-7.62],[S('stroke'),[S('width'),.254],[S('type'),S('default')]],[S('fill'),[S('type'),S('background')]]]]
  for num,n,t,x,y,an in pins:g.append([S('pin'),S(t),S('line'),[S('at'),x,y,an],[S('length'),2.54],[S('name'),n,[S('effects'),[S('font'),[S('size'),1.27,1.27]]]],[S('number'),str(num),[S('effects'),[S('font'),[S('size'),1.27,1.27]]]]])
  a.append(g);return a
 if lib not in cache:
  cache[lib]={a[1]:a for a in sx.loads((ROOT/'symbols'/(lib+'.kicad_sym')).read_text()) if key(a)=='symbol'}
 a=copy.deepcopy(cache[lib][name]);ext=find(a,'extends')
 if ext:
  base=load(lib+':'+ext[1]);a.remove(ext)
  for el in base:
   if key(el)=='symbol':
    el[1]=el[1].replace(ext[1]+'_',name+'_',1);a.append(el)
 return a
liblocal=[]
for p in parts:
 lib=p['lib']
 if lib not in used:
  a=load(lib); old=a[1]; new=lib.replace(':','_');a[1]=new
  for c in a:
   if key(c)=='symbol': c[1]=c[1].replace(old+'_',new+'_',1)
  # remove property ids legacy, hide description metadata. Reuse full drawing + pin types.
  for c in a:
   if key(c)=='property':c[:]=[z for z in c if key(z)!='id']
  used[lib]=a;liblocal.append(a)
(P/'libraries/HYDRA.kicad_sym').write_text(out([S('kicad_symbol_lib'),[S('version'),20220914],[S('generator'),S('kicad_symbol_editor')]]+liblocal))
(P/'sym-lib-table').write_text('(sym_lib_table (lib (name "HYDRA")(type "KiCad")(uri "${KIPRJMOD}/libraries/HYDRA.kicad_sym")(options "")(descr "Self contained HYDRA symbols")))')
fpdir=P/'libraries/HYDRA.pretty';fpdir.mkdir(exist_ok=True)
for p in parts:
 if p['fp']:
  lib,fp=p['fp'].split(':');src=ROOT/'footprints'/(lib+'.pretty')/(fp+'.kicad_mod')
  if not src.exists():raise FileNotFoundError(src)
  shutil.copy(src,fpdir/(fp+'.kicad_mod'));p['fp']='HYDRA:'+fp
for f in (P.parent/'logo_work').glob('*.kicad_mod'):shutil.copy(f,fpdir/f.name)
(P/'fp-lib-table').write_text('(fp_lib_table (lib (name "HYDRA")(type "KiCad")(uri "${KIPRJMOD}/libraries/HYDRA.pretty")(options "")(descr "Project local footprints")))')
rootuuid=U();sheetids=[rootuuid,U(),U(),U()];names=['HYDRA_MAIN_V1','Power_USB','Peripherals','Interfaces']
# symbol support and standalone pin-labelled drawing. All global nets explicit.
def pins(lib):
 a=used[lib];result=[]
 for g in a:
  if key(g)=='symbol':
   for t in g:
    if key(t)=='pin':result.append((find(t,'number')[1],find(t,'at')[1:],t))
 return result
for i,name in enumerate(names):
 a=[S('kicad_sch'),[S('version'),20230121],[S('generator'),S('eeschema')],[S('uuid'),sheetids[i]],[S('paper'),'A3'],[S('title_block'),[S('title'),'HYDRA MAIN BOARD V1 — '+name],[S('date'),'2026-10-27'],[S('rev'),'A1 COMPACT'],[S('company'),'HYDRA / Proteus + HydroVinci']]]
 lsy=[]
 for lib in {p['lib'] for p in parts if p['sch'][0]==i}:
  d=copy.deepcopy(used[lib]);d[1]='HYDRA:'+d[1];lsy.append(d)
 a.append([S('lib_symbols')]+lsy)
 for p in [p for p in parts if p['sch'][0]==i]:
  lib=p['lib']; libid='HYDRA:'+used[lib][1];x,y=[round(round(v/1.27)*1.27,5) for v in p['sch'][1:]];uid=U();p['uuid']=uid
  inst=[S('symbol'),[S('lib_id'),libid],[S('at'),x,y,0],[S('unit'),1],[S('in_bom'),S('no') if p['ref'].startswith('#') else S('yes')],[S('on_board'),S('no') if p['ref'].startswith('#') else S('yes')],[S('dnp'),S('no')],[S('uuid'),uid]]
  # Reference above symbol based on bounding box.
  pp=pins(lib); miny=min([-float(at[1]) for n,at,t in pp]+[-4]);maxx=max([float(at[0]) for n,at,t in pp]+[4])
  for j,(k,v) in enumerate([('Reference',p['ref']),('Value',p['value']),('Footprint',p['fp']),('Datasheet',''),('MPN',p['mpn']),('Manufacturer',p['maker'])]):
   ef=[S('effects'),[S('font'),[S('size'),1.0,1.0]]];
   if j>1:ef.append(S('hide'))
   inst.append([S('property'),k,v,[S('at'),x if p['ref']=='U1' else x+maxx+7,y+miny-10+j*2 if p['ref']=='U1' else y-2+j*2,0],ef])
  for n,at,t in pp:
   inst.append([S('pin'),n,[S('uuid'),U()]])
   px=round(x+float(at[0]),5);py=round(y-float(at[1]),5);ang=float(at[2]);net=p['nets'].get(n)
   if net is None:a.append([S('no_connect'),[S('at'),px,py],[S('uuid'),U()]]);continue
   # external direction opposite pin direction; screen y inverted.
   dx=-math.cos(math.radians(ang));dy=math.sin(math.radians(ang));length=3.81
   ex=round(px+dx*length,5);ey=round(py+dy*length,5)
   a.append([S('wire'),[S('pts'),[S('xy'),px,py],[S('xy'),ex,ey]],[S('stroke'),[S('width'),0],[S('type'),S('default')]],[S('uuid'),U()]])
   la=0 if abs(dx)>0.9 else 90
   ef=[S('effects'),[S('font'),[S('size'),.85,.85]],[S('justify'),S('right') if dx<-.5 else S('left')]]
   a.append([S('global_label'),net,[S('shape'),S('bidirectional')],[S('at'),ex,ey,0 if dx<-.5 else 180 if dx>.5 else 90 if dy>0 else 270],ef,[S('uuid'),U()],[S('property'),'Intersheetrefs','${INTERSHEET_REFS}',[S('at'),ex,ey,0],[S('effects'),[S('font'),[S('size'),.85,.85]],S('hide')]]])
  path='/'+rootuuid+('' if i==0 else '/'+sheetids[i]);inst.append([S('instances'),[S('project'),'HYDRA_MAIN_V1',[S('path'),path,[S('reference'),p['ref']],[S('unit'),1]]]])
  a.append(inst)
 if i==0:
  for j in range(1,4):
   x=14;y=157+(j-1)*14
   a.append([S('sheet'),[S('at'),x,y],[S('size'),55,10],[S('stroke'),[S('width'),.15],[S('type'),S('default')]],[S('fill'),[S('color'),0,0,0,0]],[S('uuid'),sheetids[j]],[S('property'),'Sheetname',names[j],[S('at'),x,y-1,0],[S('effects'),[S('font'),[S('size'),1.27,1.27]],[S('justify'),S('left')]]],[S('property'),'Sheetfile',names[j]+'.kicad_sch',[S('at'),x,y+11,0],[S('effects'),[S('font'),[S('size'),1.27,1.27]],[S('justify'),S('left')]]],[S('instances'),[S('project'),'HYDRA_MAIN_V1',[S('path'),'/'+rootuuid,[S('page'),str(j+1)]]]]])
  a.append([S('sheet_instances'),[S('path'),'/',[S('page'),'1']]])
 # Clear page note.
 notes=['Core: HSE8MHz; VDDA filtered; VCAP2x2.2uF. No motor / Lumen / Navigator sensors.', 'Input 5V only 4.75-5.25V. Schottky OR drops voltage; +5V_SYS is not a precision 5V rail.', 'BME280 I2C3 0x77. Flash SPI2. STATUS and DATA are firmware-driven GPIO LEDs.', 'All cable pin numbering: connector mating face, confirm latch orientation. INA pullups only here; no hotplug.']
 a.append([S('text'),notes[i],[S('at'),145,16,0],[S('effects'),[S('font'),[S('size'),1.15,1.15]]],[S('uuid'),U()]])
 (P/(name+'.kicad_sch')).write_text(out(a))
# Project settings based on provided project preserving valid structure only.
proj=json.loads((P/'scripts/templates/base_project.kicad_pro').read_text())
proj['meta']={'filename':'HYDRA_MAIN_V1.kicad_pro','version':1}
proj['board']['design_settings']['rules'].update({'min_clearance':.15,'min_track_width':.15,'min_via_diameter':.6,'min_through_hole_diameter':.3,'min_hole_clearance':.25,'min_copper_edge_clearance':.3,'min_text_height':.8,'min_text_thickness':.12,'min_silk_text_height':.8,'min_silk_text_thickness':.12})
proj['net_settings']['classes']=[{'name':'Default','clearance':.18,'track_width':.2,'via_diameter':.6,'via_drill':.3,'diff_pair_width':.2,'diff_pair_gap':.15,'diff_pair_via_gap':.25,'bus_width':12,'line_style':0,'microvia_diameter':.3,'microvia_drill':.1,'pcb_color':'rgba(0, 0, 0, 0.000)','schematic_color':'rgba(0, 0, 0, 0.000)','wire_width':6}]
proj['net_settings']['netclass_assignments']={};proj['net_settings']['netclass_patterns']=[]
proj['erc']['erc_exclusions']=[];proj['board']['design_settings']['drc_exclusions']=[]
(P/'HYDRA_MAIN_V1.kicad_pro').write_text(json.dumps(proj,indent=2))
(P/'design.json').write_text(json.dumps(parts,indent=2))
print('Generated native 4-sheet schematic, local libraries and',len(parts),'parts')
