#include <Wire.h>
#include <PVision.h>
//#include "Wire.h"

// I2Cdev and MPU6050 must be installed as libraries, or else the .cpp/.h files
// for both classes must be in the include path of your project
#include <I2Cdev.h>
//#include "MPU6050_6Axis_MotionApps20.h"
#include <MPU6050.h>
//#include "new_gyro.h"

//motor directions
#define REVERSE 1
#define FORWARD 2
#define BRAKE 3

//pin definitions
#define PWM_R 5
#define PWM_L 10
#define DIR_R1 6
#define DIR_R2 7
#define DIR_L1 8
#define DIR_L2 9
#define SHARP_PIN 6

#define REV 1
#define FORW 2

// states
#define HUNT 1
#define APPROACH 2
#define ATTACK 3
#define HONING 4
#define LINE_DETECTED 5

//sensor flags
#define LINE_FR		    1
#define LINE_FL		    2
#define LINE_R		    4
#define CAMERA			8
#define SHARP_FAR		16
#define SHARP_CLOSE		32
#define SHARP_HERE		64

//sensor limits
#define SHARP_LIM_FAR	100
#define SHARP_LIM_CLOSE	300


#define NULL_FF -30
#define GYRO_CAL 235434205	//this has to be measured by rotating the gyro 360 deg. and reading the output

boolean gyro_flag = false, cal_flag = false, blob_flag = false, long_flag = false;
long gyro_count = 0, gyro_null=0, accum=0, time=0, count, last_millis;
double angle_diff, angle_last, angle_target, x=0, y=0, angle=0;
const byte InterruptPin = 2 ;		//intterupt on digital pin 2
int speed_current, speed_target, speed_turn, speed_ramp, speed_right, speed_left, steer_gain;
byte result, state, flags;

MPU6050 accelgyro;
PVision ircam;

void updateSpeed(){
	if ((speed_target - speed_current) > 0){
		speed_current += speed_ramp;
		if (speed_current > speed_target) speed_current = speed_target - 1;
	}
	
	else{
		speed_current -= speed_ramp;
		if (speed_current <= speed_target) speed_current = speed_target + 1;
	}
	
	int speed_right = speed_current - speed_turn;
	int speed_left = speed_current + speed_turn;
	
	if (speed_right < 0) dirRight(REV);
	else dirRight(FORW);
	if (speed_left < 0) dirLeft(REV);
	else dirLeft(FORW);
	
	analogWrite(PWM_R, abs(speed_right));
	analogWrite(PWM_L, abs(speed_left));
}

void dirRight(byte direction) {   //sets the direction of the right motor
	switch (direction) {
	case REV:
		digitalWrite(DIR_R1, HIGH);
		digitalWrite(DIR_R2, LOW);
		break;
	case FORW:
		digitalWrite(DIR_R1, LOW);
		digitalWrite(DIR_R2, HIGH);
		break;
	case BRAKE:
		digitalWrite(DIR_R1, HIGH);
		digitalWrite(DIR_R2, HIGH);
		break;
	}
}

void dirLeft(byte direction) {  //sets the direction of the left motor
	switch (direction) {
	case REV:
		digitalWrite(DIR_L1, HIGH);
		digitalWrite(DIR_L2, LOW);
		break;
	case FORW:
		digitalWrite(DIR_L1, LOW);
		digitalWrite(DIR_L2, HIGH);
		break;
	case BRAKE:
		digitalWrite(DIR_L1, HIGH);
		digitalWrite(DIR_L2, HIGH);
		break;
	}
}

boolean checkProcesses(){
	if ((millis() - last_millis) >= 10) {
		last_millis = millis();
		read_FIFO();
		updateSpeed();
		readCamera();
		return true;
	}
	return false;
}

void readCamera(){
	result = ircam.read();
	if (result & BLOB1) {
		angle_target = (512-ircam.Blob1.X) * .0005;
		flags += CAMERA;
	}
	//else blob_flag = false;
}

void testCamera() {
	byte i = 0;
	while (true) {
		//delay 500;
		//Serial.printls("cool");
		if (checkProcesses()) i++;
		if (i > 10){
			i = 0;
			Serial.println(angle_target);
			Serial.println(angle);
		}
	}
}

void testLong(){
	byte i = 0;
	while (true) {
		//delay 500;
		//Serial.printls("cool");
		if (checkProcesses()) i++;
		if (i > 10){
			i = 0;
			Serial.println(analogRead(SHARP_PIN));
		}
	}
	
}

