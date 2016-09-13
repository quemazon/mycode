//AVC SETTINGS
#define TH			//use either MM (minuteman) or RR (roadrunner)
#define BLUETOOTH 	//use either BLUETOOTH or USB to define the serial port for program output

#define WAYPOINT_COUNT 19
#define WAYPOINTS_STRING \
int excel_waypoints[19][2] = {{96,2456}, {3774,2673}, {8926,2266}, {12349,2266}, {12742,-215}, {12062,-2400}, {4966,-2200}, {235,-2400}, {298,1318}, {315,1412}, {0,0}, {0,0}, {0,0}, {0,0}, {0,0}, {0,0}, {0,0}, {0,0}, {0,0}};

//************************************  MINUTEMAN  ***********************************************************************

#ifdef MM
//WAYPOINT AND SPEED PARAMETERS
// 2015 speeds: 1st waypoint 1780, discombobulator 1820, regular speed 1650
#define WAYPOINT_ACCEPT 185	//waypoint acceptance radius in inches
#define SPEED1 1500				// some default values:
#define SPEED2 1600				//"moderate/slow" speed  1600
							//S1 1500, S2 1560, S3 1580, S4 2000, SB 1250
#define SPEED3 1650				//This is the speed for negotiating wp's 1600
#define SPEED4 1780 			//fast speed 1650
#define SPEED5 1820
#define SPEEDB 1300				//breaking speed default 1300
#define P1 50				//proximity to allow car to align with next waypoint in inches
#define P2 100				//close proximity to waypoint in inches
#define P3 625				//far proximity to waypoint in inches
#define BREAKING_SPEED 4000	//microseconds should be slightly faster than S3 so that the car slows down to S3 and continues at that speed default 6000
#define L1 10
#define L2 27
#define L3 50
#define L4 185
#define SPEED_TOGGLE_ANGLE 20.0
#define XGYROOFFSET 88	//85
#define YGYROOFFSET -72	//-70
#define ZGYROOFFSET -24	//-22
#define PATH_FOLLOWING 1
#define LOOK_AHEAD 80


//SENSOR PARAMETERS
//#define GYRO_CAL 470868410	//this has to be measured by rotating the gyro 360 deg. and reading the output
//#define GYRO_CAL 235434205		//this has to be measured by rotating the gyro 360 deg. and reading the output
#define GYRO_CAL 233300000		//this has to be measured by rotating the gyro 360 deg. and reading the output
#define STEER_ADJUST 1425		//steering adjustment factor. ***THIS IS JUST A PLACE HOLDER FOR NOW***
#define SERVO_LIM 300			//limits the swing of the servo so it does not get overstressed, default 300
#define STEER_GAIN 300.0			//proportional gain, default it 4.0
#define CLICK_INCHES 4.66		//used to determine the number of inches per click originally set to 2.33

//FIXED PARAMETERS
#define CAR_NAME "***MINUTEMAN***" //car name
#define CLICK_MAX 2			//in the main loop, watch clicks and wait for it to reach CLICK_MAX, then calculate position, default 3
#define WP_SIZE 20 			//number of bytes for each waypoint

//Teensy Pin Assignments:
//Optional manual throttle, autonomous steering - connect ESC signal pin to receiver CH2
#define RESET_PIN 2
#define MODE_LINE_1 5
#define MODE_LINE_2 6
#define FRICKIN_LASER 11
#define THROTTLE 20
#define STEERING 21
#define HALL_EFFECT_SENSOR 22
#define TOGGLE 23

//CH3 settings
#define MANUAL 0
#define AUTOMATIC 1
#define WP_MODE 2
#define AUX 3
#define RESET 4
#endif

//************************************  Tomahawk  ***********************************************************************

#ifdef TH
//WAYPOINT AND SPEED PARAMETERS
#define WAYPOINT_ACCEPT 185	//waypoint acceptance radius in inches
#define WAYPOINT_ACCEPT 185	//waypoint acceptance radius in inches
#define SPEED1 1500				// some default values:
#define SPEED2 1600				//"moderate/slow" speed  1600
							//S1 1500, S2 1560, S3 1580, S4 2000, SB 1250
#define SPEED3 1650				//This is the speed for negotiating wp's 1600
#define SPEED4 1780 			//fast speed 1650
#define SPEED5 1820
#define SPEEDB 1300				//breaking speed default 1300
#define P1 50				//proximity to allow car to align with next waypoint in inches
#define P2 100				//close proximity to waypoint in inches
#define P3 625				//far proximity to waypoint in inches
#define BREAKING_SPEED 4000	//microseconds should be slightly faster than S3 so that the car slows down to S3 and continues at that speed default 6000
#define L1 0
#define L2 30
#define L3 100
#define L4 100
#define SPEED_TOGGLE_ANGLE 10.0
#define XGYROOFFSET 88	//85
#define YGYROOFFSET -72	//-70
#define ZGYROOFFSET -24	//-22
#define PATH_FOLLOWING 1
#define LOOK_AHEAD 80


