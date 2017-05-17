/*
  LED & CAPACITANCE CONTROL MODULE
*/
 
// Global Variables
int ledArray[70];
int count;

void setup() {                
  Serial.begin(9600);
  int i;
  for(i=0; i<69; i++){
    ledArray[i] = 0;
  }
  //ledArray[60] = 1;
  for(i=0; i<69; i++){
    ledArray[i] = 3;
  } 
  //ledArray[] = 1;
  PinSetup();
  //digitalWrite(7, LOW); //Uncomment when using this sketch in PCB version
  count = millis();
}

void loop() {
  int i;
  int ledsOn = 0;
  
  //Capacitance Reading Block
  //SPENCER: PUT THIS FIRST IN DATA ACQUIRE BLOCK (SO THAT CAPACITANCE IS ONLY READ WHEN THE TOP LEVEL APP WANTS THE CAPACITANCE DATA)
//  Serial.print("key ; Capacitance: ");
//  Serial.println(touchRead(23));
//  Serial.print("key L Capacitance: ");
//  Serial.println(touchRead(22));
//  Serial.print("key K Capacitance: ");
//  Serial.println(touchRead(19));
//  Serial.print("key S Capacitance: ");
//  Serial.println(touchRead(18));
//  Serial.print("key J Capacitance: ");
//  Serial.println(touchRead(17));
//  Serial.print("key A Capacitance: ");
//  Serial.println(touchRead(16));
//  Serial.print("key F Capacitance: ");
//  Serial.println(touchRead(15));
//  Serial.print("key D Capacitance: ");
//  Serial.println(touchRead(0));
  
  if (touchRead(16) > 4000)
    Serial.print("A  ");
  else
    Serial.print("   ");
  if (touchRead(18) > 4000)
    Serial.print("S  ");
  else
    Serial.print("   ");
  if (touchRead(0) > 4000)
    Serial.print("D  ");
  else
    Serial.print("   ");
  if (touchRead(15) > 4000)
    Serial.print("F  ");
  else
    Serial.print("   ");
  if (touchRead(17) > 4000)
    Serial.print("J  ");
  else
    Serial.print("   ");
  if (touchRead(19) > 4000)
    Serial.print("K  ");
  else
    Serial.print("   ");
  if (touchRead(22) > 4000)
    Serial.print("L  ");
  else
    Serial.print("   ");
  if (touchRead(23) > 4000)
    Serial.print(";");
  else
    Serial.print("   ");
//  touchRead(23); // key ;
//  touchRead(22); // key L
//  touchRead(19); // key K
//  touchRead(18); // key J
//  touchRead(17); // key F
//  touchRead(16); // key D
//  touchRead(15); // key S
//  touchRead(0); //  key A
  Serial.println();
  //Serial.println(micros() - count);
  
  
  //Check for GREEN STATE (1)
  digitalWrite(5, HIGH); //Disable Output for Shift registers
  for (i = 0; i<70; i++){
    if (ledArray[i] > 0){ //Count number of LEDS that are ON.
      ledsOn = ledsOn + 1;
    }
    if (ledArray[i] == 1 || ledArray[i] == 3){
      digitalWrite(2, LOW);
      digitalWrite(3, HIGH);
    }
    else{
      digitalWrite(2, LOW);
      digitalWrite(3, LOW);
    }
    digitalWrite(4, LOW);
    __asm__("nop\n\t""nop\n\t""nop\n\t""nop\n\t""nop\n\t""nop\n\t""nop\n\t""nop\n\t""nop\n\t""nop\n\t""nop\n\t""nop\n\t"); 
    digitalWrite(4, HIGH);
    __asm__("nop\n\t""nop\n\t""nop\n\t""nop\n\t""nop\n\t""nop\n\t""nop\n\t""nop\n\t""nop\n\t""nop\n\t""nop\n\t""nop\n\t");
  }
  digitalWrite(5, LOW); //Enable Output for Shift registers
  delayMicroseconds(1100); //Wait After Green State is set

  //Duty Cycle Adjustment delay (further testing required -> what is max amperage draw possible from usb?)
  //Currently Expects a max current draw of 200mA
  if (ledsOn > 10){
    digitalWrite(5, HIGH); //Disable Output for Shift registers
    //delayMicroseconds(ledsOn*10); //Wait After Red State is set
  }
  
  
  //Check for RED STATE (2)
  digitalWrite(5, HIGH); //Disable Output for Shift registers
  for (i = 0; i<70; i++){
    if (ledArray[i] == 2 || ledArray[i] == 3){
      digitalWrite(2, HIGH);
      digitalWrite(3, LOW);
      //Serial.write("test");
    }
    else{
      digitalWrite(2, LOW);
      digitalWrite(3, LOW);
    }
    digitalWrite(4, LOW);
    __asm__("nop\n\t""nop\n\t""nop\n\t""nop\n\t""nop\n\t""nop\n\t""nop\n\t""nop\n\t""nop\n\t""nop\n\t""nop\n\t""nop\n\t");
    digitalWrite(4, HIGH);
    __asm__("nop\n\t""nop\n\t""nop\n\t""nop\n\t""nop\n\t""nop\n\t""nop\n\t""nop\n\t""nop\n\t""nop\n\t""nop\n\t""nop\n\t");
  }
  digitalWrite(5, LOW); //Enable Output for Shift registers
  delayMicroseconds(1000); //Duty Cycle Delay

  //Duty Cycle Adjustment delay (further testing required -> what is max amperage draw possible from usb?)
  //Currently Expects a max current draw of 200mA
  if (ledsOn > 10){
    digitalWrite(5, HIGH); //Disable Output for Shift registers
    //delayMicroseconds(ledsOn*10);
  }
}

void PinSetup(){
  for (int i = 1; i < 8; i++) {
    pinMode(i, OUTPUT);
  }
}

