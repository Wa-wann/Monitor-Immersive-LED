#include <Adafruit_NeoPixel.h>
Adafruit_NeoPixel strip = Adafruit_NeoPixel(50, 6, NEO_GRB + NEO_KHZ800);

//Déclaration des variables globales//
char tab[800];

boolean receive=1;
boolean treat=1;

int i=0;
int j=0;
int k=0;

int value=0;
int value_r=0;
int value_g=0;
int value_b=0;
int pos=0;

char color;

//End of declaration//


void setup() {
  Serial.begin(500000);
  strip.begin();
  delay(3000);
}

void loop() {
  while (Serial.available() > 0)
  {Serial_read();}
  
  if (receive==1 && treat==0)
  {translation();}
  
  if(receive && treat)
  { 
    Light_led();
    i=0;
    receive=0;
    treat=0;
    Serial.write(0);
  }
}


void translation(void)
{
  for(int k=0;k<i;k++)
  {
    //Serial.print("on traite \n\r");
      switch (tab[k]) {
        case ',':
          Led_color();
          break;
          
        case '#':
          //strip.show();
          treat=1;
          j=0;
          break;
          
        case '$':
          color='r';
          break;
          
        default:
       
          break;
        }
      
      }
  i=0;
}


void Serial_read(void)
{
  tab[i] = Serial.read(); 
  if (tab[i] == '#')
  {
    receive=1;
    treat=0;
  }
  i+=1;
}

void Light_led(void)
{
  strip.setBrightness(100);
  strip.show();
}

void Led_color(void)
{
  if (color=='b'){
    value_b=value;
    strip.setPixelColor(j,value_r,value_g,value_b);
    j+=1;
    pos=0;
    value=0;
    }
    
  if (color=='g'){
    value_g=value;
    color='b';
    value=0;
    pos=0;
    }
    
  if (color=='r'){
    value_r=value;
    color='g';
    value=0;
    pos=0;
    }
}

void Char2Int (void){
  if(tab[k]>= 48 && tab[k] <=57)  //48 represente le zero et 57 le 9
          {
          pos+=1;
          if (pos==1){
            value=(int)tab[k]-48;}
          if (pos==2){
            value=value*10+(int)tab[k]-48;}
          if (pos==3){
            value=value*10+(int)tab[k]-48;}
          }
}
