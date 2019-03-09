/*----------------------------------------------------------------------------
 Copyright:      Radig Ulrich  mailto: mail@ulrichradig.de
 Author:         Radig Ulrich
 Remarks:
 known Problems: none
 Version:        27.09.2007
 Description:    RGB-LED Farbenspiel
----------------------------------------------------------------------------*/

#include <avr/interrupt.h>
#include <avr/io.h>

/*
Pin 1: ADC0, PB5
Pin 2: ADC3, PB3
Pin 3: ADC2, PB4
Pin 5: PB0
Pin 6: PB1
Pin 7: ADC1, PB2

*/

// PB2: Pin 7, PB1: Pin 6, PB0: Pin5
#define LED_R   (1 << 2)
#define LED_G   (1 << 1)
#define LED_B   (1 << 0)

// ADC2 and ADC3
#define CTRL_R  2
#define CTRL_G  3
#define CTRL_B  0

#if defined (__AVR_ATtiny45__) || defined (__AVR_ATtiny85__)
    #define TIMER0_OVF0_vect TIMER0_OVF_vect
    #define TCCR0 TCCR0B
#endif


volatile char pwm_counter, pwm_r, pwm_g, pwm_b, channel;

//----------------------------------------------------------------------------
ISR (TIMER0_OVF0_vect)
{
    if (pwm_counter++ > 63)
    {
        PORTB = 0x00;
        pwm_counter = 0;
    }
    if (pwm_counter > pwm_r) PORTB |= LED_R;
    if (pwm_counter > pwm_g) PORTB |= LED_G;
    if (pwm_counter > pwm_b) PORTB |= LED_B;
}
//----------------------------------------------------------------------------
//Hauptprogramm
int main (void)
{
    CLKPR = _BV(CLKPCE);
    CLKPR = 0;

    //Port für LED auf output
    DDRB = LED_R|LED_G|LED_B;

    //Interrupt for the Clock enable
    TIMSK |= (1 << TOIE0);
    //Setzen des Prescaler auf 1024
    TCCR0 |= (1<<CS00 | 0<<CS01 | 0<<CS02);
    //TCNT0 = 65535 - (OSC_CLK / 1024);

    channel = 0;
    ADCSRA = _BV(ADEN);
    ADMUX = 0x20 | _BV(CTRL_R); // set ADLAR, set Vref to VCC, input channel
    ADCSRA |= _BV(ADSC); // start conversion

    sei();

    pwm_r = 0;
    pwm_g = 0;
    pwm_b = 0;

    while(1)
    {
        if (bit_is_set(ADCSRA, ADIF)) {
            if (channel == 0) {
                pwm_g = ADCH >> 2;
                ADMUX = CTRL_G;
            }
            else if (channel == 1) {
                pwm_r = ADCH >> 2;
                ADMUX = CTRL_B;
            }
            else {
                pwm_b = ADCH - 230;
                ADMUX = CTRL_R;
            }
            channel += 1;
            if (channel > 3) {
                channel = 0;
            }
            ADMUX |= 0x20;
            ADCSRA |= _BV(ADIF);
            ADCSRA |= _BV(ADSC); // start conversion
        }
    }
}

