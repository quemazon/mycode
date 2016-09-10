#include <Audio.h>
#include <Wire.h>
#include <SPI.h>
#include <SD.h>
#include <SerialFlash.h>

// GUItool: begin automatically generated code
AudioSynthWaveformSine   sine1;          //xy=222,301
AudioOutputAnalog        dac1;           //xy=389,327
AudioConnection          patchCord1(sine1, dac1);
// GUItool: end automatically generated code
void setup() {  
  // Audio connections require memory to work. For more  
  // detailed information, see the MemoryAndCpuUsage example  
  AudioMemory(3);  
  }  
  void loop() {  
  sine1.frequency(350); //350  
  sine1.amplitude(0.1);  
  }  

