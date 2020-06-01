//libraries
#include <SPI.h>
#include <WiFiNINA.h>
#include <Servo.h>
#include "secret.h"

#define MIN_MOTOR_SPEED 100
#define FORWARD_DIR true
#define BACKWARD_DIR false

//SSID of your network
char ssid[] = SECRET_SSID;
char pass[] = SECRET_PWD;

int keyIndex = 0;                 // your network key Index number (needed only for WEP)

int status = WL_IDLE_STATUS;      //connection status
WiFiServer server(80);            //server socket

//special characters
char quote = '"';
char slash = '/';

const double INPUT_MOTOR_RATIO = 255.0 / (255 - MIN_MOTOR_SPEED);  // Joystick ranges from 0-9, Motor ranges from MIN_SPEED-255

const float STEPS_PER_REV = 32;
const float GEAR_RED = 64;
const float STEPS_PER_OUT_REV = STEPS_PER_REV * GEAR_RED;

int stepsRequired;

Servo myServo;

int servoPos = 92;

struct serialInput {
  int val = 0;
  char dir = 'X';
};

int speedPin = 5; 
int dir1Pin = 4;
int dir2Pin = 3;
int ledPin = 2;

char inputDir = 'S';

int motorSpeed = 0;
bool ledStatus = false;

void set_direction(bool dir) {
  if(dir == FORWARD_DIR){
    digitalWrite(dir1Pin, HIGH);
    digitalWrite(dir2Pin, LOW);
  } else {
    digitalWrite(dir1Pin, LOW);
    digitalWrite(dir2Pin, HIGH);
  }
}

serialInput parseWifiInput(WiFiClient &client) {
  serialInput x;
  while(client.available()){
    char c = client.read();
    delay(1);
    if(c == 'F' || c == 'B'){
      x.dir = c;
      x.val = int(client.read());
      if(x.val == 0){
        x.dir = 'S'; // still
      }
    }
  }
  return x;
}

void setup() {
  Serial.begin(9600);      // initialize serial communication

  pinMode(speedPin, OUTPUT);
  pinMode(dir1Pin, OUTPUT);
  pinMode(dir2Pin, OUTPUT);
  pinMode(ledPin, OUTPUT);

  analogWrite(speedPin, 100);

  myServo.attach(9);      
  myServo.write(45);
  
  digitalWrite(ledPin, HIGH);

  // check for the presence of the shield:
  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("WiFi shield not present");
    while (true);       // don't continue
  }

  Serial.print("Attempting to connect to Network named: ");
  Serial.println(ssid);                   // print the network name (SSID);

  // Connect to WPA/WPA2 network. Change this line if using open or WEP network:
  status = WiFi.begin(ssid, pass);

  // attempt to connect to WiFi network:
  while ( status != WL_CONNECTED) {
    delay(1000);
  }
  server.begin();                           // start the web server on port 80
  printWiFiStatus();                        // you're connected now, so print out the status
}


void loop() {

  // attempt to connect to WiFi network:
  while ( status != WL_CONNECTED) {
    Serial.print("Attempting to connect to Network named: ");
    Serial.println(ssid);                   // print the network name (SSID);

    // Connect to WPA/WPA2 network. Change this line if using open or WEP network:
    status = WiFi.begin(ssid, pass);
    // wait 10 seconds for connection:
    delay(10000);
  }

  WiFiClient client = server.available();   // listen for incoming clients

  if (client) {
    Serial.println("new client");
    while(client.connected()) {
      String currentLine = "";
      if(client.available()) {
        serialInput input = parseWifiInput(client);
        Serial.print("Direction: "); Serial.println(input.dir);
        Serial.print("Speed: "); Serial.println(input.val);
      }
      delay(1);
    }
    Serial.println("client disconnected");
  }


}

void printWiFiStatus() {
  // print the SSID of the network you're attached to:
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your WiFi shield's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  // print the received signal strength:
  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
  // print where to go in a browser:
  Serial.print("To see this page in action, open a browser to http://");
  Serial.println(ip);
}
