#include <DHTesp.h>


//ESP32 things
#include <WiFi.h>
#include <WiFiClient.h>
#include <WebServer.h>
#include <ESPmDNS.h>

const char* ssid = "****";
const char* password = "*****";
// The webserver port
int port=80;

WebServer server(port);

const int led = 16;

//DHT11 things
#include "DHT.h"
#define DHTPIN 22
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

//Other things
float asoilmoist=analogRead(32);//global variable to store exponential smoothed soil moisture reading

void handleRoot() {
  digitalWrite(led, 1);
  String jsonResponse ;
  int sec = millis() / 1000;
  int min = sec / 60;
  int hr = min / 60;
  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  float hum = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float temp = dht.readTemperature();

  // Check if any reads failed and exit early (to try again).
  if (isnan(hum) || isnan(temp)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }
  jsonResponse="{\"ok\":true,\"temp\":" + String(temp)+",\"humid\":"+String(hum)+",\"soil\":"+String(asoilmoist)+"}";
  server.send(200, "application/json", jsonResponse);
}

void handleNotFound() {
  digitalWrite(led, 1);
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET) ? "GET" : "POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";
  for (uint8_t i = 0; i < server.args(); i++) {
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }
  server.send(404, "text/plain", message);
  digitalWrite(led, 0);
  delay(1000);
  digitalWrite(led, 1);
}

void setup(void) {
  pinMode(led, OUTPUT);
  digitalWrite(led, 0);
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  

  if (MDNS.begin("esp32")) {
    Serial.println("MDNS responder started");
  }

  server.on("/", handleRoot);

  server.on("/ping", []() {
    server.send(200, "application/json", "true");
  });

  server.onNotFound(handleNotFound);

  server.begin();
  Serial.println("HTTP server started");
  dht.begin();
  delay(2000);
  
}

void loop(void) {
  asoilmoist=0.95*asoilmoist+0.05*analogRead(32);//exponential smoothing of soil moisture
  server.handleClient(); 
}