byte hunt(){
	speed_current = 0;
	speed_target = 0;
	speed_turn = 30;
	while(true) {
		flags = 0;
		checkProcesses();
		readLong();
		readLine();
		if (flags & SHARP_FAR) return APPROACH;
		if (flags & SHARP_CLOSE) return ATTACK;
		if (flags & CAMERA) return HONING;
		if (flags & LINE_FR & LINE_FL & LINE_R) return LINE_DETECTED;
	}
}

byte approach(){
	int counter = 500;		//this variable counts-down every time the camera doesn't see anything eventually it times-out
	while(counter) {
		flags = 0;
		checkProcesses();	//1. read gyro 2. update speed 3. read camera
		readLong();
		readLine();
		if (flags & SHARP_FAR) speed_target = 100;
		else if (flags & SHARP_CLOSE) return ATTACK;
		else speed_target = 0;
		if (LINE_FR || LINE_FL|| LINE_R) return LINE_DETECTED;
		if (flags & CAMERA) {
			speed_turn = steer_gain * (angle_target - angle);
			counter = 50;
		}
		else counter -= 1;
	}
	return HUNT;  // if counter reaches 0, nothing has been seen for a while, to go back to hunting.
}

byte attack() {
	
}

void readLong(){			//reads the long range sharp sensor. "flags" should be cleared before calling
	int temp = analogRead(SHARP_PIN);
	if (temp > SHARP_LIM_CLOSE) flags += SHARP_CLOSE;
	else if (temp > SHARP_LIM_FAR) flags += SHARP_FAR;
	// else nothing seen, then nothing
}

void readLine(){
	
}

void testMotors() {
	speed_target = 230;
	for (int i = 0; i < 50; i++) {
		updateSpeed();
		delay(10);
	}
	speed_target = 0;
	for (int i = 0; i < 50; i++) {
		updateSpeed();
		delay(10);
	}
	speed_target = -230;
	for (int i = 0; i < 50; i++) {
		updateSpeed();
		delay(10);
	}
}

void watch_angle(){
	Serial.println();
	setup_mpu6050();
	calculate_null();

	Serial.println("watch angle");
	do {
		read_FIFO();

		if((millis()-time)> 250){
			Serial.println(angle);  //watching in radians
			//Serial.println(angle*180.0/3.14159,5);   /watching in degrees
			//Serial.println(accum);
			time = millis();
		}
	} while(true);		//keep summing unitil we turn the mode switch off.

	return ;
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
	} while(true);		//keep summing unitil we turn the mode switch off.

	return ;
}

void calculate_null(){
	Serial.println("CALCULATING NULL");

	cal_flag = true;		//tell ADC ISR that we are calibrating,
	accum = 0;				//reset the angle. angle will act as accumulator for null calculation
	gyro_null = 0;			//make sure to not subract any nulls here
	gyro_count = 0;

	while(gyro_count < 5000){
		read_FIFO();
		//delay(10);
		//Serial.println(gyro_count);
	}
	gyro_null = accum/gyro_count + NULL_FF;	//calculate the null. the -30 is a fudge factor for 5000 pts.
	cal_flag = false;		//stop calibration
	accum = 0;
	

	//should print null here
	Serial.print("Null: ");
	Serial.println(gyro_null);
	
	return ;
}

void read_FIFO(){
	uint8_t buffer[2];
	long temp = 0;
	int samplz = 0;

	samplz = accelgyro.getFIFOCount() >> 1;
	//Serial.println("FIFO_COUNTH : ");
	//Serial.println(samplz,DEC);
	for(int i=0; i < samplz; i++){
		accelgyro.getFIFOBytes(buffer, 2);
		temp = ((((int16_t)buffer[0]) << 8) | buffer[1]);
		accum -= (temp * 10) + gyro_null;
		gyro_count++;
		
		if((accum > GYRO_CAL) && (!cal_flag)) accum -= GYRO_CAL*2; //if we are calculating null, don't roll-over
		if((accum < -GYRO_CAL) && (!cal_flag)) accum += GYRO_CAL*2;
	}
	angle = (float)accum/(float)GYRO_CAL * 3.14159;

	return ;
}

