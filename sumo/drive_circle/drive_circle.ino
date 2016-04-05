#include <Wire.h>
#include <I2Cdev.h>
#include <MPU6050.h>
#include <PID_v1.h>
#include <Servo.h>

//#define GYRO_CAL 235434200	//this has to be measured by rotating the gyro 180 deg. and reading the output
#define GYRO_CAL 58408577	// for 1000 deg/sec this has to be measured by rotating the gyro 180 deg. and reading the output
#define R_ESC_PIN 3
#define L_ESC_PIN 2

//Initialize variables
boolean gyro_flag = false, cal_flag = false, long_flag = false;
long gyro_count = 0, gyro_null=0, accum=0, time=0, timeout = 0;
int angle_diff, angle_last, angle_target, angle_camera, angle=0;
int turn_rate=0;
byte result, state;


double Setpoint, Input, Output;

PID myPID(&Input, &Output, &Setpoint,0.03,0,0, DIRECT);

Servo escR;
Servo escL;


//Initialize objects
MPU6050 accelgyro;

void watch_angle(){
	Serial.println("watch angle");
	while(true) {
		read_FIFO();
		Serial.println(angle);  //watching in radians
		delay(30);
	}
}

void watch_gyro(){
	Serial.println();
	setup_mpu6050();
	calculate_null();

	Serial.println("watch gyro");
	do {
		read_FIFO();

		if((millis()-time)> 250){
			Serial.println(accum);
			time = millis();
		}
	} while(true);		//keep summing until we turn the mode switch off.

	return ;
}

void calculate_null(){
	Serial.println("CALCULATING NULL");
	cal_flag = true;		//calibrating,
	accum = 0;				//reset the angle. angle will act as accumulator for null calculation
	gyro_null = 0;			//make sure to not subtract any nulls here
	gyro_count = 0;

	while(gyro_count < 500)	read_FIFO();

	gyro_null = accum/gyro_count - 1;	//calculate the null. the -30 is a fudge factor for 5000 pts.
	cal_flag = false;		//stop calibration
	accum = 0;
	
	//should print null here
	Serial.println("Null: ");
	Serial.println(gyro_null);
	
	return ;
}

void read_FIFO(){
	//Serial.println("FIFO");
	uint8_t buffer[2];
	long temp = 0;
	int samplz = 0;
	samplz = accelgyro.getFIFOCount() >> 1;
	//Serial.println(samplz,DEC);
	for(int i=0; i < samplz; i++){
		accelgyro.getFIFOBytes(buffer, 2);
		temp = ((((int16_t)buffer[0]) << 8) | buffer[1]);
		accum += temp*10 - gyro_null;    
		//accum += temp;  // - gyro_null;    
		gyro_count++;
		
		if((accum > GYRO_CAL) && (!cal_flag)) accum -= GYRO_CAL*2; //if we are calculating null, don't roll-over
		if((accum < -GYRO_CAL) && (!cal_flag)) accum += GYRO_CAL*2;
	}
	//angle = (float)accum/(float)GYRO_CAL * -3.14159;   //change sign of PI for flipped gyro
	angle = (float)accum/(float)GYRO_CAL * -180;   //using degrees *10, negative for flipped gyro.
	if (temp != 0) turn_rate = temp;

	return ;
}

