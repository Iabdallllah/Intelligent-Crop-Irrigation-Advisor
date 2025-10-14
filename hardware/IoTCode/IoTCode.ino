#include <Arduino.h>
#include <DHT.h>
#include <LiquidCrystal_I2C.h>
#include <Wire.h>
#include <Keypad.h>
#include <ESP32Servo.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h> // Library for building JSON payload
#include <WiFiClientSecure.h> 

// ======================= 1. NETWORK & CLOUD CONFIG =======================
const char* ssid = "realme 5 Pro";
const char* password = "afmm1234";
const char* mqtt_server = "92c5a082559e4308b31fd91598a72e87.s1.eu.hivemq.cloud"; // Public HiveMQ Broker
const int mqtt_port = 8883;
const char* mqtt_user = "hivemq.webclient.1760050422778"; // Leave blank for public broker hivemq.webclient.1760038209476
const char* mqtt_password = "7i5?<uwOQPR*2ok0Sv,N"; // Leave blank for public broker 3a5S2J.vrxbnI9AVU!#;
const char* mqtt_client_id = "ESP32_Rain_Device_01";
const char* mqtt_topic_publish = "user/7/rain_data";

// Timing for publishing data (milliseconds)
const long publishingInterval = 5000;
long lastPublishTime = 0;

//supabaseURL = "https://fsafbsqnecnehujnptuc.supabase.co"
//ServiceKey ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZzYWZic3FuZWNuZWh1am5wdHVjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1OTk5NzYyNywiZXhwIjoyMDc1NTczNjI3fQ.z6BjvoRdMN1pCkYc0m2OKsqk7cZQzOgOpmLLbcb1j4U"
//MQTTtopic ="user/7/rain_data"

// ======================= 2. HARDWARE PINS & OBJECTS =======================
#define DHTPIN 5
#define DHTTYPE DHT11
#define WATER_PIN 34 // Analog Pin
#define RAIN_PIN 23  // Digital Pin
#define SERVO_PIN 4

LiquidCrystal_I2C lcd(0x27, 16, 2);
DHT dht(DHTPIN, DHTTYPE);
Servo myServo;

// Network clients
//WiFiClient espClient;
//PubSubClient client(espClient);

// Network clients
// WiFiClient espClient; // تم استبدالها
WiFiClientSecure espClient; // <--- استخدام العميل الآمن هنا
PubSubClient client(espClient);

// ======================= 3. KEYPAD CONFIG =======================
const byte ROWS = 4;
const byte COLS = 4;
char keys[ROWS][COLS] = {
  {'1','2','3','A'},
  {'4','5','6','B'},
  {'7','8','9','C'},
  {'*','0','#','D'}
};
byte rowPins[ROWS] = {13, 12, 14, 27};
byte colPins[COLS] = {26, 25, 33, 32};
Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

// ======================= 4. MENU FSM & THRESHOLD =======================
enum State {
  MENU,
  RAIN_STATE,
  DHT_STATE,
  CONTAINER_STATE,
  SERVO_STATE
};
State currentState = MENU;

String menuItems[] = {
  "RainSensor State",
  "DHT11 State",
  "Container State",
  "ServoMotor State"
};
int menuIndex = 0;
int currentServoAngle = 0; // State variable for the servo (0 or 90)

const int WATER_THRESHOLD = 1800;

// ======================= 5. FUNCTION PROTOTYPES =======================
void setup_wifi();
void reconnect_mqtt();
void updateServo(int rain, int water);
void showMenu();
void showState(float temp, float hum, int water, int rain);
void publish_data(float temp, float hum, int water, int rain);

// ======================= 6. WIFI & MQTT IMPLEMENTATION =======================
void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    lcd.setCursor(0,0);
    lcd.print("Connecting WiFi...");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  lcd.setCursor(0,0);
  lcd.print("WiFi Connected    ");
  lcd.setCursor(0,1);
  lcd.print(WiFi.localIP());
  delay(2000);
}

