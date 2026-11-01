import json,os,math
from pathlib import Path
import pcbnew as b
P=Path(__file__).resolve().parents[1];parts=json.loads((P/'design.json').read_text());pcb=b.BOARD();pcb.SetCopperLayerCount(4)
M=b.FromMM; V=lambda x,y:b.VECTOR2I(M(x),M(y))
pcb.GetDesignSettings().SetCopperLayerCount(4)
names=sorted({n for p in parts for n in p['nets'].values() if n}); nets={}
for n in names:net=b.NETINFO_ITEM(pcb,n);pcb.Add(net);nets[n]=net
footprints={}
for p in parts:
 if not p['fp']:continue
 fp=b.FootprintLoad(str(P/'libraries/HYDRA.pretty'),p['fp'].split(':')[1]);assert fp,p['fp']
 
 if p['ref']=='J5':b.FootprintSave(str(P/'libraries/HYDRA.pretty'),fp)
 fp.SetReference(p['ref']);fp.SetValue(p['value']);fp.SetFPID(b.LIB_ID('HYDRA',p['fp'].split(':')[1]))
 fp.SetPath(b.KIID_PATH('/'+p['uuid']))
 pcb.Add(fp);x,y,a=p['pcb'];fp.SetPosition(V(x,y));fp.SetOrientationDegrees(a)
 for pad in fp.Pads():
  num=pad.GetNumber();net=p['nets'].get(num)
  if net:pad.SetNet(nets[net])
 for field in [fp.Reference(),fp.Value()]:
  field.SetVisible(field==fp.Reference());field.SetTextSize(V(.8,.8));field.SetTextThickness(M(.12))
 fp.Reference().SetPosition(V(x,y-3));fp.Reference().SetLayer(b.F_SilkS)
 fp.Value().SetVisible(False)
 footprints[p['ref']]=fp
# Provisional rectangle 90x75mm, mounting holes NPTH.
for a,c in [((0,0),(75,0)),((75,0),(75,60)),((75,60),(0,60)),((0,60),(0,0))]:
 g=b.PCB_SHAPE();g.SetShape(b.SHAPE_T_SEGMENT);g.SetStart(V(*a));g.SetEnd(V(*c));g.SetWidth(M(.05));g.SetLayer(b.Edge_Cuts);pcb.Add(g)
def text(s,x,y,size=1,layer=b.F_SilkS):
 t=b.PCB_TEXT(pcb);t.SetText(s);t.SetPosition(V(x,y));t.SetTextSize(V(size,size));t.SetTextThickness(M(.15));t.SetLayer(layer);pcb.Add(t)
logo=b.FootprintLoad(str(P/'libraries/HYDRA.pretty'),'HYDRA_Official_Wordmark_40mm');pcb.Add(logo);logo.SetPosition(V(42,53));logo.SetReference('LOGO1');logo.Reference().SetVisible(False)
text('MAIN BOARD V1',42,59,1.0);text('A1',67,58,.8)
text('5V',10,6,.8);text('I2C',25,4,.8);text('UART',39,4,.8);text('V2',57,4,.8)
text('BOOT',15,41,.8);text('RESET',24,47,.8);text('SWD',6,29,.8)
for s,x in [('5V',6),('3V3',10),('STATUS',14),('DATA',18)]:text(s,x,51,.8)
# USB FS: short, adjacent front-layer pair with a short connector crossover.
def fixed_path(net,pts,layer=b.F_Cu):
 pts=[(x-(15 if x>=79 else 7),y-5) for x,y in pts]
 for aa,cc in zip(pts,pts[1:]):
  t=b.PCB_TRACK(pcb);t.SetStart(V(*aa));t.SetEnd(V(*cc));t.SetWidth(M(.2));t.SetLayer(layer);t.SetNet(nets[net]);t.SetLocked(True);pcb.Add(t)
