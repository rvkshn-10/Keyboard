# Keyboard 
Hello, this is a Keyboard Project which was my first time developing a PCB, after numerous errors and attempts, I finally got it done thanks to the Half Life Program at Hack Club. 
Firmware for the Raspberry Pi Pico is in the firmware folder, while the PCB and schematic files are in the main folder. Inside of the keyboard61 folder you can find the fabrication files for the circuit board. The layout and pictures have also been put there.

## Bill of materials

This table lists the whole planned build and who is responsible for each purchase. The Hack Club request covers only the rows marked **Hack Club funding request**, the other parts are planned personal purchases. Prices are estimates in USD before checkout unless noted. The PCB estimate is from the older, larger outline and needs a new quote for the compact layout.

| Part | Qty | Unit | Total | Vendor | Buyer |
| --- | ---: | ---: | ---: | --- | --- |
| [Keyboard PCB, batch of 5](https://cart.jlcpcb.com/quote) | 1 | $31.15 | $31.15 | JLCPCB | Hack Club funding request; re-quote revised board |
| [onsemi 1N4148 DO-35 diodes](https://www.digikey.com/en/products/detail/onsemi/1N4148/458603) | 61 | $0.0422 | $2.57 | DigiKey | Hack Club funding request |
| [Raspberry Pi Pico H](https://www.digikey.com/en/products/detail/raspberry-pi/SC0917/16608257) | 1 | $5.00 | $5.00 | DigiKey | Hack Club funding request |
| [Adafruit Pico female socket pair](https://www.digikey.com/en/products/detail/adafruit-industries-llc/5583/16688063) | 1 pair | $0.95 | $0.95 | DigiKey | Hack Club funding request |
| [Adafruit 4111 USB-A to Micro-B cable, 1 m](https://www.digikey.com/en/products/detail/adafruit-industries-llc/4111/9992197) | 1 | $3.95 | $3.95 | DigiKey | Hack Club funding request |
| **Hack Club request parts subtotal** |  |  | **$43.62** |  |  |
| Tax and shipping estimate (not a current checkout quote) | 1 | $20.00 | $20.00 | Multiple vendors | Hack Club request estimate |
| **Estimated Hack Club total** |  |  | **$63.62 of $65** |  | **$1.38 remaining; confirm current carts** |
| [Gateron Milky Yellow Pro V2, 70 switches](https://www.amazon.com/dp/B0BBPPP7HD) | 1 pack | $19.99 | $19.99 | Amazon | Personal purchase |
| [XVX green keycap set](https://www.amazon.com/dp/B0DNMV32L2) | 1 set | $13.99 | $13.99 | Amazon | Personal purchase |
| [Chilkey snap-in stabilizer kit](https://www.amazon.com/dp/B0D2KMVVL3) | 1 kit | $21.99 | $21.99 | Amazon | Personal purchase |
| [Tactile reset buttons, 126-piece pack](https://www.amazon.com/dp/B0D5M2ZNSL) | 1 pack | $4.66 | $4.66 | Amazon | Personal purchase |
| [M3 nylon standoff and fastener kit](https://www.amazon.com/dp/B0G3XCGSNV) | 1 kit | $6.99 | $6.99 | Amazon | Personal purchase |
| [Adafruit rotary encoder with knob](https://www.adafruit.com/product/377) | 1 | $4.50 | $4.50 | Adafruit | Personal purchase |
| [Adafruit 1955 jumper wire pack](https://www.adafruit.com/product/1955) | 1 pack | $3.95 | $3.95 | Adafruit | Personal purchase |
| [ShillehTek AA317 2.8-inch ILI9341 TFT](https://shillehtek.com/products/2-8-spi-tft-lcd-touch-screen-module-240x320-ili9341-for-arduino) | 1 | $10.99 | $10.99 | ShillehTek | Personal purchase |
| Paid printing service for case, plate, and spacers | 1 | Quote needed | Quote needed | TBD | Personal purchase; quote current CAD |
| **Personal parts subtotal** |  |  | **$87.06** |  | **Before tax, shipping, and printing** |
| **Combined known parts subtotal** |  |  | **$130.68** |  | **Before tax, shipping, and printing** |

The $20 tax-and-shipping amount is a planning placeholder, not a confirmed cart total. The Amazon prices were last checked October 7, 2026 and need checkout verification. The prior enclosure-print quote used older geometry and is not included.

## Compact PCB layout

The current KiCad board outline is 295.05 × 100.05 mm, reduced from the earlier 295 × 168 mm layout. The Pico is mounted on the underside beneath the left key area, so it does not need a separate blank strip above the keyboard. Moving it beside the full-width key matrix would require a wider board or a separate wired module, so the current compact outline keeps it inside the keyboard footprint. The two KiCad 3D renders below show the front and underside, physical clearance still needs a hardware fit check.

![KiCad 3D render of the compact keyboard PCB top](CAD/review/pcb-top-3d.png)

![KiCad 3D render of the PCB underside with the Pico and diodes](CAD/review/pcb-bottom-3d.png)

Here are some images of my work!
![Project image 1](https://halflife.hackclub-assets.com/hackclub-half-life/sessions/3jjjr94n6OVBuAuok83iCpwSTn9oI9Z0/2844f40d75c5796160a3fc0e4111c849d99f9a8e8a85075c33664b29f76958e6.jpg)
![Project image 2](https://halflife.hackclub-assets.com/hackclub-half-life/sessions/3jjjr94n6OVBuAuok83iCpwSTn9oI9Z0/1ce5be343caff0c61ab4016f752b8d9515fbfa89795fed86c663ede11e9eeec6.png)
![Project image 3](https://halflife.hackclub-assets.com/hackclub-half-life/sessions/3jjjr94n6OVBuAuok83iCpwSTn9oI9Z0/6d660de9637e0b907a25daf5680e9168ea810fe933ba5206ebef935523ce8c37.png)
![Project image 4](https://halflife.hackclub-assets.com/hackclub-half-life/sessions/3jjjr94n6OVBuAuok83iCpwSTn9oI9Z0/96064cbf2dae7636ce794e34669d33f09c4712a7b40dfe2b68e3ad4e3d0c8126.png)
![Project image 5](https://halflife.hackclub-assets.com/hackclub-half-life/sessions/3jjjr94n6OVBuAuok83iCpwSTn9oI9Z0/4aad322bfb6f143ab1dbf59bddeb86e5bbb4e1c6f556318b76ef5f5194c42ceb.png)
![Project image 6](https://halflife.hackclub-assets.com/hackclub-half-life/sessions/3jjjr94n6OVBuAuok83iCpwSTn9oI9Z0/4d90e7126712b07fb729884dd06a1cf8b81b48d4b9f6ad75a873305a741dd5c3.png)
![Project image 7](https://halflife.hackclub-assets.com/hackclub-half-life/sessions/3jjjr94n6OVBuAuok83iCpwSTn9oI9Z0/2968c0a8a03da4ef494fb9d00208e11051d0f48078f3af143ee9bd9a53434c6b.png)
![Project image 8](https://halflife.hackclub-assets.com/hackclub-half-life/sessions/3jjjr94n6OVBuAuok83iCpwSTn9oI9Z0/5f12dc12cfa9dc35a2a9fd2210207e06fdea44fa817c951d62eeb21929e9158b.png)
![Project image 9](https://halflife.hackclub-assets.com/hackclub-half-life/sessions/3jjjr94n6OVBuAuok83iCpwSTn9oI9Z0/c91cceff1e5670762f1b32b61f960f69a1cca61d0eba6e4534c9dbc367dc4ae5.png)
![Project image 10](https://halflife.hackclub-assets.com/hackclub-half-life/sessions/3jjjr94n6OVBuAuok83iCpwSTn9oI9Z0/d6bd2181e24846ba51d9f8a30a60647065539afe7f0dd30ba3d5dba011afa4a8.png)
![Project image 11](https://halflife.hackclub-assets.com/hackclub-half-life/sessions/3jjjr94n6OVBuAuok83iCpwSTn9oI9Z0/eab954a873282cca162a78d8e920870463b7103c9327fb3bdca17ff2b42283ef.png)
![Project image 12](https://halflife.hackclub-assets.com/hackclub-half-life/sessions/3jjjr94n6OVBuAuok83iCpwSTn9oI9Z0/942b03c3524fabad6b11df0404272491656dd57b52222f556d02fd2b44e51a5a.png)
![Project image 13](https://halflife.hackclub-assets.com/hackclub-half-life/sessions/3jjjr94n6OVBuAuok83iCpwSTn9oI9Z0/c3bc702737a021fe5a6d49c9a58fac6d1a9b3909316d45e9701b576ea9dede89.png)
![Project image 14](https://halflife.hackclub-assets.com/hackclub-half-life/sessions/3jjjr94n6OVBuAuok83iCpwSTn9oI9Z0/bd0b317dc335715baf4aee61fdf86eacbc8f3ac63f42f7975988054d51fce02e.png)
![Project image 15](https://halflife.hackclub-assets.com/hackclub-half-life/sessions/3jjjr94n6OVBuAuok83iCpwSTn9oI9Z0/625b72ee99f4c3e56e71418c850e5b3e35eb97e628f5baa8a03fde9f128c8062.png)
![Project image 16](https://halflife.hackclub-assets.com/hackclub-half-life/sessions/3jjjr94n6OVBuAuok83iCpwSTn9oI9Z0/0b6b56f8961bd738425d091deb2750fc97ec065e7eeccbe2dce3432145c802c7.png)
![Project image 17](https://halflife.hackclub-assets.com/hackclub-half-life/sessions/3jjjr94n6OVBuAuok83iCpwSTn9oI9Z0/5a519c2b78881e31534b583dcee24f203fd03819496d71a958b3f3ca4a4b945b.png)
![Project image 18](https://halflife.hackclub-assets.com/hackclub-half-life/sessions/3jjjr94n6OVBuAuok83iCpwSTn9oI9Z0/57cc32490635e3243c4068b93a2888d7e6416f411c1d1504c7e2824c417accc0.png)
![Project image 19](https://halflife.hackclub-assets.com/hackclub-half-life/sessions/3jjjr94n6OVBuAuok83iCpwSTn9oI9Z0/1ccebb1bf9a8c59374a5aab74a32cd02d4ad2d0dcf79b6c4073d05719be1d418.png)
