/***************************************
* function:get the id of RFID key
* RFID   MEGA 2560
* VCC    3.3V
* RST    45
* GND    GND
* MISO   49 Way In & 50 Way Out
* MOSI   51
* SCK    52
* SDA    53 Way In & 48 Way Out
* IRQ    44
****************************************/

#include <AFMotor.h>
#include "rfid1.h"     
#include <LiquidCrystal.h> 

#define TRIG_PIN1 22               
#define ECHO_PIN1 23               
#define TRIG_PIN2 26
#define ECHO_PIN2 27
#define TIME_OUT  5000           
#define LedRed1   30   
#define LedRed2   31
#define LedGreen  34    //alarm of button
#define Buzzer    36 

const int rs = 16, en = 17, d4 = 18, d5 = 19, d6 = 20, d7 = 21;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
String Check_Car_Number; 
unsigned long time;
unsigned int in,out,Check_full = 0;
unsigned int Total_of_car = 6;    //The limited of parking car                    
RFID1 rfid;         //create a variable type of RFID1 
uchar serNum[20];   // array to store your ID
AF_Stepper motor1(255, 1);    // chia quay moi vong la 255 steps o chanel 1&2
AF_Stepper motor2(255, 2);    // chia quay moi vong la 255 steps o chanel 3&4