fixed_path('USB_DP',[(50.675,32.75),(52.7,32.75),(53.75,31.7),(55.175,31.7)])
fixed_path('USB_DM',[(50.675,33.25),(52.7,33.25),(53.05,33.6),(55.175,33.6)])
fixed_path('USB_DP_EXT',[(56.825,31.7),(59.8625,31.7),(62.1375,31.7),(63,31.7),(64,32.7),(79,32.7),(79.8,31.9),(81.82,31.9)])
fixed_path('USB_DM_EXT',[(56.825,33.6),(59.8625,33.6),(62.1375,33.6),(63,33.6),(63.45,33.15),(79,33.15),(79.8,33.4),(81.82,33.4)])
fixed_path('USB_DP_EXT',[(79.8,31.9),(80.8,32.9),(81.82,32.9)])
fixed_path('USB_DM_EXT',[(81.82,32.4),(82.8,32.4)])
fixed_path('USB_DM_EXT',[(82.8,32.4),(82.8,34.2),(80.5,34.2)],b.B_Cu)
fixed_path('USB_DM_EXT',[(80.5,34.2),(79.8,33.5),(79.8,33.4),(81.82,33.4)])
fixed_path('VBUS_USB',[(62.1375,32.65),(62.9,32.65)])
for x,y in [(55.9,27.65)]:
 v=b.PCB_VIA(pcb);v.SetPosition(V(x,y));v.SetWidth(M(.6));v.SetDrill(M(.3));v.SetViaType(b.VIATYPE_THROUGH);v.SetLayerPair(b.F_Cu,b.B_Cu);v.SetNet(nets['VBUS_USB']);v.SetLocked(True);pcb.Add(v)
for x,y in [(67.8,27.4),(65.5,29.2)]:
 v=b.PCB_VIA(pcb);v.SetPosition(V(x,y));v.SetWidth(M(.6));v.SetDrill(M(.3));v.SetViaType(b.VIATYPE_THROUGH);v.SetLayerPair(b.F_Cu,b.B_Cu);v.SetNet(nets['USB_DM_EXT']);v.SetLocked(True);pcb.Add(v)
# Fan-out every SMD supply pad to its solid inner reference plane.
def mmrect(pad,margin):
 bb=pad.GetBoundingBox();return (b.ToMM(bb.GetLeft())-margin,b.ToMM(bb.GetTop())-margin,b.ToMM(bb.GetRight())+margin,b.ToMM(bb.GetBottom())+margin)
def segrect(x,y,ex,ey,rr):
 lo,hi=0.,1.
 for v,d,mn,mx in [(x,ex-x,rr[0],rr[2]),(y,ey-y,rr[1],rr[3])]:
  if abs(d)<1e-8:
   if v<mn or v>mx:return False
  else:
   q1,q2=(mn-v)/d,(mx-v)/d
   if q1>q2:q1,q2=q2,q1
   lo=max(lo,q1);hi=min(hi,q2)
   if lo>hi:return False
 return True
allpads=[p for fp in pcb.GetFootprints() for p in fp.Pads()];vias=[];no_fan=[]
for pad in allpads:
 if pad.GetNetname() not in ['GND','+3V3'] or pad.GetAttribute()!=b.PAD_ATTRIB_SMD:continue
 x,y=b.ToMM(pad.GetPosition().x),b.ToMM(pad.GetPosition().y);chosen=None
 for d in [.9,1.2,1.5,2.,2.5,3.,4.,5.,6.,7.]:
  for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(.707,.707),(-.707,.707),(.707,-.707),(-.707,-.707)]:
   ex,ey=x+dx*d,y+dy*d
   if not(1<ex<74 and 1<ey<59):continue
   if any(r[0]<ex<r[2] and r[1]<ey<r[3] for r in [mmrect(z,.5) for z in allpads]):continue
   if any((ex-vx)**2+(ey-vy)**2<.85**2 for vx,vy in vias):continue
   if any(segrect(x,y,ex,ey,(min(b.ToMM(t.GetStart().x),b.ToMM(t.GetEnd().x))-.4,min(b.ToMM(t.GetStart().y),b.ToMM(t.GetEnd().y))-.4,max(b.ToMM(t.GetStart().x),b.ToMM(t.GetEnd().x))+.4,max(b.ToMM(t.GetStart().y),b.ToMM(t.GetEnd().y))+.4)) for t in pcb.GetTracks() if t.GetNetCode()!=pad.GetNetCode() and not isinstance(t,b.PCB_VIA)):continue
   if any(segrect(x,y,ex,ey,mmrect(z,.29)) for z in allpads if z.GetNetCode()!=pad.GetNetCode()):continue
   chosen=(ex,ey);break
  if chosen:break
 if not chosen:no_fan.append((pad.GetNetname(),pad.GetNumber()));continue
 ex,ey=chosen
 t=b.PCB_TRACK(pcb);t.SetStart(V(x,y));t.SetEnd(V(ex,ey));t.SetWidth(M(.2));t.SetLayer(b.F_Cu);t.SetNet(pad.GetNet());pcb.Add(t)
 v=b.PCB_VIA(pcb);v.SetPosition(V(ex,ey));v.SetWidth(M(.6));v.SetDrill(M(.3));v.SetViaType(b.VIATYPE_THROUGH);v.SetLayerPair(b.F_Cu,b.B_Cu);v.SetNet(pad.GetNet());pcb.Add(v);vias.append(chosen)
