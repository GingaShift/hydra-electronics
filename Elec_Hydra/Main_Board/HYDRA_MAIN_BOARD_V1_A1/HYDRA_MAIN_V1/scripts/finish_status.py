import pcbnew as b,numpy as np,heapq,math
from pathlib import Path
P=Path(__file__).resolve().parents[1];f=str(P/'HYDRA_MAIN_V1.kicad_pcb');p=b.LoadBoard(f);M=b.FromMM;V=lambda x,y:b.VECTOR2I(M(x),M(y));net=p.FindNet('LED_STATUS')
def track(a,c,layer):
 t=b.PCB_TRACK(p);t.SetStart(V(*a));t.SetEnd(V(*c));t.SetLayer(layer);t.SetWidth(M(.2));t.SetNet(net);t.SetLocked(True);p.Add(t)
ends=[(46.5,30.55),(14.9,46.325)]
for pad,via in [((43.675,30.75),ends[0]),((14,46.325),ends[1])]:
 
 if pad==(43.675,30.75):
  track(pad,(44.55,30.75),b.F_Cu);track((44.55,30.75),(44.75,30.55),b.F_Cu);track((44.75,30.55),via,b.F_Cu)
 else:track(pad,via,b.F_Cu)
 v=b.PCB_VIA(p);v.SetPosition(V(*via));v.SetWidth(M(.6));v.SetDrill(M(.3));v.SetViaType(b.VIATYPE_THROUGH);v.SetLayerPair(b.F_Cu,b.B_Cu);v.SetNet(net);p.Add(v)
step=.1;grid=np.zeros((751,601),bool)
def block(x1,y1,x2,y2,r,rect=False):
 lo=np.maximum([0,0],np.floor((np.minimum([x1,y1],[x2,y2])-r)/step).astype(int));hi=np.minimum([750,600],np.ceil((np.maximum([x1,y1],[x2,y2])+r)/step).astype(int));xx,yy=np.meshgrid(np.arange(lo[0],hi[0]+1)*step,np.arange(lo[1],hi[1]+1)*step,indexing='ij')
 if rect:mask=np.ones(xx.shape,bool)
 else:
  dx=x2-x1;dy=y2-y1;l=dx*dx+dy*dy;t=np.clip(((xx-x1)*dx+(yy-y1)*dy)/l,0,1) if l else 0;mask=(xx-x1-t*dx)**2+(yy-y1-t*dy)**2<r*r
 grid[lo[0]:hi[0]+1,lo[1]:hi[1]+1]|=mask
for t in p.GetTracks():
 if t.GetNetname()=='LED_STATUS':continue
 if isinstance(t,b.PCB_VIA):x,y=b.ToMM(t.GetPosition().x),b.ToMM(t.GetPosition().y);block(x,y,x,y,b.ToMM(t.GetWidth(b.F_Cu))/2+.33)
 elif t.GetLayer()==b.B_Cu:
  a,c=t.GetStart(),t.GetEnd();block(b.ToMM(a.x),b.ToMM(a.y),b.ToMM(c.x),b.ToMM(c.y),b.ToMM(t.GetWidth())/2+.33)
for fp in p.GetFootprints():
 for a in fp.Pads():
  if a.GetNetname()=='LED_STATUS':continue
  if a.GetAttribute()!=b.PAD_ATTRIB_SMD:
   bb=a.GetBoundingBox();block(b.ToMM(bb.GetLeft()),b.ToMM(bb.GetTop()),b.ToMM(bb.GetRight()),b.ToMM(bb.GetBottom()),.35,True)
grid[:5,:]=True;grid[-5:,:]=True;grid[:,:5]=True;grid[:,-5:]=True
start,goal=[tuple(int(round(q/step)) for q in a) for a in ends];print('blocked endpoints',grid[start],grid[goal]);print('candidate vias',[(x, bool(grid[int(round(x/step)),int(round(30.75/step))])) for x in [44.4,44.5,44.6,44.7,45,45.2,45.5,46,46.5,47]]);assert not grid[start] and not grid[goal]
Q=[(0,start)];cost={start:0};prev={};directions=[(a,c) for a in [-1,0,1] for c in [-1,0,1] if a or c]
while Q:
 _,a=heapq.heappop(Q)
 if a==goal:break
 for dx,dy in directions:
  c=(a[0]+dx,a[1]+dy)
  if not(0<=c[0]<=750 and 0<=c[1]<=600) or grid[c]:continue
  nc=cost[a]+math.hypot(dx,dy)
  if nc<cost.get(c,1e20):cost[c]=nc;prev[c]=a;heapq.heappush(Q,(nc+math.hypot(c[0]-goal[0],c[1]-goal[1]),c))
assert goal in prev
path=[goal]
while path[-1]!=start:path.append(prev[path[-1]])
path.reverse();simple=[path[0]]
for i in range(1,len(path)-1):
 if (path[i][0]-path[i-1][0],path[i][1]-path[i-1][1])!=(path[i+1][0]-path[i][0],path[i+1][1]-path[i][1]):simple.append(path[i])
simple.append(goal);pts=[ends[0]]+[(x*step,y*step) for x,y in simple]+[ends[1]]
for a,c in zip(pts,pts[1:]):
 if a!=c:track(a,c,b.B_Cu)
for t in p.GetDrawings():
 if isinstance(t,b.PCB_TEXT) and t.GetText()=='MAIN BOARD V1':t.SetPosition(V(42,58.8));t.SetTextSize(V(.8,.8));t.SetTextThickness(M(.12))
p.BuildConnectivity();fill=b.ZONE_FILLER(p);fill.Fill(p.Zones());b.SaveBoard(f,p);print('status segments',len(pts)-1)