//SENSOR PARAMETERS
//#define GYRO_CAL 470868410	//this has to be measured by rotating the gyro 360 deg. and reading the output
//#define GYRO_CAL 235434205		//this has to be measured by rotating the gyro 360 deg. and reading the output
#define GYRO_CAL 233300000		//this has to be measured by rotating the gyro 360 deg. and reading the output
//#define STEER_ADJUST 1565		//steering adjustment factor. ***THIS IS JUST A PLACE HOLDER FOR NOW***
#define STEER_ADJUST 1500		//steering adjustment factor. ***THIS IS JUST A PLACE HOLDER FOR NOW*** 1565
#define SERVO_LIM 300			//limits the swing of the servo so it does not get overstressed, default 300
#define STEER_GAIN 300.0			//proportional gain, default it 4.0
#define CLICK_INCHES 3.1		//used to determine the number of inches per click originally set to 2.33

//FIXED PARAMETERS
#define CAR_NAME "***QUIXOTE FORWARD***" //car name
#define CLICK_MAX 1			//in the main loop, watch clicks and wait for it to reach CLICK_MAX, then calculate position, default 3
#define WP_SIZE 20 			//number of bytes for each waypoint

//Teensy Pin Assignments:
//Optional manual throttle, autonomous steering - connect ESC signal pin to receiver CH2
#define RESET_PIN 2
#define MODE_LINE_1 5
#define MODE_LINE_2 6
#define FRICKIN_LASER 11
#define THROTTLE 20
#define STEERING 21
#define HALL_EFFECT_SENSOR 22
#define TOGGLE 23

//CH3 settings
#define MANUAL 0
#define AUTOMATIC 1
#define WP_MODE 2
#define AUX 3
#define RESET 4
#endif


//************************************  QUIXOTE FORWARD  ***********************************************************************

#ifdef QF
//WAYPOINT AND SPEED PARAMETERS
#define WAYPOINT_ACCEPT 185	//waypoint acceptance radius in inches
#define S1 1500				// some default values:
#define S2 1550				//S1 1500, S2 1540, S3 1560, S4 1600, S5 1650, SB 1300
							//S1 1500, S2 1560, S3 1580, S4 2000, SB 1250
#define S3 1600				//This is the speed for negotiating wp's 
#define S4 1565 			//1680 is pretty ridiculously fast. Don't use for general use. maybe try 1650, 1720 fastest
#define SB 1300				//breaking speed default 1300
#define P1 50				//proximity to allow car to align with next waypoint in inches
#define P2 100				//close proximity to waypoint in inches
#define P3 625				//far proximity to waypoint in inches
#define BREAKING_SPEED 4000	//microseconds should be slightly faster than S3 so that the car slows down to S3 and continues at that speed default 6000
#define L1 0
#define L2 30
#define L3 100
#define L4 100
#define SPEED_TOGGLE_ANGLE 10.0
#define XGYROOFFSET 88	//85
#define YGYROOFFSET -72	//-70
#define ZGYROOFFSET -24	//-22
#define PATH_FOLLOWING 1
#define LOOK_AHEAD 80


//SENSOR PARAMETERS
//#define GYRO_CAL 470868410	//this has to be measured by rotating the gyro 360 deg. and reading the output
//#define GYRO_CAL 235434205		//this has to be measured by rotating the gyro 360 deg. and reading the output
#define GYRO_CAL 233300000		//this has to be measured by rotating the gyro 360 deg. and reading the output
//#define STEER_ADJUST 1565		//steering adjustment factor. ***THIS IS JUST A PLACE HOLDER FOR NOW***
#define STEER_ADJUST 1582		//steering adjustment factor. ***THIS IS JUST A PLACE HOLDER FOR NOW*** 1565
#define SERVO_LIM 300			//limits the swing of the servo so it does not get overstressed, default 300
#define STEER_GAIN -300.0			//proportional gain, default it 4.0
#define CLICK_INCHES 5.1		//used to determine the number of inches per click originally set to 2.33

//FIXED PARAMETERS
#define CAR_NAME "***QUIXOTE FORWARD***" //car name
#define CLICK_MAX 2			//in the main loop, watch clicks and wait for it to reach CLICK_MAX, then calculate position, default 3
#define WP_SIZE 20 			//number of bytes for each waypoint

//Teensy Pin Assignments:
//Optional manual throttle, autonomous steering - connect ESC signal pin to receiver CH2
#define RESET_PIN 2
#define MODE_LINE_1 5
#define MODE_LINE_2 6
#define FRICKIN_LASER 11
#define THROTTLE 20
#define STEERING 21
#define HALL_EFFECT_SENSOR 22
#define TOGGLE 23

//CH3 settings
#define MANUAL 0
#define AUTOMATIC 1
#define WP_MODE 2
#define AUX 3
#define RESET 4
#endif



#ifdef BLUETOOTH
#define SERIAL_OUT Serial2
#endif

#ifdef USB
#define SERIAL_OUT Serial	
#endif

