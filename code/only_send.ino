#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// WiFi 相关配置
const char* ssid = "1111";
const char* password = "20041019";
//const char* serverName = "http://192.168.43.133:5000/receive_data";
const char* serverName = "http://192.168.43.251:5000/receive_data";
//const char* serverName = "http://192.168.80.129:5000/receive_data";

// 传感器引脚
int sensorPin = 34;  // 假设压力传感器连接到GPIO 34
int led = 14;   //指示灯
int sensorValue = 0;  // 存储传感器值的变量

void setup() {
  Serial.begin(115200);  // 初始化串口
  WiFi.begin(ssid, password);  // 连接WiFi
  pinMode(sensorPin, INPUT);  // 设置传感器引脚为输入模式
  pinMode(led,OUTPUT);
  digitalWrite(led, LOW);

  // 尝试连接WiFi，超时时间为10秒
  unsigned long startAttemptTime = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - startAttemptTime < 10000) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }

  // 检查WiFi是否连接成功
  if (WiFi.status() == WL_CONNECTED) {
    Serial.print("Connected, IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("Failed to connect to WiFi");
  }
}

void loop() {
  sensorValue = analogRead(sensorPin);  // 读取传感器值
  
  if (sensorValue > 300) {  // 如果传感器值大于300，发送数据到服务器
    Serial.print("Sensor value: ");
    Serial.println(sensorValue);
    
    digitalWrite(led, HIGH);
    sendDataToServer(sensorValue);
    delay(500);                   
    digitalWrite(led, LOW);
  } else {
    Serial.print("Sensor value too low: ");
    Serial.println(sensorValue);
  }
  delay(100);  // 延时100毫秒
}

void sendDataToServer(int sensorValue) {
  if (WiFi.status() == WL_CONNECTED) {  // 检查WiFi连接状态
    HTTPClient http;
    http.begin(serverName);  // 初始化HTTP请求
    http.addHeader("Content-Type", "application/json");  // 设置HTTP头

    // 创建JSON对象
    StaticJsonDocument<200> jsonDoc;
    jsonDoc["device_id"] = "ESP32_4";  // 记得改成另一个!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    jsonDoc["sensor_value"] = sensorValue;
    
    // 序列化JSON对象
    String jsonString;
    serializeJson(jsonDoc, jsonString);
    
    int httpResponseCode = http.POST(jsonString);  // 发送HTTP POST请求
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);  // 打印HTTP响应码
    http.end();  // 结束HTTP请求
  } else {
    Serial.println("WiFi not connected");  // WiFi未连接
  }
}
