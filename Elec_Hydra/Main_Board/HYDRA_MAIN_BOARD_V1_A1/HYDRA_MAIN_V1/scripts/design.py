"""HYDRA V1 authoritative component/net/placement model; rebuild with generate.py."""
from pathlib import Path
import json
P=Path(__file__).resolve().parents[1]
parts=[]
def add(ref,lib,value,fp,nets,sch,pcb,mpn='',maker='',note=''):
 parts.append(dict(ref=ref,lib=lib,value=value,fp=fp,nets={str(k):v for k,v in nets.items()},sch=sch,pcb=pcb,mpn=mpn,maker=maker,note=note))
RFP='Resistor_SMD:R_0603_1608Metric';CFP='Capacitor_SMD:C_0603_1608Metric'
ri=ci=0
def R(val,a,b,sch,pcb,mpn=None):
 global ri;ri+=1
 code={'10k':'10K','100k':'100K','4.7k':'4K7','2.2k':'2K2','1k':'1K','5.1k':'5K1','33k':'33K','82k':'82K','22':'22R','47':'47R','0':'0R','3.3k':'3K3'}[val]
 add('R'+str(ri),'Device:R',val,RFP,{1:a,2:b},sch,pcb,mpn or 'RC0603FR-07'+code+'L','Yageo');return 'R'+str(ri)
def C(val,a,sch,pcb,fp=CFP,mpn=None):
 global ci;ci+=1
 mpn=mpn or {'100n':'GRM188R71C104KA01D','2.2u':'GRM188R71A225KE15D','4.7u':'GRM21BR71A475KA73L','10u':'GRM21BR71A106KE51L','30p':'GRM1885C1H300JA01D','14p':'GRM1885C1H140JA01D'}[val]
 add('C'+str(ci),'Device:C',val,fp,{1:a,2:'GND'},sch,pcb,mpn,'Murata');return 'C'+str(ci)
# Complete MCU mapping; None explicitly unconnected.
n={i:None for i in range(1,65)}
n.update({1:'+3V3',39:'LED_STATUS',5:'HSE_IN',6:'HSE_OUT',7:'NRST',8:'EXT_ADC1',9:'EXT_ADC2',12:'GND',13:'VDDA',14:'EXT_PWM1',15:'EXT_PWM2',16:'EXT_PWM3',17:'EXT_PWM4',18:'GND',19:'+3V3',28:'BOOT1',29:'STM_TX',30:'STM_RX',31:'VCAP1',32:'+3V3',33:'FLASH_CS',34:'FLASH_SCK',35:'FLASH_MISO',36:'FLASH_MOSI',37:'EXT_GPIO1',38:'EXT_GPIO2',40:'BME_SDA',41:'BME_SCL',42:'VBUS_SENSE',44:'USB_DM',45:'USB_DP',46:'SWDIO',47:'VCAP2',48:'+3V3',49:'SWCLK',54:'LED_DATA',55:'SWO',58:'PB_SCL_MCU',59:'PB_SDA_MCU',60:'BOOT0',61:'INA_ALERT_MCU',63:'GND',64:'+3V3'})
add('U1','MCU_ST_STM32F4:STM32F405RGTx','STM32F405RGT6','Package_QFP:LQFP-64_10x10mm_P0.5mm',n,(0,110,100),(45,35,0),'STM32F405RGT6','STMicroelectronics')
# Support, spread on schematic right side.
for i,xy in enumerate([(39,27,90),(52,27,90),(53,42,0),(37,42,0)]):C('100n','+3V3',(0,170+i*23,45),xy)
C('4.7u','+3V3',(0,170,72),(55,46,0),'Capacitor_SMD:C_0805_2012Metric')
C('2.2u','VCAP1',(0,195,72),(37,35,0));C('2.2u','VCAP2',(0,220,72),(47,43,90))
add('FB1','Device:FerriteBead','600R@100MHz','Inductor_SMD:L_0603_1608Metric',{1:'+3V3',2:'VDDA'},(0,170,100),(35,24,0),'BLM18AG601SN1D','Murata')
C('100n','VDDA',(0,195,100),(35,28,0));C('4.7u','VDDA',(0,220,100),(31,26,90),'Capacitor_SMD:C_0805_2012Metric')
add('Y1','Device:Crystal_GND24','8MHz CL10pF','Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm',{1:'HSE_IN',2:'GND',3:'HSE_OUT',4:'GND'},(0,180,135),(33,34,90),'ECS-80-10-33-CHN-TR','ECS','CL10pF; C0max5pF ESRmax400R; gmcrit0.91mA/V, qualifier oscillation')
C('14p','HSE_IN',(0,210,135),(30,32,90));C('14p','HSE_OUT',(0,235,135),(30,36,90))
R('10k','BOOT0','GND',(0,170,165),(37,21,0));R('10k','BOOT1','GND',(0,195,165),(51,23,0));R('10k','NRST','+3V3',(0,220,165),(29,44,0));C('100n','NRST',(0,245,165),(29,48,0))
for ref,net,xy,sx in [('SW1','BOOT0',(19,52,0),180),('SW2','NRST',(30,52,0),230)]:
 add(ref,'Switch:SW_Push','BOOT' if ref=='SW1' else 'RESET','Button_Switch_SMD:SW_SPST_TL3342',{1:net,2:'+3V3' if ref=='SW1' else 'GND'},(0,sx,192),xy,'TL3342F160QG','E-Switch')