void setup_mpu6050(){
	// initialize device
	Serial.println("Initializing I2C devices...");
	accelgyro.initialize();

	// verify connection
	Serial.println("Testing device connections...");
	Serial.println(accelgyro.testConnection() ? "MPU6050 connection successful" : "MPU6050 connection failed");
	
	// reset device
	Serial.println(F("\nResetting MPU6050..."));
	accelgyro.reset();
	delay(30); // wait after reset


	// disable sleep mode
	Serial.println(F("Disabling sleep mode..."));
	accelgyro.setSleepEnabled(false);

	// get X/Y/Z gyro offsets
	Serial.println(F("Reading gyro offset values..."));
	int8_t xgOffset = accelgyro.getXGyroOffset();
	int8_t ygOffset = accelgyro.getYGyroOffset();
	int8_t zgOffset = accelgyro.getZGyroOffset();
	Serial.print(F("X gyro offset = "));
	Serial.println(xgOffset);
	Serial.print(F("Y gyro offset = "));
	Serial.println(ygOffset);
	Serial.print(F("Z gyro offset = "));
	Serial.println(zgOffset);

	Serial.println(F("Setting clock source to Z Gyro..."));
	accelgyro.setClockSource(MPU6050_CLOCK_PLL_ZGYRO);

	// Serial.println(F("Setting DMP and FIFO_OFLOW interrupts enabled..."));
	// accelgyro.setIntEnabled(0x12);

	Serial.println(F("Setting sample rate to 200Hz..."));
	accelgyro.setRate(0); // 1khz / (1 + 4) = 200 Hz

	// Serial.println(F("Setting external frame sync to TEMP_OUT_L[0]..."));
	// accelgyro.setExternalFrameSync(MPU6050_EXT_SYNC_TEMP_OUT_L);

	Serial.println(F("Setting DLPF bandwidth to 42Hz..."));
	accelgyro.setDLPFMode(MPU6050_DLPF_BW_42);

	Serial.println(F("Setting gyro sensitivity to +/- 250 deg/sec..."));
	accelgyro.setFullScaleGyroRange(MPU6050_GYRO_FS_250);

	// Serial.println(F("Setting X/Y/Z gyro offsets to previous values..."));
	// accelgyro.setXGyroOffset(xgOffset);
	// accelgyro.setYGyroOffset(ygOffset);
	// accelgyro.setZGyroOffset(61);

	// Serial.println(F("Setting X/Y/Z gyro user offsets to zero..."));
	// accelgyro.setXGyroOffsetUser(0);
	// accelgyro.setYGyroOffsetUser(0);
	//accelgyro.setZGyroOffsetUser(0);
	//Serial.print(F("Z gyro offset = "));
	//Serial.println(accelgyro.getZGyroOffset());

	// Serial.println(F("Setting motion detection threshold to 2..."));
	// accelgyro.setMotionDetectionThreshold(2);

	// Serial.println(F("Setting zero-motion detection threshold to 156..."));
	// accelgyro.setZeroMotionDetectionThreshold(156);

	// Serial.println(F("Setting motion detection duration to 80..."));
	// accelgyro.setMotionDetectionDuration(80);

	// Serial.println(F("Setting zero-motion detection duration to 0..."));
	// accelgyro.setZeroMotionDetectionDuration(0);

	Serial.println(F("Resetting FIFO..."));
	accelgyro.resetFIFO();

	Serial.println(F("Enabling FIFO..."));
	accelgyro.setFIFOEnabled(true);
	accelgyro.setZGyroFIFOEnabled(true);
	
	return ;
}

void setup() {
	ircam.init();
	Serial.begin(115200);
	setup_mpu6050();
	calculate_null();
	pinMode(PWM_R, OUTPUT);   // sets the pin as output
	pinMode(PWM_L, OUTPUT);   // sets the pin as output
	pinMode(DIR_R1, OUTPUT);   // sets the pin as output
	pinMode(DIR_R2, OUTPUT);   // sets the pin as output
	pinMode(DIR_L1, OUTPUT);   // sets the pin as output
	pinMode(DIR_L2, OUTPUT);   // sets the pin as output

}

void loop()
{
	//  readReflectorValues();
	//  sensors.read(sensor_values);
	//watch_angle();
	testLong();
	testCamera();
	speed_current = 0;
	speed_ramp = 30;
	while(true) testMotors();
	
	switch (state) {
	case HUNT:			//No sensors see anything. move until a sensor picks something up
		state = hunt();
		break;

	case APPROACH:
		state = approach();
		break;
		
	case ATTACK:
		state = attack();
		break;
		/*		
	case LINE_DETECTED_RIGHT:
		state = enemyLong();
		break;
		
	case LINE_DETECTED_LEFT:
		state = enemyLongRear();
		break;
		
	case SWITCH_ATTACK:
		state = switchAttack();
		break;
	case SWITCH_ATTACK_REAR:
		state = switchAttackRear();
		break;
	case ATTACK_1:
		state = attack1();
		break;  */
	}
}
