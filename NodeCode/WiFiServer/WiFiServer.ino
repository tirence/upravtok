// ESP32 open server on port 10000 to receive data structure

#include <WiFi.h>
#include <unordered_map>
//#include <string.h>

 //adjusts both outputs & output_pins for relays
#define outputs 4
const int output_pins[outputs]={32,33,26,27};

//WiFi Credentials
const char* ssid = "debelahlebarka";
const char* password = "D38elAH13bArkA12345678987654321";
const int port=65432;

WiFiServer server(port);  // server port to listen on

void setup() {
  Serial.begin(115200);
  // setup Wi-Fi network with SSID and password
  Serial.printf("Connecting to %s\n", ssid);
  Serial.printf("\nattempting to connect to WiFi network SSID '%s' password '%s' \n", ssid, password);

  for(int i=0; i<outputs; i++){
    pinMode(output_pins[i], OUTPUT); //set relay pin mode
  }

  // attempt to connect to Wifi network:
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    delay(500);
  }
  server.begin();
  //Print out the status after connecting:
  printWifiStatus();
  Serial.print("Listening on port: ");
  Serial.println(port);
}
boolean alreadyConnected = false;  // whether or not the client was connected previously

void loop() {
  static WiFiClient client;
  static int16_t seqExpected = 0;
  if (!client)
    client = server.available();  // Listen for incoming clients

  if (client) {                   // if client connected
    if (!alreadyConnected) {
      // clead out the input buffer:
      client.flush();
      Serial.println("We have a new client");
      alreadyConnected = true;
      delay(50);
    }
    // if data available from client read and display it
    String dataln;
    char out_states[outputs];
    if(client.available()){
      for (int i=0; i<outputs; i++){
        out_states[i] = (char)client.read();
        // dataln+=datach;
        Serial.print(out_states[i]);
      }
    }
    delay(10);
    client.stop();

    for (int i=0; i<outputs; i++){
      if(out_states[i]=='1'){digitalWrite(output_pins[i], LOW);}
      else if(out_states[i]=='0'){digitalWrite(output_pins[i], HIGH);}
    }
  }
}

void printWifiStatus() {
  // print the SSID of the network you're attached to:
  Serial.print("\nSSID: ");
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
}