# Power and USB, page1.
add('J1','Connector_Generic:Conn_01x02','5V POWER IN','Connector_Molex:Molex_Micro-Fit_3.0_43650-0221_1x02_P3.00mm_Vertical',{1:'PB_5V',2:'GND'},(1,35,35),(10,11,0),'43650-0221','Molex')
for ref,src,dst,xy,sx in [('F1','PB_5V','PB_FUSED',(12,18,0),70),('F2','VBUS_USB','USB_FUSED',(9,35,90),150)]:
 add(ref,'Device:Polyfuse','0.50A hold','Fuse:Fuse_1206_3216Metric',{1:src,2:dst},(1,sx,35),xy,'1206L050/15YR','Littelfuse')
for ref,src,xy,sx in [('D1','PB_FUSED',(14,23,0),100),('D2','USB_FUSED',(14,31,0),190)]:
 add(ref,'Device:D_Schottky','SS14','Diode_SMD:D_SMA',{1:'+5V_SYS',2:src},(1,sx,35),xy,'SS14-E3/61T','Vishay','OR passif; protege retours et inversion polarite')
add('U2','HYDRA:AP7361C_33E','AP7361C-33E-13','Package_TO_SOT_SMD:SOT-223-3_TabPin2',{1:'+5V_SYS',2:'GND',3:'+3V3'},(1,90,80),(21,22,90),'AP7361C-33E-13','Diodes Inc.','SOT223: 1IN 2GND/tab 3OUT, pas AMS1117')
C('4.7u','+5V_SYS',(1,55,80),(19,16,0),'Capacitor_SMD:C_0805_2012Metric');C('4.7u','+3V3',(1,125,80),(25,22,90),'Capacitor_SMD:C_0805_2012Metric')
C('100n','+5V_SYS',(1,55,108),(20,29,0))
usb={k:'GND' for k in ['A1','A12','B1','B12','S1']};usb.update({k:'VBUS_USB' for k in ['A4','A9','B4','B9']});usb.update({'A5':'USB_CC1','B5':'USB_CC2','A6':'USB_DP_EXT','B6':'USB_DP_EXT','A7':'USB_DM_EXT','B7':'USB_DM_EXT','A8':None,'B8':None})
add('J5','Connector:USB_C_Receptacle_USB2.0_16P','USB-C USB2 DEVICE','Connector_USB:USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal',usb,(1,40,158),(4.5,29,270),'USB4105-GF-A','GCT')
R('5.1k','USB_CC1','GND',(1,85,130),(10,25,90));R('5.1k','USB_CC2','GND',(1,110,130),(10,29,90))
add('U5','Power_Protection:USBLC6-2SC6','USBLC6-2SC6','Package_TO_SOT_SMD:SOT-23-6',{1:'USB_DP_EXT',6:'USB_DP_EXT',3:'USB_DM_EXT',4:'USB_DM_EXT',2:'GND',5:'VBUS_USB'},(1,150,158),(13,39,90),'USBLC6-2SC6','STMicroelectronics')
C('100n','VBUS_USB',(1,190,130),(10,42,90))
R('22','USB_DM_EXT','USB_DM',(1,200,158),(36,48,90));R('22','USB_DP_EXT','USB_DP',(1,230,158),(39,48,90))
R('33k','VBUS_USB','VBUS_SENSE',(1,200,190),(43,49,90));R('82k','VBUS_SENSE','GND',(1,230,190),(47,49,90))
# Four LEDs only status/data connected GPIO; rest supply indicators.
for i,(net,label,color,mpn,res,xy) in enumerate([('+5V_SYS','PWR_5V','green','LTST-C190KGKT','3.3k',(7,61,0)),('+3V3','PWR_3V3','green','LTST-C190KGKT','2.2k',(12,61,0)),('LED_STATUS','STATUS','blue','LTST-C190TBKT','1k',(17,61,0)),('LED_DATA','DATA','yellow','LTST-C190KSKT','2.2k',(22,61,0))]):
 ref='D'+str(i+3);ln='LED_A'+str(i)
 R(res,net,ln,(2,40+i*65,180),(xy[0],57,90))
 add(ref,'Device:LED',label,'LED_SMD:LED_0603_1608Metric',{1:'GND',2:ln},(2,40+i*65,205),xy,mpn,'Lite-On',color)
