# Affectation STM32F405RGT6 — LQFP64

Source: ST DS8626 rev12, tables7et9. Directions TX/RX vues depuis STM32. Deux voyants d’alimentation sont câblés aux rails; seuls STATUS et DATA emploient des GPIO.

|Pin|Nom|Signal|Fonction/AF|Destination|Justification|
|---:|---|---|---|---|---|
|1|VBAT|+3V3|Alimentation|+3V3|Pin alimentation decouplee|
|2|PC13|NC|NC|Non connectee|Reserve non accessible, firmware analogique sans pull|
|3|PC14|NC|NC|Non connectee|Reserve non accessible, firmware analogique sans pull|
|4|PC15|NC|NC|Non connectee|Reserve non accessible, firmware analogique sans pull|
|5|PH0|HSE_IN|OSC_IN|Y1.1|HSE8MHz|
|6|PH1|HSE_OUT|OSC_OUT|Y1.3|HSE8MHz|
|7|NRST|NRST|NRST|SW2/J6.10/TP4|Reset10k/100n|
|8|PC0|EXT_ADC1|ADC123_IN10|J4.7|Reserve analogique0..VDDA|
|9|PC1|EXT_ADC2|ADC123_IN11|J4.8|Reserve analogique0..VDDA|
|10|PC2|NC|NC|Non connectee|Reserve non accessible, firmware analogique sans pull|
|11|PC3|NC|NC|Non connectee|Reserve non accessible, firmware analogique sans pull|
|12|VSSA|GND|Alimentation|GND|Pin alimentation decouplee|
|13|VDDA|VDDA|Alimentation|VDDA|Pin alimentation decouplee|
|14|PA0|EXT_PWM1|TIM2_CH1 AF1|J4.1|Reserve PWM, frequence commune TIM2|
|15|PA1|EXT_PWM2|TIM2_CH2 AF1|J4.2|Reserve PWM|
|16|PA2|EXT_PWM3|TIM2_CH3 AF1|J4.3|Reserve PWM|
|17|PA3|EXT_PWM4|TIM2_CH4 AF1|J4.4|Reserve PWM|
|18|VSS|GND|Alimentation|GND|Pin alimentation decouplee|
|19|VDD|+3V3|Alimentation|+3V3|Pin alimentation decouplee|
|20|PA4|NC|NC|Non connectee|Reserve non accessible, firmware analogique sans pull|
|21|PA5|NC|NC|Non connectee|Reserve non accessible, firmware analogique sans pull|
|22|PA6|NC|NC|Non connectee|Reserve non accessible, firmware analogique sans pull|
|23|PA7|NC|NC|Non connectee|Reserve non accessible, firmware analogique sans pull|
|24|PC4|NC|NC|Non connectee|Reserve non accessible, firmware analogique sans pull|
|25|PC5|NC|NC|Non connectee|Reserve non accessible, firmware analogique sans pull|
|26|PB0|NC|NC|Non connectee|Reserve non accessible, firmware analogique sans pull|
|27|PB1|NC|NC|Non connectee|Reserve non accessible, firmware analogique sans pull|
|28|PB2|BOOT1|BOOT1 strap|R2|10k GND pourROM DFU|
|29|PB10|STM_TX|USART3_TX AF7|J3.1 via1k|UART disponible Navigator SERIAL3 RX|
|30|PB11|STM_RX|USART3_RX AF7|J3.2 via1k|UART bidirectionnel3V3|
|31|VCAP1|VCAP1|VCAP1|C6|2.2u versGND, aucun autre usage|
|32|VDD|+3V3|Alimentation|+3V3|Pin alimentation decouplee|
|33|PB12|FLASH_CS|GPIO output|U3.1 CS|Pullup10k repos haut|
|34|PB13|FLASH_SCK|SPI2_SCK AF5|U3.6|SPI dedie Flash|
|35|PB14|FLASH_MISO|SPI2_MISO AF5|U3.2|SPI dedie Flash|
|36|PB15|FLASH_MOSI|SPI2_MOSI AF5|U3.5|SPI dedie Flash|
|37|PC6|EXT_GPIO1|GPIO|J4.5|Reserve polyvalente|
|38|PC7|EXT_GPIO2|GPIO|J4.6|Reserve polyvalente|
|39|PC8|LED_STATUS|GPIO output|R12 D5|STATUS; PC13 non utilise|
|40|PC9|BME_SDA|I2C3_SDA AF4 OD|U4.3|Bus interne independant|
|41|PA8|BME_SCL|I2C3_SCL AF4 OD|U4.4|Bus interne independant|
|42|PA9|VBUS_SENSE|OTG_FS_VBUS / input|VBUS div33k/82k|Detection hote sans5V direct|
|43|PA10|NC|NC|Non connectee|Reserve non accessible, firmware analogique sans pull|
|44|PA11|USB_DM|USB_OTG_FS_DM AF10|J5 via22R/ESD|USB FS device|
|45|PA12|USB_DP|USB_OTG_FS_DP AF10|J5 via22R/ESD|USB FS device|
|46|PA13|SWDIO|SWDIO AF0|J6.2|Programmation|
|47|VCAP2|VCAP2|VCAP2|C7|2.2u versGND, aucun autre usage|
|48|VDD|+3V3|Alimentation|+3V3|Pin alimentation decouplee|
|49|PA14|SWCLK|SWCLK AF0|J6.4|Programmation|
|50|PA15|NC|NC|Non connectee|Reserve non accessible, firmware analogique sans pull|
|51|PC10|NC|NC|Non connectee|Reserve non accessible, firmware analogique sans pull|
|52|PC11|NC|NC|Non connectee|Reserve non accessible, firmware analogique sans pull|
|53|PC12|NC|NC|Non connectee|Reserve non accessible, firmware analogique sans pull|
|54|PD2|LED_DATA|GPIO output|R13 D6|DATA firmware|
|55|PB3|SWO|TRACESWO AF0|J6.6|Debug optionnel|
|56|PB4|NC|NC|Non connectee|Reserve non accessible, firmware analogique sans pull|
|57|PB5|NC|NC|Non connectee|Reserve non accessible, firmware analogique sans pull|
|58|PB6|PB_SCL_MCU|I2C1_SCL AF4 OD|J2.2 via47R|Bus dedie INA226|
|59|PB7|PB_SDA_MCU|I2C1_SDA AF4 OD|J2.1 via47R|Bus dedie INA226|
|60|BOOT0|BOOT0|BOOT0 strap|SW1/R1|0 normal,1ROM|
|61|PB8|INA_ALERT_MCU|GPIO input EXTI8|J2.3 via1k|INA_ALERT actif bas OD|
|62|PB9|NC|NC|Non connectee|Reserve non accessible, firmware analogique sans pull|
|63|VSS|GND|Alimentation|GND|Pin alimentation decouplee|
|64|VDD|+3V3|Alimentation|+3V3|Pin alimentation decouplee|

TIM2 CH1–CH4 partagent la base de temps; quatre rapports cycliques independants, frequence commune. Les ADC et huit GPIO externes sont strictement logiques3V3.