print('Supply fanouts',len(vias),'unplaced',no_fan)
# Place visible reference labels clear of pads and other text.
def rect(item,margin=0):
 bb=item.GetBoundingBox();return (b.ToMM(bb.GetLeft())-margin,b.ToMM(bb.GetTop())-margin,b.ToMM(bb.GetRight())+margin,b.ToMM(bb.GetBottom())+margin)
def hit(a,c):return a[0]<c[2] and a[2]>c[0] and a[1]<c[3] and a[3]>c[1]
obs=[rect(p,.22) for fp in pcb.GetFootprints() for p in fp.Pads()]
# Reserve official logo extent.
obs.append((21,48,63,58))
obs += [rect(g,.12) for f in pcb.GetFootprints() for g in f.GraphicalItems() if g.GetLayer()==b.F_SilkS]
texts=[g for g in pcb.GetDrawings() if isinstance(g,b.PCB_TEXT)]
texts += [f.Reference() for f in pcb.GetFootprints() if f.Reference().IsVisible()]
for t in texts:
 if t.GetText()=='LOGO1':continue
 x,y=b.ToMM(t.GetPosition().x),b.ToMM(t.GetPosition().y)
 candidates=[(x,y)]+[(x+dx,y+dy) for d in [1.2,2,3,4,5,6,8] for dx,dy in [(0,-d),(0,d),(-d,0),(d,0),(-d,-d),(d,-d),(-d,d),(d,d)]]
 for cx,cy in candidates:
  t.SetPosition(V(cx,cy));rr=rect(t,.08)
  if rr[0]<1 or rr[1]<1 or rr[2]>74 or rr[3]>59:continue
  if not any(hit(rr,r) for r in obs):break
 obs.append(rect(t,.08))
# Continuous internal reference planes, no signal routing on these layers.
for layer,netname in [(b.In1_Cu,'GND'),(b.In2_Cu,'+3V3')]:
 z=b.ZONE(pcb);z.SetLayer(layer);z.SetNet(nets[netname]);z.SetLocalClearance(M(.18));z.SetPadConnection(b.ZONE_CONNECTION_FULL);z.SetThermalReliefGap(M(.25));z.SetThermalReliefSpokeWidth(M(.25));z.SetMinThickness(M(.15))
 poly=z.Outline();poly.NewOutline()
 for x,y in [(.5,.5),(74.5,.5),(74.5,59.5),(.5,59.5)]:poly.Append(M(x),M(y))
 pcb.Add(z)
# Fill only after serialization/load, to initialize project settings
# Rules/export temporary board; route all required signals on outer layers.
pcb.GetDesignSettings().m_SolderMaskMargin=M(.05)
pcb.SetFileName(str(P/'HYDRA_MAIN_V1.kicad_pcb'))
b.SaveBoard(str(P/'HYDRA_MAIN_V1.kicad_pcb'),pcb)
print('Board generated',len(footprints),'footprints',len(nets),'nets')
for num in ['19','32','48','64','31','47','44','45','5','6','12','13']:
 pad=next(p for p in footprints['U1'].Pads() if p.GetNumber()==num);pos=pad.GetPosition();print('U1',num,round(b.ToMM(pos.x),3),round(b.ToMM(pos.y),3))
pcb=b.LoadBoard(str(P/'HYDRA_MAIN_V1.kicad_pcb'));pcb.BuildConnectivity();filler=b.ZONE_FILLER(pcb);filler.Fill(pcb.Zones());b.SaveBoard(str(P/'HYDRA_MAIN_V1.kicad_pcb'),pcb)
# Native export to Specctra; keep input for reproducibility.
b.ExportSpecctraDSN(pcb,str(P/'reports/HYDRA_unrouted.dsn'))

# Restrict router to outer signal layers; inner planes are power reference layers.
dsn=P/'reports/HYDRA_unrouted.dsn'
s=dsn.read_text()
for layer in ['In1.Cu','In2.Cu']:
 s=s.replace('(layer '+layer+'\n      (type signal)', '(layer '+layer+'\n      (type power)')
dsn.write_text(s)