# BME and flash page2.
add('U3','Memory_Flash:W25Q128JVS','W25Q128JVSIQ','Package_SO:SOIC-8_5.23x5.23mm_P1.27mm',{1:'FLASH_CS',2:'FLASH_MISO',3:'FLASH_WP',4:'GND',5:'FLASH_MOSI',6:'FLASH_SCK',7:'FLASH_HOLD',8:'+3V3'},(2,60,65),(63,34,0),'W25Q128JVSIQ','Winbond')
C('100n','+3V3',(2,100,40),(64,28,0));C('4.7u','+3V3',(2,125,40),(69,28,0),'Capacitor_SMD:C_0805_2012Metric')
for i,net in enumerate(['FLASH_CS','FLASH_WP','FLASH_HOLD']):R('10k',net,'+3V3',(2,35+i*40,105),(59+i*4,42,90))
add('U4','Sensor:BME280','BME280','Package_LGA:Bosch_LGA-8_2.5x2.5mm_P0.65mm_ClockwisePinNumbering',{1:'GND',2:'+3V3',3:'BME_SDA',4:'BME_SCL',5:'BME_ADDR',6:'+3V3',7:'GND',8:'+3V3'},(2,205,65),(77,48,0),'BME280','Bosch Sensortec','I2C3 adresse7bits0x77, CSB1 SDO1')
C('100n','+3V3',(2,245,35),(76,44,0));C('100n','+3V3',(2,245,65),(81,48,90))
R('4.7k','BME_SDA','+3V3',(2,185,105),(72,47,90));R('4.7k','BME_SCL','+3V3',(2,220,105),(72,51,90))
R('10k','BME_ADDR','+3V3',(2,250,105),(80,53,0))
# Interfaces page3.
add('J2','Connector_Generic:Conn_01x04','POWER I2C ALERT','Connector_Molex:Molex_Micro-Latch_53253-0470_1x04_P2.00mm_Vertical',{1:'PB_SDA',2:'PB_SCL',3:'INA_ALERT',4:'GND'},(3,45,45),(30,10,0),'53253-0470','Molex')
R('47','PB_SDA','PB_SDA_MCU',(3,85,40),(34,18,90));R('47','PB_SCL','PB_SCL_MCU',(3,115,40),(38,18,90));R('1k','INA_ALERT','INA_ALERT_MCU',(3,145,40),(42,18,90))
# Pullups on main are removable; no duplicates on Power Board.
for i,net in enumerate(['PB_SDA','PB_SCL','INA_ALERT']):R('2.2k' if i<2 else '10k',net,'+3V3',(3,85+i*30,70),(30+i*4,22,90))
add('J3','Connector_Generic:Conn_01x03','RPi UART 3V3','Connector_Molex:Molex_Micro-Latch_53253-0370_1x03_P2.00mm_Vertical',{1:'UART_TX',2:'UART_RX',3:'GND'},(3,205,40),(48,10,0),'53253-0370','Molex','vers Navigator SERIAL3: 1 vers RX3, 2 vers TX2, 3 vers GND6')
R('1k','STM_TX','UART_TX',(3,235,40),(48,18,90));R('1k','UART_RX','STM_RX',(3,265,40),(52,18,90))
add('J4','Connector_Generic:Conn_01x10','8 GPIO V2 LOGIC','Connector_Molex:Molex_Micro-Latch_53253-1070_1x10_P2.00mm_Vertical',{1:'EXT_PWM1',2:'EXT_PWM2',3:'EXT_PWM3',4:'EXT_PWM4',5:'EXT_GPIO1',6:'EXT_GPIO2',7:'EXT_ADC1',8:'EXT_ADC2',9:'GND',10:'+3V3'},(3,205,125),(62,10,0),'53253-1070','Molex','3V3 logique max50mA; aucune puissance actionneur')
add('J6','Connector_Generic:Conn_02x05_Odd_Even','SWD 2.54mm','Connector_PinHeader_2.54mm:PinHeader_2x05_P2.54mm_Vertical',{1:'+3V3',2:'SWDIO',3:'GND',4:'SWCLK',5:'GND',6:'SWO',7:None,8:None,9:'GND',10:'NRST'},(3,60,130),(9,46,0),'61301021121','Wurth','Standard ARM signaux mais pas pas1.27: adaptateur requis')
for i,(net,xy) in enumerate([('+5V_SYS',(23,34,0)),('+3V3',(27,34,0)),('GND',(23,38,0)),('NRST',(24,48,0)),('UART_TX',(48,24,0)),('UART_RX',(52,24,0)),('PB_SDA',(29,17,0)),('PB_SCL',(32,17,0)),('INA_ALERT',(42,24,0)),('BOOT0',(37,17,0))]):
 add('TP'+str(i+1),'Connector:TestPoint',net,'TestPoint:TestPoint_Pad_D1.5mm',{1:net},(3,35+(i%5)*48,180+(i//5)*25),xy,'','', 'Test pad')
# ERC flags actual supply origins. Invisible on PCB, no fabrication item.
for i,net in enumerate(['GND','+5V_SYS','VDDA']):
 add('#FLG'+str(i+1),'power:PWR_FLAG','PWR_FLAG','',{1:net},(1,40+i*40,220),(0,0,0))
for ref,xy in [('H1',(4,4,0)),('H2',(86,4,0)),('H3',(4,71,0)),('H4',(86,71,0))]:
 add(ref,'Mechanical:MountingHole','M2.5 NPTH','MountingHole:MountingHole_2.7mm_M2.5',{},(3,220+(int(ref[-1])-1)*15,225),xy,'','')
# Layout refinements: critical loops and connector clearance.
fix={'C1':(41.25,26,90),'C2':(53.5,30,0),'C3':(49,44,90),'C4':(41.5,44,90),'C5':(56,46,0),'C6':(46,44,90),'C7':(53.5,33.5,0),'FB1':(33,40,0),'C8':(35.5,38,0),'C9':(33,44,90),'Y1':(34,33.5,90),'C10':(30,31,90),'C11':(30,36,90),'R1':(44,21,0),'F1':(6,18,0),'C16':(16,43,90),'R2':(55,24,0),'R3':(29,44,0),'F2':(14,35,0),'D1':(13,21,0),'D2':(14,31,0),'U2':(22,21.5,90),'C14':(27,21,90),'R4':(11,24,0),'R5':(11,27,0),'J6':(6,43,0),'TP10':(43,14,0),'R10':(7,57.5,90),'R11':(12,57.5,90),'TP6':(57,20,0),'TP9':(44,25,0)}
fix.update({'J5':(85.5,32.65,90),'U5':(61,32.65,0),'R6':(56,33.6,180),'R7':(56,31.7,180),'C7':(53.5,36.5,0),'R4':(78,26,0),'R5':(78,39,0),'C16':(61,28,0),'F2':(78,21,0),'D2':(69,21,0),'U3':(66,46,0),'C17':(65,40,0),'C18':(70,40,0),'R14':(61,54,90),'R15':(65,54,90),'R16':(69,54,90)})
for part in parts:
 if part['ref'] in fix:part['pcb']=fix[part['ref']]
# Compact placement A1; all packages keep their original dimensions.
for part in parts:
 x,y,a=part['pcb'];part['pcb']=(x-7,y-5,a)
compact={'J1':(9,11,0),'J2':(23,8,0),'J3':(37,8,0),'J4':(49,8,0),'J5':(70.5,27.65,90),'J6':(5,32,0),'H1':(3.5,3.5,0),'H2':(71.5,3.5,0),'H3':(3.5,56.5,0),'H4':(71.5,56.5,0),'F1':(6,20,0),'D1':(12,23,0),'U2':(18,18.5,90),'C13':(17,12.5,0),'C14':(23,18,90),'C15':(18,25,0),'F2':(65,16,0),'D2':(57,16,0),'R4':(63,21,0),'R5':(63,34,0),'U3':(56,40,0),'C17':(56,34,0),'C18':(60,34,0),'R14':(52,47,90),'R15':(56,47,90),'R16':(60,47,90),'U4':(68,44,0),'C19':(67,40,0),'C20':(71,44,90),'R17':(64,43,90),'R18':(64,47,90),'R19':(70,49,0),'D3':(6,48,0),'D4':(10,48,0),'D5':(14,48,0),'D6':(18,48,0),'R10':(6,44.5,90),'R11':(10,44.5,90),'R12':(14,44.5,90),'R13':(18,44.5,90),'SW1':(15,38,0),'SW2':(24,44,0),'TP1':(23,25,0),'TP2':(24,29,0),'TP3':(19,29,0),'TP4':(19,42,0),'TP5':(39,18,0),'TP6':(43,18,0),'TP7':(20,17,0),'TP8':(24,17,0),'TP9':(37,20,0),'TP10':(31,13,0)}
compact.update({'D1':(9,26,0),'R10':(6,45.5,90),'R11':(10,45.5,90),'R12':(14,45.5,90),'R13':(18,45.5,90),'SW2':(26,46,0),'C12':(21,37,0),'TP1':(15,28,0),'TP2':(18,32,0),'TP4':(21,34,0),'TP7':(18,8,0),'TP8':(33,12,0),'TP10':(33,17,0),'R23':(23,14,90),'R5':(68,36,0)})
for part in parts:
 if part['ref'] in compact:part['pcb']=compact[part['ref']]
if __name__=='__main__':(P/'design.json').write_text(json.dumps(parts,indent=2));print(len(parts),'components')
