#include <SPI.h>
#include <RFID.h>

#define SS_PIN 10
#define RST_PIN 9
#define DELAY_TIME 5000
#define FORCE_PIN A0
#define NUM_CARDS 2

// FLAG TO DETERMINE IF CARD IS VALID
bool access = false;

// TO STORE THE TWO CARDS THAT GIVE ACCESS
int cards[][5] = {
  {73, 130, 172, 133, 226},
  {213,176,95,95,101}
  
};

// CONSTRUCTOR FOR THE RFID CARD
RFID card_read ( SS_PIN, RST_PIN );

void setup(){

    // INITIALIZE SERIAL AND SPI DATA
    Serial.begin(9600);
    SPI.begin();

    // INITIALIZE THE RFID CARD READER
    card_read.init();
   
}

void loop(){

    int press_reading = analogRead( FORCE_PIN ); 
    Serial.print( "Press reading: " );
    Serial.println( press_reading );

//  OUR FSR GOES FROM 10g - 10kg --> .220462 - 22.0462 lb
//  MAP THE VALUE TO BETWEEN THIS RANGE

    float lb_reading = map( press_reading, 0, 1023, .220462, 22.0462 );
    Serial.print( "Lb reading: ");
    Serial.println( lb_reading );
    Serial.println( "------------------------\n");

//  if ( lb_reading > 20 ) Serial.write( "weight" );
//  if ( press_reading > 1000 ) Serial.write( "weight" );

//    THOUGHT ABOUT USING THIS METHODOLOGY..

//    FSR_V = Vcc ( R / (R + FSR_R) ) or FSR_V * ( R + FSR_R) = Vcc * R
//    or ( R + FSR_R ) = Vcc * R / FSR_V or ( ( Vcc * R ) / FSR_V ) - R = FSR_R

//    1.  int voltage_reading = map( press_reading, 0, 1023, 0, 5000 );
//    2.  unsigned long resistance_reading = VOLTAGE_IN - voltage_reading;
//    3.  resistance_reading *= RESISTANCE;
//    4.  resistance_reading /= voltage_reading;

//    AFTER FINDING RESISTANCE, USE LOG GRAPH TO FIND FORCE IN G
//    FROM THERE, COULD CONVERT TO POUNDS
//    DID NOT USE THE BECAUSE NOT NEEDED

    // SEE IF THERE IS A CARD
    if( card_read.isCard() ){

        // READ THE CARD INFO
        if( card_read.readCardSerial() ){

            // SEARCH THROUGH SERIAL NUMBER TO 
            // SEE IF IT IS ONE THAT IS ALLOWED
            for( int j = 0; j < NUM_CARDS; j++ ) {
              for( int i = 0; i < sizeof( card_read.serNum ); i++ ){
                Serial.println( "Card read is: " + String( card_read.serNum[i] ) );
                Serial.println( "Card is: " + String( cards[j][i] ) );
                Serial.println( "-----------------------\n" );

                // IF THERE ISN'T A MATCH, BREAK
                if( card_read.serNum[i] != cards[j][i] ) {
                  access = false;
                  break;
                } else {
                  access = true;
                }
              }

              // IF THERE IS A MATCH ON CARD, BREAKOUT
              // TO KEEP FROM CHECKING OTHER CARD
              if( access ) break;
            }
            
            if ( access ) {
              Serial.println( "Access granted\n" );
              //Serial.write( "granted" );
              delay( DELAY_TIME );
            } else {
              Serial.println( "Access denied\n" );
              //Serial.write( "denied" );
            }
        }
    
    }
    
    card_read.halt();
    delay( 500 );
}