void reconnect_mqtt() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    lcd.setCursor(0,0);
    lcd.print("MQTT Reconnect...");
    lcd.setCursor(0,1);
    
    // Attempt to connect
    if (client.connect(mqtt_client_id, mqtt_user, mqtt_password)) {
      Serial.println("connected");
      lcd.print("Connected!      ");
      delay(1000);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      lcd.print("Failed. Retry.");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

// ======================= 7. HELPER FUNCTIONS =======================
// Servo logic and state tracking (FIXED)
void updateServo(int rain, int water) {
  if (rain == LOW) { // Rain detected
    if (water > WATER_THRESHOLD) {
      myServo.write(0); // close container (full)
      currentServoAngle = 0; 
    } else {
      myServo.write(90); // open to collect
      currentServoAngle = 90; 
    }
  } else {
    myServo.write(0); // no rain -> closed
    currentServoAngle = 0; 
  }
}

void showMenu() {
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Menu");
  lcd.setCursor(0,1);
  lcd.print(menuItems[menuIndex]);
}

// Updated showState to take sensor readings as parameters
void showState(float temp, float hum, int water, int rain) {
  lcd.clear();
  switch(currentState) {
    case RAIN_STATE: {
      lcd.print("RainSensor State");
      lcd.setCursor(0,1);
      if (rain == LOW) lcd.print("Rain detected");
      else lcd.print("No Rain");
      break;
   }
      case DHT_STATE: {
      lcd.print("DHT11 State");
      lcd.setCursor(0,1);
      if (!isnan(temp)) {
        lcd.print("T:"); lcd.print(temp, 1);
        lcd.print(" H:"); lcd.print(hum, 1);
      } else lcd.print("No reading");
      break;
    }
    case CONTAINER_STATE: {
      lcd.print("Container State");
      lcd.setCursor(0,1);
      lcd.print("Value:"); lcd.print(water);
      if (water > WATER_THRESHOLD) lcd.print(" (FULL)");
      else lcd.print(" (OK)");
      break;
    }
    case SERVO_STATE: {
      lcd.print("ServoMotor State");
      lcd.setCursor(0,1); 
      // Use currentServoAngle (the fix)
      lcd.print(currentServoAngle == 90 ? "Opened (90 deg)" : "Closed (0 deg)"); 
      break;
    }
    default: break;
  }
}

void publish_data(float temp, float hum, int water, int rain) {
    // Check for connectivity before publishing
    if (!client.connected()) {
        reconnect_mqtt();
    }

    // StaticJsonDocument size of 200 bytes should be enough for this small payload
    StaticJsonDocument<200> doc;

    doc["temperature"] = temp;
    doc["humidity"] = hum;
    doc["rain_status"] = (rain == LOW) ? "DETECTED" : "NO_RAIN";
    doc["water_status"] = (water > WATER_THRESHOLD) ? "FULL" : "NOT_FULL";
    doc["container_status"] = (currentServoAngle == 0) ? "Closed" : "Opened";

    char jsonBuffer[200];
    serializeJson(doc, jsonBuffer);
    
    // Publish the JSON string
    client.publish(mqtt_topic_publish, jsonBuffer);
    Serial.print("MQTT Published: ");
    Serial.println(jsonBuffer);
}

// ======================= 8. SETUP =======================
void setup() {
  Serial.begin(115200);
  dht.begin();
  lcd.init();
  lcd.backlight();
// ***** الحل الأمني المؤقت: تجاوز التحقق من الشهادة *****
  espClient.setInsecure(); // <--- أضف هذا السطر

  pinMode(WATER_PIN, INPUT);
  pinMode(RAIN_PIN, INPUT);

  myServo.attach(SERVO_PIN);
  myServo.write(0);
  currentServoAngle = 0; // Initialize state variable

  // Setup Wi-Fi and MQTT
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
  // No client.setCallback() needed as we are only publishing

  // Initial LCD display
  showMenu();
}

// ======================= 9. LOOP =======================
void loop() { 
  // 1. Check/Reconnect MQTT
  if (!client.connected()) {
    reconnect_mqtt();
  }
  client.loop();

  // 2. Sensors reading (done less frequently for the DHT11)
  // We read them in the loop and pass the values to helper functions
  float temp = dht.readTemperature();
  float hum = dht.readHumidity();
  int water = analogRead(WATER_PIN);
  int rain = digitalRead(RAIN_PIN);
  
  // 3. Serial Logging (For debugging)
  if (isnan(temp) || isnan(hum)) {
    Serial.println("DHT11 not reading");
  } else {
    Serial.printf("Temp: %.1fC Hum: %.1f%%\n", temp, hum);
  }
  Serial.printf("Water: %d, Rain: %s\n", water, rain == LOW ? "Detected" : "No Rain"); 
  // 4. Servo Control Logic
  updateServo(rain, water);
  
  // 5. MQTT Publishing Timer
  if (millis() - lastPublishTime > publishingInterval) {
    publish_data(temp, hum, water, rain);
    lastPublishTime = millis();
  }

  // 6. Keypad/Menu Logic
  char key = keypad.getKey();
  if (key) {
    if (currentState == MENU) {
      if (key == '#') { // Next
        menuIndex = (menuIndex + 1) % 4;
        showMenu();
      } else if (key == '*') { // Previous
        menuIndex = (menuIndex - 1 + 4) % 4;
        showMenu();
      } else if (key == 'D') { // Enter
        currentState = (State)(menuIndex + 1);
      }
    } else {
      if (key == 'B') { // Back to Menu
        currentState = MENU;
        showMenu();
      }
    }
  }


  // 7. Dynamic Display Update
  if (currentState != MENU) {
    showState(temp, hum, water, rain);
  }

  delay(1000); // Small delay to prevent resource hogging (sensor readings are still fresh)
}
