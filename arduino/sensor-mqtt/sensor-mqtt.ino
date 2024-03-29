#include <WiFi.h>
#include <PubSubClient.h>
#include <DHTesp.h>
#include <Preferences.h>
#include <ESPmDNS.h>
//DHT11 things
#include "DHT.h"

#define DHTPIN 22
#define DHTTYPE DHT11
#define PIN_SOIL 32

DHT dht(DHTPIN, DHTTYPE);

const int BLUE_LED = 16;

const char* ssid = "";
const char* password = "";
const char* mqttServer = "192.168.1.28";
const int mqttPort = 1883;
const char* mqttUser = "";
const char* mqttPassword = "";
const char* mqttTopic = "homeassistant/esp32/%s_002/state";

float asoilmoist = NAN;
float asoilmoistRaw = NAN;
float humidity = dht.readHumidity();
float temperature = dht.readTemperature();

Preferences preferences;

WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {  
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.print("WiFi connected - ESP IP address: ");
  Serial.println(WiFi.localIP());
}

void smoothValue(float newValue, float& oldValue, String type){
  Serial.println("");
  if(isnan(newValue)) {
    Serial.printf("Failed read NaN for new %s value", type);
    Serial.println("");
  } else {
    Serial.print("Read ");
    Serial.print(newValue);
    Serial.printf(" for new %s value", type);
    Serial.println("");
    if(isnan(oldValue)){
      oldValue = newValue;
    } else {
      oldValue = 0.3*oldValue + 0.7*newValue;   
    }
  }
}

float toPercentage(int value, int valueMin, int valueMax, bool revert, String type) {
  {
    char prefName[100];
    sprintf(prefName, "per.%s", type);
    preferences.begin(prefName, false);
  }
  valueMin = preferences.getInt("min", valueMin);
  valueMax = preferences.getInt("max", valueMax);
  if ( value > valueMax ) {
    valueMax = value;
    Serial.printf("Saving new max: %d\n", valueMax);
    preferences.putInt("max", valueMax);
  } else if ( value < valueMin ) {
    valueMin = value;
    Serial.printf("Saving new min: %d\n", valueMin);
    preferences.putInt("min", valueMin);
  }
  preferences.end();

  Serial.printf("Value: %d, Min: %d, Max: %d\n", value, valueMin, valueMax);

  float per = 100.0 * (value - valueMin) / (valueMax - valueMin);
  if ( revert ) {
    per = 100 - per;
  }

  return per;
}

void readMoisture() { // Fetching data from ADC
  const int nb_readings = 20;
  const int measures_time = 10000;
  int soilMoistureLevel = 0;

  for( int i = 0 ; i < nb_readings; i++ ) {
    int reading = analogRead(PIN_SOIL);
    soilMoistureLevel += reading;
    Serial.printf("Soil moisture (raw): %d (%d)\n", reading, i);
    delay(measures_time/nb_readings);
  }
  soilMoistureLevel /= nb_readings;
  Serial.printf("Soil moisture (raw): %d\n", soilMoistureLevel);

  //exponential smoothing of soil moisture
  asoilmoistRaw = toPercentage(soilMoistureLevel, 1100, 3000, true, "soil");
  if (isnan(asoilmoist)) {
    Serial.println("First time moisture read!");
    asoilmoist = asoilmoistRaw;
  } else {
    asoilmoist = 0.9*asoilmoist + 0.1*asoilmoistRaw;
  }

  Serial.printf("Soil moisture (corrected): %.2f%%\n", asoilmoist);
}

void readTemperature() {
  smoothValue(dht.readTemperature(), temperature, "Temperature");
}

void readHumidity() {
  smoothValue(dht.readHumidity(), humidity, "Humidity");
}

void setup() {
  pinMode(BLUE_LED, OUTPUT);
  digitalWrite(BLUE_LED, 0);
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqttServer, mqttPort);

  dht.begin();
  delay(2000);
}

void loop() {
  if (!client.connected()) {
    digitalWrite(BLUE_LED, 0);
    reconnect();
    digitalWrite(BLUE_LED, 1);
  }
  client.loop();
  Serial.println("");

  readMoisture();
  if(!isnan(asoilmoist) && !isnan(asoilmoistRaw)){
    Serial.printf("Sending moisture %f", asoilmoist);
    Serial.println("");
    publishMoisture(asoilmoist, asoilmoistRaw);
  } else {
    Serial.println("Failed to read mositure");
  }

  // Read the values
  readTemperature();
  if(!isnan(temperature)){
    Serial.printf("Sending temperature %f", temperature);
    Serial.println("");
    publishTemperature(temperature);
  } else {
    Serial.println("Failed to read temperature");
  }

  readHumidity();
  if(!isnan(humidity)){
    Serial.printf("Sending humidity %f", humidity);
    Serial.println("");
    publishHumidity(humidity);
  } else {
    Serial.println("Failed to read humidity");
  }

  delay(10000);  // Wait for 2 seconds before publishing the next message
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32Client", mqttUser, mqttPassword)) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void publishTemperature(float value) {
  char message[50];
  char formattedTopic[50];
  sprintf(message, "{\"ok\":true,\"temp\":%f}", value);
  sprintf(formattedTopic, mqttTopic, "temperature");
  client.publish(formattedTopic, message, true);
}

void publishHumidity(float value) {
  char message[50];
  char formattedTopic[50];
  sprintf(message, "{\"ok\":true,\"humid\":%f}", value);
  sprintf(formattedTopic, mqttTopic, "humidity");
  client.publish(formattedTopic, message, true);
}

void publishMoisture(float avgValue, float rawValue) {
  char message[50];
  char formattedTopic[50];
  sprintf(message, "{\"ok\":true,\"avg\":%f,\"raw\":%f}", avgValue, rawValue);
  sprintf(formattedTopic, mqttTopic, "moisture");
  client.publish(formattedTopic, message, true);
}

