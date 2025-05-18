#include <DHT.h>

#define DHTPIN D5         // D5 = GPIO14 on Wemos D1 R1
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

int SoilPin = A0;         // 토양 수분 센서
int lightPin = D4;        // D4 = GPIO2
int AA = 10;              // 워터펌프 제어 핀 A
int AB = 6;               // 워터펌프 제어 핀 B

void setup() {
  Serial.begin(115200);
  pinMode(lightPin, OUTPUT);
  pinMode(AA, OUTPUT);
  pinMode(AB, OUTPUT);
  dht.begin();

  Serial.println("🌱 아두이노 스마트팜 시스템 시작됨");
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "LIGHT_ON") {
      digitalWrite(lightPin, HIGH);
      Serial.println("💡 조명 ON");
    } 
    else if (cmd == "LIGHT_OFF") {
      digitalWrite(lightPin, LOW);
      Serial.println("🌙 조명 OFF");
    } 
    else if (cmd == "WATER_ON") {
      Serial.println("🚿 물 주는 중...");
      digitalWrite(AA, HIGH);
      digitalWrite(AB, LOW);
      delay(5000);
      digitalWrite(AA, LOW);
      digitalWrite(AB, LOW);
      Serial.println("✅ 물주기 완료");
    } 
    else if (cmd == "READ_SENSOR") {
      float h = dht.readHumidity();
      float t = dht.readTemperature();
      int moisture = analogRead(SoilPin);

      if (isnan(h) || isnan(t)) {
        Serial.println("❌ DHT 센서 읽기 실패");
      } else {
        Serial.print("TEMP:");
        Serial.print(t);
        Serial.print(" HUMI:");
        Serial.print(h);
        Serial.print(" SOIL:");
        Serial.println(moisture);
      }
    }
  }
}
