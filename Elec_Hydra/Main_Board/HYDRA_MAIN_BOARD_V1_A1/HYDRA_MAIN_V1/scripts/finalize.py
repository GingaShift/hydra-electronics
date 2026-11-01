import pcbnew as b,json,xml.etree.ElementTree as E,collections
from pathlib import Path
P=Path(__file__).resolve().parents[1];p=P/'HYDRA_MAIN_V1.kicad_pcb';pcb=b.LoadBoard(str(p))
assert b.ImportSpecctraSES(pcb,str(P/'reports/HYDRA_fast.ses')), 'Specctra import failed; no board saved'
print('Specctra import verified')
# Restore exact schematic association from netlist stamps.
x=E.parse(P/'reports/schematic_netlist.xml')
for c in x.findall('.//components/comp'):
 fp=next((f for f in pcb.GetFootprints() if f.GetReference()==c.attrib['ref']),None)
 if fp:
  stamp=c.findtext('tstamps');sheet=c.find('sheetpath').attrib['tstamps'];fp.SetPath(b.KIID_PATH(sheet+stamp))
# Match deliberate NC nets and mechanical/testpoint BOM flags exactly.
for nn in x.findall('.//nets/net'):
 name=nn.attrib['name']
 if not name.startswith('unconnected-'):continue
 net=b.NETINFO_ITEM(pcb,name);pcb.Add(net)
 for node in nn.findall('node'):
  for fp in pcb.GetFootprints():
   if fp.GetReference()==node.attrib['ref']:
    for pad in fp.Pads():
     if pad.GetNumber()==node.attrib['pin']:pad.SetNet(net)
for fp in pcb.GetFootprints():
 if fp.GetReference().startswith(('TP','H')):fp.SetAttributes(fp.GetAttributes() & ~b.FP_EXCLUDE_FROM_BOM)
pcb.BuildConnectivity();filler=b.ZONE_FILLER(pcb);filler.Fill(pcb.Zones());b.SaveBoard(str(p),pcb)
# Verify every pad net against exported native schematic connectivity.
expected={}
for n in x.findall('.//nets/net'):
 for node in n.findall('node'):expected[(node.attrib['ref'],node.attrib['pin'])]=n.attrib['name']
errors=[]
for fp in pcb.GetFootprints():
 for pad in fp.Pads():
  e=expected.get((fp.GetReference(),pad.GetNumber()),'');actual=pad.GetNetname()
  if e!=actual:errors.append([fp.GetReference(),pad.GetNumber(),e,actual])
report={'native_schematic_netlist':'kicad-cli 9.0.9 kicadxml','mismatched_pad_nets':errors,'tracks_by_layer':dict(collections.Counter(t.GetLayerName() for t in pcb.GetTracks())),'routed_track_count':sum(1 for t in pcb.GetTracks() if not isinstance(t,b.PCB_VIA)),'via_count':sum(isinstance(t,b.PCB_VIA) for t in pcb.GetTracks()),'outline_mm':[75,60],'copper_layers':4}
(P/'reports/CONNECTIVITY.json').write_text(json.dumps(report,indent=2));print(report)
