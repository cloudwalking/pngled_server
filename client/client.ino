#include <Adafruit_NeoPixel.h>

#define LED_COUNT 150
#define LED_DATA_PIN 3
#define LED_DEFAULT_BRIGHTNESS 25

#define SERIAL_START_COMMAND 0x60
#define SERIAL_BEGIN_ANIMATION_FRAME_COMMAND 0x0

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

uint8_t i;

void loop() {
  while (Serial.available() <= 2) {
    // Wait for data.
  }

  i = Serial.read();

  // 0x60 0x00 <numPixels * 3 bytes>

  if (i != SERIAL_START_COMMAND) {
    return;
  }

  i = Serial.read();

  if (i == SERIAL_BEGIN_ANIMATION_FRAME_COMMAND) {
    readFrame();
  }
}

uint8_t r, g, b;

void readFrame() {
  for (uint8_t x = 0; x < LED_COUNT; ++x) {
    while (Serial.available() < 3) {
      // Wait for more pixel data.
    }

    r = Serial.read();
    g = Serial.read();
    b = Serial.read();
    _pixels.setPixelColor(x, r, g, b);
  }
  _pixels.show();
}
