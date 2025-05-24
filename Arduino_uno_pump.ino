#include <DHT.h>

// ✅ 핀 설정
#define DHTPIN 5           // DHT11 센서 연결 핀
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

int SoilPin = A0;          // 토양 수분 센서 (아날로그)
int LightSensorPin = A1;   // ✅ 조도 센서 핀 추가
int lightPin = 4;          // 조명 제어 핀 (릴레이 또는 LED)
int AA = 10;               // 워터펌프 제어 핀 A (모터 드라이버 IN1)
int AB = 6;                // 워터펌프 제어 핀 B (모터 드라이버 IN2)

void setup() {
  Serial.begin(115200);

  pinMode(lightPin, OUTPUT);
  pinMode(AA, OUTPUT);
  pinMode(AB, OUTPUT);

  // ✅ 초기 상태: 모든 장치 OFF
  digitalWrite(lightPin, LOW);
  digitalWrite(AA, HIGH);  // 정지 상태
  digitalWrite(AB, HIGH);  // 정지 상태

  // ✅ 시리얼 버퍼 클리어 (쓰레기 데이터 방지)
  while (Serial.available()) Serial.read();

  dht.begin();
  Serial.println("🌱 아두이노 스마트팜 시스템 시작됨 (UNO)");
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    // ✅ 쓰레기 명령 방어
    if (cmd.length() == 0) return;

    // ✅ 조명 ON
    if (cmd == "LIGHT_ON") {
      digitalWrite(lightPin, HIGH);
      Serial.println("💡 조명 ON");
    }

    // ✅ 조명 OFF
    else if (cmd == "LIGHT_OFF") {
      digitalWrite(lightPin, LOW);
      Serial.println("🌙 조명 OFF");
    }

    // ✅ 워터펌프 제어 (예: WATER:3)
    else if (cmd.startsWith("WATER:") && cmd.length() <= 10 && isDigit(cmd.charAt(6))) {
      int duration = cmd.substring(6).toInt();  // 초 단위 추출
      Serial.print("🚿 물 주는 중... ");
      Serial.print(duration);
      Serial.println("초");

      digitalWrite(AA, HIGH);
      digitalWrite(AB, LOW);
      delay(duration * 1000);

      // ✅ 펌프 정지 (HIGH-HIGH로!)
      digitalWrite(AA, HIGH);
      digitalWrite(AB, HIGH);
      Serial.println("✅ 물주기 완료");
    }

    // ✅ 센서 값 읽기
    else if (cmd == "READ_SENSOR") {
      float h = dht.readHumidity();
      float t = dht.readTemperature();
      int moisture = analogRead(SoilPin);
      int light = analogRead(LightSensorPin);

      if (isnan(h) || isnan(t)) {
        Serial.println("❌ DHT 센서 읽기 실패");
      } else {
        Serial.print("TEMP:");
        Serial.print(t);
        Serial.print(" HUMI:");
        Serial.print(h);
        Serial.print(" SOIL:");
        Serial.println(moisture);
        Serial.print(" LIGHT:");
        Serial.println(light);
      }
    }
  }
}
