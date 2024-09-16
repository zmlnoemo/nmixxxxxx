#include <WiFi.h>
#include <HTTPClient.h>
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include <ArduinoJson.h>

// WiFi 相关配置
const char* ssid = "1111";
const char* password = "20041019";
const char* serverName = "http://192.168.43.251:5000/receive_data";

// 传感器和蜂鸣器的引脚
int sensorPin = 34;  // 假设压力传感器连接到GPIO 34，一定得是ADC2！！！！！！！！
int sensorValue = 0;       // 存储传感器值的变量

int frequency = 0;
int duration = 0;

// 创建一个Web服务器对象在端口80  //另一个传感器是81
AsyncWebServer server(81);

void setup() {
  Serial.begin(115200);  // 初始化串口
  WiFi.begin(ssid, password);  // 连接WiFi
  pinMode(sensorPin, INPUT);   // 设置传感器引脚为输入模式

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

    // WiFi连接成功后，打印IP地址
  Serial.print("Connected, IP Address: ");
  Serial.println(WiFi.localIP());

  // 定义HTTP端点，用于接收音符数据
  server.on("/play_note", HTTP_GET, [](AsyncWebServerRequest *request) {
    // 检查请求参数是否存在
    if (request->hasParam("frequency") && request->hasParam("duration")) {
      int frequency = request->getParam("frequency")->value().toInt();
      int duration = request->getParam("duration")->value().toInt();
      //Serial.print("yessssssssssssssr ");
      // 打印接收到的参数
      Serial.print("Received frequency: ");
      Serial.print(frequency);
      Serial.print(" and duration: ");
      Serial.println(duration);
      request->send(200, "text/plain", "Note played 818181");       //这里也需要改
    } else {
      //Serial.print("Missing frequency or duration parameter ");
      request->send(400, "text/plain", "Missing frequency or duration parameter");
    }
  });

  server.begin();  // 启动服务器
}


void loop() {
  Serial.println("Loop running");  // 添加调试信息
  sensorValue = analogRead(sensorPin);  // 读取传感器值
  
  if (sensorValue > 500) {  // 如果传感器值大于500，发送数据到服务器
    Serial.print("Sensor value: ");
    Serial.println(sensorValue);
    sendDataToServer(sensorValue);
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
    jsonDoc["device_id"] = "ESP32_2";  // 记得改成另一个
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
