#include <Adafruit_NeoPixel.h>

#define LED_COUNT 150
#define LED_DATA_PIN 3
#define LED_DEFAULT_BRIGHTNESS 25

#define SERIAL_BEGIN_ANIMATION_FRAME_COMMAND 0x199

Adafruit_NeoPixel _pixels = Adafruit_NeoPixel(LED_COUNT, LED_DATA_PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  Serial.begin(9600);
  
  _pixels.begin();
  _pixels.setBrightness(LED_DEFAULT_BRIGHTNESS);

  uint32_t red = _pixels.Color(255, 0, 0);
  uint32_t green = _pixels.Color(0, 255, 0);
  uint32_t blue = _pixels.Color(0, 0, 255);

  _pixels.setPixelColor(0, red);
  _pixels.setPixelColor(1, green);
  _pixels.setPixelColor(2, blue);
  _pixels.show();
}

uint16_t i;

void loop() {
  while (Serial.available() == 0) {
    // Wait for data.
  }

  i = Serial.read();

  // 0x199 <numPixels * 3 bytes>

  if (i == SERIAL_BEGIN_ANIMATION_FRAME_COMMAND) {
    readFrame();
  }
}

uint8_t r, g, b;

void readFrame() {
  for (uint16_t x = 0; x < LED_COUNT; ++x) {
    while (Serial.available() < 3) {
      // Wait for more pixel data.
    }

    r = Serial.read();
    g = Serial.read();
    b = Serial.read();
    _pixels.setPixelColor(x, g, r, b);
  }
  _pixels.show();
}