void setup_mpu6050(){
    // join I2C bus (I2Cdev library doesn't do this automatically)
    #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
        Wire.begin();
    #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
        Fastwire::setup(400, true);
    #endif

    // initialize device
    Serial.println("Initializing I2C devices...");
    accelgyro.initialize();

    // verify connection
    Serial.println("Testing device connections...");
    Serial.println(accelgyro.testConnection() ? "MPU6050 connection successful" : "MPU6050 connection failed");

    // use the code below to change accel/gyro offset values
    accelgyro.setXGyroOffset(7);  //85
    accelgyro.setYGyroOffset(60);  //-70
    accelgyro.setZGyroOffset(44);  //-22
    Serial.print(accelgyro.getXAccelOffset()); Serial.print("\t"); // 
    Serial.print(accelgyro.getYAccelOffset()); Serial.print("\t"); // 
    Serial.print(accelgyro.getZAccelOffset()); Serial.print("\t"); // 
    Serial.print(accelgyro.getXGyroOffset()); Serial.print("\t"); // 
    Serial.print(accelgyro.getYGyroOffset()); Serial.print("\t"); // 
    Serial.print(accelgyro.getZGyroOffset()); Serial.print("\t"); // 
    Serial.print("\n");
    
	Serial.println(F("Setting clock source to Z Gyro..."));
	accelgyro.setClockSource(MPU6050_CLOCK_PLL_ZGYRO);
	//Serial.println(accelgyro.getClockSource(MPU6050_CLOCK_PLL_ZGYRO);

	Serial.println(F("Setting sample rate to 200Hz..."));
	accelgyro.setRate(0); // 1khz / (1 + 4) = 200 Hz

 // *          |   ACCELEROMETER    |           GYROSCOPE
 // * DLPF_CFG | Bandwidth | Delay  | Bandwidth | Delay  | Sample Rate
 // * ---------+-----------+--------+-----------+--------+-------------
 // * 0        | 260Hz     | 0ms    | 256Hz     | 0.98ms | 8kHz
 // * 1        | 184Hz     | 2.0ms  | 188Hz     | 1.9ms  | 1kHz
 // * 2        | 94Hz      | 3.0ms  | 98Hz      | 2.8ms  | 1kHz
 // * 3        | 44Hz      | 4.9ms  | 42Hz      | 4.8ms  | 1kHz
 // * 4        | 21Hz      | 8.5ms  | 20Hz      | 8.3ms  | 1kHz
 // * 5        | 10Hz      | 13.8ms | 10Hz      | 13.4ms | 1kHz
 // * 6        | 5Hz       | 19.0ms | 5Hz       | 18.6ms | 1kHz
 // * 7        |   -- Reserved --   |   -- Reserved --   | Reserved

	Serial.println(F("Setting DLPF bandwidth"));
	accelgyro.setDLPFMode(MPU6050_DLPF_BW_42);

	Serial.println(F("Setting gyro sensitivity to +/- 250 deg/sec..."));
	accelgyro.setFullScaleGyroRange(MPU6050_GYRO_FS_1000);
	//accelgyro.setFullScaleGyroRange(0);  // 0=250, 1=500, 2=1000, 3=2000 deg/sec

	Serial.println(F("Resetting FIFO..."));
	accelgyro.resetFIFO();

	Serial.println(F("Enabling FIFO..."));
	accelgyro.setFIFOEnabled(true);
	accelgyro.setZGyroFIFOEnabled(true);
	accelgyro.setXGyroFIFOEnabled(false);
	accelgyro.setYGyroFIFOEnabled(false);
	accelgyro.setAccelFIFOEnabled(false);
	Serial.print("Z axis enabled?\t"); Serial.println(accelgyro.getZGyroFIFOEnabled());
	Serial.print("x axis enabled?\t"); Serial.println(accelgyro.getXGyroFIFOEnabled());
	Serial.print("y axis enabled?\t"); Serial.println(accelgyro.getYGyroFIFOEnabled());
	Serial.print("accel enabled?\t"); Serial.println(accelgyro.getAccelFIFOEnabled());
	accelgyro.resetFIFO();
	return ;
}

void setup(){
	Wire.begin();
	Serial.begin(115200);
	setup_mpu6050();
	pinMode(9, INPUT_PULLUP);
	pinMode(10, OUTPUT);
	//while(digitalRead(9));
	calculate_null();
	//delay(3200);
	accelgyro.resetFIFO();
	timeout = millis();
	Setpoint = -3000;
	myPID.SetMode(AUTOMATIC);
	myPID.SetSampleTime(20);
	myPID.SetOutputLimits(-500, 500);
	escR.attach(R_ESC_PIN);
	escL.attach(L_ESC_PIN);
//	escL.writeMicroseconds(1550);
//	escR.writeMicroseconds(2000);
//	while (angle > -50) read_FIFO();
	escL.writeMicroseconds(1900);
	escR.writeMicroseconds(1800);
	delay(150);
}

void loop(){
	//watch_angle();
	read_FIFO();
	Input = (double)turn_rate;
	if (myPID.Compute()) {
		escR.writeMicroseconds(Output+1500);
		Serial.println(Input);  //watching in radians

	}
}