/*-----------------------------Read Distance WAY IN--------------------------------------------
----------------------------------------------------------------------------------------------*/ 
float GetDistance1()
{
    long duration1, distanceCm1;     
    digitalWrite(TRIG_PIN1, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN1, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN1, LOW);
    Serial.begin(9600);           
    duration1 = pulseIn(ECHO_PIN1, HIGH, TIME_OUT); 
    distanceCm1 = duration1 / 29.1 / 2; 
    return distanceCm1; 
}
/*-----------------------------Read Distance WAY OUT--------------------------------------------
-----------------------------------------------------------------------------------------------*/ 
float GetDistance2()
{
    long duration2, distanceCm2;    
    digitalWrite(TRIG_PIN2, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN2, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN2, LOW);
    Serial.begin(9600);           
    duration2 = pulseIn(ECHO_PIN2, HIGH, TIME_OUT); 
    distanceCm2 = duration2 / 29.1 / 2;  
    return distanceCm2;
}
/*-----------------------------Detect Object WAY IN---------------------------------------------
-----------------------------------------------------------------------------------------------*/ 
int Detect_Object_In()
{   
    int i = 0;
    long distance1 = GetDistance1();
    if (distance1 >= 1 && distance1 <= 15 )
    {
        digitalWrite(LedRed1,HIGH);
        i = 1;
        if (Check_full == Total_of_car)      
        {
            i++;  
        }
    }   
    else
    {
        digitalWrite(LedRed1,LOW);
        lcd.clear();
        i = 0; 
    }
    return i;
}
/*-----------------------------Detect Object WAY OUT--------------------------------------------
-----------------------------------------------------------------------------------------------*/ 
int Detect_Object_Out()
{   
    int o = 0;
    long distance2 = GetDistance2();
    if (distance2 >= 1 && distance2 <= 15 )
    {
        digitalWrite(LedRed2,HIGH);
        o = 1; 
    }
    else
    {
        digitalWrite(LedRed2,LOW);
        o = 0; 
    }
    return o;
}
/*------------------------------------CHECK CARD ID-----------------------------------------------
------------------------------------------------------------------------------------------------*/
int Check_Card_ID()
{
  int Check_ID = 0;
  uchar*id = serNum; 
  /*--------------------------------CARD 1---------------------------------*/ 
  if( id[0] == 0x29 && id[1] == 0x17 && id[2] == 0x8C && id[3] == 0xC1) 
  {
        Check_ID = 1;
        Check_Car_Number = "43E12656";       //License plate 
        tone(Buzzer, 3000, 200);      
  }
  //--------------------------------CARD 2---------------------------------//
  else if( id[0] == 0xE9 && id[1] == 0x7E && id[2] == 0xC5 && id[3] == 0xA2) 
  {
        Check_ID = 1;
        Check_Car_Number = "51E12312";        
        tone(Buzzer, 3000, 200);      
  }
  //--------------------------------CARD 3---------------------------------//
  else if( id[0] == 0xA9 && id[1] == 0x0E && id[2] == 0x8B && id[3] == 0xC1) 
  {
        Check_ID = 1;
        Check_Car_Number = "59F96936";         
        tone(Buzzer, 3000, 200);      
  }
  //--------------------------------CARD 4---------------------------------//
  else if( id[0] == 0x19 && id[1] == 0x91 && id[2] == 0x7A && id[3] == 0xC1) 
  {
        Check_ID = 1;
        Check_Car_Number = "62F30952";          
        tone(Buzzer, 3000, 200);      
  }
  //--------------------------------CARD 5---------------------------------//
  else if( id[0] == 0xE9 && id[1] == 0x5F && id[2] == 0x7A && id[3] == 0xC2) 
  {
        Check_ID = 1;
        Check_Car_Number = "62E02512";       
        tone(Buzzer, 3000, 200);      
  }
  //--------------------------------CARD 6---------------------------------//
  else if( id[0] == 0x29 && id[1] == 0x07 && id[2] == 0xF3 && id[3] == 0xA2) 
  {
        Check_ID = 1;
        Check_Car_Number = "59E07221";      
        tone(Buzzer, 3000, 200);      
  }     
  /*else if("add card ID and license plate here")
  {
        Check_ID = 1;
  }
  */
  else
  {
        Check_ID = 0;
        Check_Car_Number = "0";       //License plate: Nothing      
        tone(Buzzer, 200, 500);     
  } 
  return Check_ID;
}
/*------------------------------------Display LCD-----------------------------------------------
------------------------------------------------------------------------------------------------*/
void Display_LCD()
{
    lcd.clear();
    lcd.print("Occupied:");
    lcd.setCursor(10,0);
    lcd.print(Check_full);
    lcd.setCursor(0,1);
    lcd.print("Empty:");
    lcd.setCursor(7,1);
    lcd.print(Total_of_car - Check_full);  
}   
/*------------------------------------------ MAIN ------------------------------------------------
------------------------------------------------------------------------------------------------*/
void setup()
{
    Serial.begin(9600);
    pinMode(TRIG_PIN1, OUTPUT);
    pinMode(ECHO_PIN1, INPUT);                                     
    pinMode(TRIG_PIN2, OUTPUT);
    pinMode(ECHO_PIN2, INPUT);
    pinMode(Buzzer,OUTPUT);
    pinMode(LedRed1,OUTPUT);
    pinMode(LedRed2,OUTPUT);
    pinMode(LedGreen,OUTPUT);
    motor1.setSpeed(255);
    motor2.setSpeed(255);          
    lcd.begin(16, 2);   
}
void loop()
{    
  int in = Detect_Object_In();
  if (in == 2) 
  {   
      while(in == 2)        
      {
          in = Detect_Object_In();
          out = Detect_Object_Out();
          if (out == 1 )
          {
              goto jump;
          }
      }
  }
  //========================================WAY_IN=============================================//  
  if (in == 1 )
  {               
      rfid.begin( 44, 52,  51,  49, 53, 45);                     
      //rfid.begin(irq,sck,mosi,miso,sda,rst);
      rfid.init();
      uchar status;
      uchar str[MAX_LEN];
      status = rfid.request(PICC_REQIDL, str);
      if (status != MI_OK )
      {
          Display_LCD();
          goto jump;    // After this line Check Way Out  
      } 
      //rfid.showCardType(str);
      status = rfid.anticoll(str);
      if (status == MI_OK)
      {       
          memcpy(serNum, str, 20);
          //rfid.showCardID(str);    // Show card ID
          uchar*id = serNum;               
          int Check = Check_Card_ID();
          if (Check == 1) 
          {      
              //---------------Send Require Check License Plate-----------------//            
              Serial.print("I\n");      // Send require to Raspberry check license plate recognition                       
              time = millis();              
              while(1)    // This is a loop for check RPI can receive the required from Arduino
              {                
                  if (Serial.available() > 0)     // If RPI received then it send back for Arduino confirmation
                  {
                      String data = Serial.readStringUntil('\n');
                      if ((data.equals("I")))                   
                          break;                             
                  }  
                  if ((unsigned long) (millis() - time) > 5000)   // If RPI can't receive command in 5 seconds then return loop
                  {
                      tone(Buzzer, 3000, 100);
                      delay(150);
                      tone(Buzzer, 3000, 100);
                      Display_LCD();
                      goto jump;                        
                  }
              }
              //---------------------------Receive Data-------------------------//
              time = millis(); 
              while(1)
              {
                  if (Serial.available() > 0)      // Receive data frome RPI
                  {
                      String data = Serial.readStringUntil('\n');     // Read up to the last characters of "\n" & save into buffer 
                      if ((data.equals(Check_Car_Number)))        // Compare license plate of a camera with the license plate of UID card
                      {
                          lcd.clear();
                          lcd.print("Correct");
                          tone(Buzzer, 3000, 200);
                          break;                              
                      }
                      else
                      {
                          lcd.clear();
                          lcd.print("Incorrect");
                          tone(Buzzer, 200, 500);
                          Display_LCD();
                          goto jump;  
                      }
                  }
                  if ((unsigned long) (millis() - time) > 10000)   // If Arduino can't receive the license plate in 10 seconds then return loop
                  {
                      tone(Buzzer, 3000, 100);
                      delay(150);
                      tone(Buzzer, 3000, 100);
                      delay(150);
                      tone(Buzzer, 3000, 100);
                      delay(150);
                      tone(Buzzer, 3000, 100);
                      Display_LCD();
                      goto jump;                        
                  }
              }
              //----------------------------------------------------------------//
              motor1.step(510, FORWARD, MICROSTEP);       // Open Barrier 
              time = millis();
              while (in == 1)                             
              {     
                  in = Detect_Object_In(); 
                  out = Detect_Object_Out();
                  if ((unsigned long) (millis() - time) > 5000)   // if the car does not move in the parking in 5 seconds, just close barrier
                  {
                      motor1.step(510, BACKWARD, MICROSTEP);    // Close Barrier 
                      Display_LCD();
                      goto jump;
                  }                                                                  
              }
              Check_full++;             
              digitalWrite(LedGreen,LOW);
              delay(2000);
              motor1.step(510, BACKWARD, MICROSTEP);      // Close Barrier   
          }   
      }  
      rfid.halt();   
      Display_LCD(); 
  }
  //========================================WAY_OUT=============================================//  
  jump:
  int out = Detect_Object_Out();
  if (out == 1)        
  {   
      rfid.begin_1( 44, 52,  51,  50, 48, 45);
      //rfid.begin(irq,sck,mosi,miso,sda,rst);
      rfid.init_1();       
      uchar status_1;
      uchar str[MAX_LEN_1];
      status_1 = rfid.request_1(PICC_REQIDL, str);
      Display_LCD();
      if (status_1 != MI_OK_1)
      {
          return;
      }
      //rfid.showCardType(str);
      status_1 = rfid.anticoll_1(str);
      if (status_1 == MI_OK_1 )                        
      { 
          memcpy(serNum, str, 20);
          //rfid.showCardID(str);   // Show card ID          
          Serial.println();               
          uchar*id = serNum;  
          int Check = Check_Card_ID(); 
          if (Check == 1)
          {               
              //------------------------Send Require Check License Plate------------------------//
              Serial.print("O\n");      // Send require to Raspberry check license plate recognition    
              time = millis();                                  
              while(1)      // This is a loop for check RPI can receive the required from Arduino
              {
                if (Serial.available() > 0)     // If RPI received then it send back for Arduino confirmation  
                {
                  String data = Serial.readStringUntil('\n');
                  if ((data.equals("O")))                 
                      break;                            
                }
                if ((unsigned long) (millis() - time) > 5000)    // If RPI can't receive command in 5 seconds then return loop
                {
                  tone(Buzzer, 3000, 100);
                  delay(150);
                  tone(Buzzer, 3000, 100);
                  Display_LCD();
                  return;                        
                }              
              }
              //-----------------------------------Receive Data---------------------------------//    
              time = millis();                     
              while(1)
              {
                  if (Serial.available() > 0)      //Receive data from RPI
                  {
                      String data = Serial.readStringUntil('\n');     //Read up to the last characters of "\n" & save into buffer 
                      if ((data.equals(Check_Car_Number)))        //Compare license plate of a camera with the license plate of UID card
                      {
                          lcd.clear();
                          lcd.print("Correct");
                          tone(Buzzer, 3000, 200);
                          break;                              
                      }
                      else
                      {
                          lcd.clear();
                          lcd.print("Incorrect");
                          tone(Buzzer, 200, 500);
                          Display_LCD();
                          return;  
                      } 
                  } 
                  if ((unsigned long) (millis() - time) > 10000)   // If Arduino can't receive the license plate in 10 seconds then return loop
                  {
                      tone(Buzzer, 3000, 100);
                      delay(150);
                      tone(Buzzer, 3000, 100);
                      delay(150);
                      tone(Buzzer, 3000, 100);
                      delay(150);
                      tone(Buzzer, 3000, 100);
                      Display_LCD();
                      return;                        
                  }  
              }
              //------------------------------------------------------------------------------//
              motor2.step(510, BACKWARD, MICROSTEP);      //Open Barrier
              time = millis();
              while (out == 1)                           
              {    
                  out = Detect_Object_Out();
                  in = Detect_Object_In();  
                  if ((unsigned long) (millis() - time) > 5000)   //if the car does not move in the parking in 5 seconds, just close barrier
                  {
                      motor2.step(510, FORWARD, MICROSTEP);  // Close Barrier
                      Display_LCD();
                      return;
                  }                                                         
              }
              if(Check_full == 0)   //Check_full is unsigned integer
                  Check_full++;
              Check_full--;
              digitalWrite(LedGreen,LOW);
              delay(2000);
              motor2.step(510, FORWARD, MICROSTEP);     //Close Barrier
          }
      }      
      rfid.halt_1(); 
      Display_LCD();
  }  
}
  
