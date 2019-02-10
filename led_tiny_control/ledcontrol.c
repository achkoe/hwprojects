//****************************************************************************
//  ws2812 - Serial driver for ws2812 RGB leds using fastpwm
//
//  Test program
//
//  2013 by M. Marquardt (adrock0905@alice.de)
//
//  Please see README.TXT for more information
//

#define F_CPU 8000000

#include <avr/io.h>
#include <util/delay.h>
#include <avr/pgmspace.h>
#include <avr/interrupt.h>
#include <stdlib.h>

#include "ws2812.h"
#include "gammacorrection.h"



//
//  Constants for test pattern "chasing lights"
//

#ifdef WS_ARCH_XMEGA
    #define NUMLEDS     320     // number of leds on strip
    #define NUMFLOW     20      // number of "flows"
#else
    #define NUMLEDS     50      // number of leds on strip
    #define NUMFLOW     5       // number of "flows"
#endif

#define NUMFADE     5       // amount of fadeout
#define BRIGHT      60      // amount of randomized brightness
#define MINBRIGHT   32      // minimal brightness for R/G/B
#define OUTDELAY    50      // Delay in ms

//
//  Some necessary functions for XMega clock setup
//

#ifdef WS_ARCH_XMEGA

#define AVR_ENTER_CRITICAL_REGION( ) uint8_t volatile saved_sreg = SREG; \
cli();

#define AVR_LEAVE_CRITICAL_REGION( ) SREG = saved_sreg;

void CCPWrite( volatile uint8_t * address, uint8_t value )
{
    AVR_ENTER_CRITICAL_REGION( );

    volatile uint8_t * tmpAddr = address;
    #ifdef RAMPZ
    RAMPZ = 0;
    #endif
    asm volatile(
    "movw r30,  %0"       "\n\t"
    "ldi  r16,  %2"       "\n\t"
    "out   %3, r16"       "\n\t"
    "st     Z,  %1"       "\n\t"
    :
    : "r" (tmpAddr), "r" (value), "M" (CCP_IOREG_gc), "i" (&CCP)
    : "r16", "r30", "r31"
    );

    AVR_LEAVE_CRITICAL_REGION( );
}
#endif

//
//  Some macros for RGB manipulation
//

#define PUTRGB(D,I,R,G,B) {*(D+((I)*3)+1)=R; *(D+((I)*3))=G; *(D+((I)*3)+2)=B; }
#define FADE(D,V) ({ uint16_t I; for(I=0; I<sizeof(D); I++) if(D[I] > V) D[I] -= V; else D[I] = 0; })

//
//  Data
//

static uint8_t MyData[NUMLEDS*3];
static const uint8_t PROGMEM GammaTable[] = GCN_TABLE7TO8;


//****************************************************************************
//  MAIN
//

int main(void)
{
    uint16_t I, J, PixelP[NUMFLOW];
    uint8_t PixelR[NUMFLOW], PixelG[NUMFLOW], PixelB[NUMFLOW], C;


#ifdef WS_ARCH_XMEGA

    //  XMEGA specific initialization

    // On XMega setup clock to 32MHz (16 MHz osc. x2 PLL)

    OSC.XOSCCTRL = OSC_FRQRANGE_12TO16_gc|OSC_XOSCSEL_XTAL_16KCLK_gc;
    OSC.CTRL |= OSC_XOSCEN_bm;

    // Wait for it to become stable

    while(! (OSC.STATUS&OSC_XOSCRDY_bm));

    // Enable PLL

    OSC.PLLCTRL = OSC_PLLSRC_XOSC_gc|(2<<OSC_PLLFAC_gp);
    OSC.CTRL |= OSC_PLLEN_bm;

    // Wait for it to become stable

    while(! (OSC.STATUS&OSC_PLLRDY_bm));

    // Use it as new CPU clock

    CCPWrite( &CLK.CTRL, CLK_SCLKSEL_PLL_gc );

    // enable medium level interrupts

    PMIC.CTRL = PMIC_MEDLVLEN_bm;
    sei();

#endif

    // Some initialization for chasing light

    for(I=0; I<NUMFLOW; I++) {
        PixelP[I] = I*(NUMLEDS/NUMFLOW);
        PixelR[I] = 0;
        PixelG[I] = 0;
        PixelB[I] = 0;
    }

    // Init driver stuff

    WS_init();

    // Output loop

    while(1) {

        // Fade all pixels by NUMFADE

        FADE(MyData, NUMFADE);

        // For each "flow" put new pixel, when crossing "0" generate new
        // color

        for(J=0; J<NUMFLOW; J++) {
            if(PixelP[J] == 0) {
                C = (rand()%7)+1;
                PixelR[J] = C&0x01 ? (rand()%BRIGHT)+MINBRIGHT : 0;
                PixelG[J] = C&0x02 ? (rand()%BRIGHT)+MINBRIGHT : 0;
                PixelB[J] = C&0x04 ? (rand()%BRIGHT)+MINBRIGHT : 0;
            }

            PUTRGB(MyData, PixelP[J], PixelR[J], PixelG[J], PixelB[J]);
            PixelP[J] = (PixelP[J]+1)%NUMLEDS;
        }

        // Output

        WS_out(MyData, sizeof(MyData), GammaTable);

        // Delay

        _delay_ms(OUTDELAY);
    }
}
