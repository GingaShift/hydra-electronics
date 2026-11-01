from pathlib import Path
import json,csv,collections,xml.etree.ElementTree as E,shutil
P=Path(__file__).resolve().parents[1];parts=json.loads((P/'design.json').read_text())
def csvfile(name,head,rows):
 with (P/'docs'/name).open('w',newline='',encoding='utf-8-sig') as f:w=csv.writer(f);w.writerow(head);w.writerows(rows)
groups=collections.defaultdict(list)
for p in parts:
 if p['ref'].startswith(('#','TP','H')):continue
 groups[(p['value'],p['mpn'],p['maker'],p['fp'],p['note'])].append(p['ref'])
csvfile('BOM.csv',['Designators','Quantity','Value','Manufacturer','MPN','Footprint','Notes'],[[','.join(v),len(v),k[0],k[2],k[1],k[3],k[4]] for k,v in groups.items()])
csvfile('BOM_DETAIL.csv',['Designator','Value','Manufacturer','MPN','Footprint','Notes'],[[p['ref'],p['value'],p['maker'],p['mpn'],p['fp'],p['note']] for p in parts if not p['ref'].startswith('#')])
# Official complete LQFP64 table, pin names from vendor-derived KiCad symbol.
pin_names={1:'VBAT',2:'PC13',3:'PC14',4:'PC15',5:'PH0',6:'PH1',7:'NRST',8:'PC0',9:'PC1',10:'PC2',11:'PC3',12:'VSSA',13:'VDDA',14:'PA0',15:'PA1',16:'PA2',17:'PA3',18:'VSS',19:'VDD',20:'PA4',21:'PA5',22:'PA6',23:'PA7',24:'PC4',25:'PC5',26:'PB0',27:'PB1',28:'PB2',29:'PB10',30:'PB11',31:'VCAP1',32:'VDD',33:'PB12',34:'PB13',35:'PB14',36:'PB15',37:'PC6',38:'PC7',39:'PC8',40:'PC9',41:'PA8',42:'PA9',43:'PA10',44:'PA11',45:'PA12',46:'PA13',47:'VCAP2',48:'VDD',49:'PA14',50:'PA15',51:'PC10',52:'PC11',53:'PC12',54:'PD2',55:'PB3',56:'PB4',57:'PB5',58:'PB6',59:'PB7',60:'BOOT0',61:'PB8',62:'PB9',63:'VSS',64:'VDD'}
func={29:('USART3_TX AF7','J3.1 via1k','UART disponible Navigator SERIAL3 RX'),30:('USART3_RX AF7','J3.2 via1k','UART bidirectionnel3V3'),58:('I2C1_SCL AF4 OD','J2.2 via47R','Bus dedie INA226'),59:('I2C1_SDA AF4 OD','J2.1 via47R','Bus dedie INA226'),40:('I2C3_SDA AF4 OD','U4.3','Bus interne independant'),41:('I2C3_SCL AF4 OD','U4.4','Bus interne independant'),33:('GPIO output','U3.1 CS','Pullup10k repos haut'),34:('SPI2_SCK AF5','U3.6','SPI dedie Flash'),35:('SPI2_MISO AF5','U3.2','SPI dedie Flash'),36:('SPI2_MOSI AF5','U3.5','SPI dedie Flash'),44:('USB_OTG_FS_DM AF10','J5 via22R/ESD','USB FS device'),45:('USB_OTG_FS_DP AF10','J5 via22R/ESD','USB FS device'),42:('OTG_FS_VBUS / input','VBUS div33k/82k','Detection hote sans5V direct'),46:('SWDIO AF0','J6.2','Programmation'),49:('SWCLK AF0','J6.4','Programmation'),55:('TRACESWO AF0','J6.6','Debug optionnel'),61:('GPIO input EXTI8','J2.3 via1k','INA_ALERT actif bas OD'),39:('GPIO output','R12 D5','STATUS; PC13 non utilise'),54:('GPIO output','R13 D6','DATA firmware'),14:('TIM2_CH1 AF1','J4.1','Reserve PWM, frequence commune TIM2'),15:('TIM2_CH2 AF1','J4.2','Reserve PWM'),16:('TIM2_CH3 AF1','J4.3','Reserve PWM'),17:('TIM2_CH4 AF1','J4.4','Reserve PWM'),37:('GPIO','J4.5','Reserve polyvalente'),38:('GPIO','J4.6','Reserve polyvalente'),8:('ADC123_IN10','J4.7','Reserve analogique0..VDDA'),9:('ADC123_IN11','J4.8','Reserve analogique0..VDDA'),5:('OSC_IN','Y1.1','HSE8MHz'),6:('OSC_OUT','Y1.3','HSE8MHz'),60:('BOOT0 strap','SW1/R1','0 normal,1ROM'),28:('BOOT1 strap','R2','10k GND pourROM DFU'),7:('NRST','SW2/J6.10/TP4','Reset10k/100n'),31:('VCAP1','C6','2.2u versGND, aucun autre usage'),47:('VCAP2','C7','2.2u versGND, aucun autre usage')}
u=next(p for p in parts if p['ref']=='U1');rows=[]
for i in range(1,65):
 net=u['nets'][str(i)]
 f,d,j=func.get(i,('Alimentation' if net in ['+3V3','GND','VDDA'] else 'NC',net or 'Non connectee','Pin alimentation decouplee' if net else 'Reserve non accessible, firmware analogique sans pull'))
 rows.append([i,pin_names[i],net or 'NC',f,d,j])
csvfile('PIN_MAPPING_STM32.csv',['Pin physique','Nom ST','Signal net','Fonction / AF','Destination','Justification'],rows)
with (P/'docs/PIN_MAPPING_STM32.md').open('w') as f:
 f.write('# Affectation STM32F405RGT6 — LQFP64\n\nSource: ST DS8626 rev12, tables7et9. Directions TX/RX vues depuis STM32. Deux voyants d’alimentation sont câblés aux rails; seuls STATUS et DATA emploient des GPIO.\n\n|Pin|Nom|Signal|Fonction/AF|Destination|Justification|\n|---:|---|---|---|---|---|\n')
 for r in rows:f.write('|'+ '|'.join(map(str,r))+'|\n')
 f.write('\nTIM2 CH1–CH4 partagent la base de temps; quatre rapports cycliques independants, frequence commune. Les ADC et huit GPIO externes sont strictement logiques3V3.\n')
for src,dst in [('research_stm32.md','AUDIT_ST_STM32.md'),('review_electrical.md','REVUE_ELECTRIQUE.md'),('research_power_connectors.md','ETUDE_ALIMENTATION.md'),('review_power_actual.md','REVUE_CONNECTEURS.md')]:
 
 if (P.parent/src).exists():shutil.copy(P.parent/src,P/'reports'/dst)
if (P.parent/'logo_work/extraction_note.md').exists():shutil.copy(P.parent/'logo_work/extraction_note.md',P/'docs/LOGO_OFFICIEL.md')
if (P.parent/'logo_work/extraction_manifest.json').exists():shutil.copy(P.parent/'logo_work/extraction_manifest.json',P/'docs/LOGO_SOURCE.json')
print('BOM and complete64-pin mapping generated')
