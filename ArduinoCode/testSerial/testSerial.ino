
int ledPin = 2;
int resetPin = 4;

bool light_mode = false;

void toggle_light(int mode=-1){
  if (mode == 1)
  {
    digitalWrite(ledPin, HIGH);
    light_mode = true;
  }
  else if (mode == 0)
  {
    digitalWrite(ledPin, LOW);
    light_mode = false;
  }
  else
  {
    digitalWrite(ledPin, light_mode ? LOW : HIGH);
    light_mode = !light_mode;
  }
}

void setup() {
    digitalWrite(resetPin, HIGH);
    
    pinMode(ledPin, OUTPUT);
    pinMode(resetPin, OUTPUT);
    
    Serial.begin(115200);
    Serial.print("initializing");

    for(int i = 0; i < 3; i++) {
      toggle_light(); // Turn on LED
      delay(100);
      toggle_light(); // Turn off LED
      delay(100);
    }
}

void loop() {

    if(Serial.available()){
        char c = Serial.read();
        if(c == 'T'){
          toggle_light();
        } else if (c == 'I') {
          toggle_light(1);
        } else if (c == 'O') {
            toggle_light(0);
        } else if (c == 'R') { // reset
          digitalWrite(resetPin, LOW);
        }
        Serial.print(c);
        while(Serial.available()) { Serial.read(); }
    }
}
