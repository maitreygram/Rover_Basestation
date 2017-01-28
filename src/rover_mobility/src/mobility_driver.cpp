#include <ros/ros.h>
#include <std_msgs/Float64MultiArray.h>

ros::Publisher ard_pub;

void navCallback(const std_msgs::Float64MultiArray::ConstPtr& msg) {

	std::vector<double> inp = msg -> data;
	float linSpeed = inp[0];
	float angSpeed = inp[1];
	float basemotor = inp[2]
	float shoulderactuator = inp[3];
	float elbowmotor = inp[4];
	float pitchmotor = inp[5];
	float rollmotor = inp[6];
	float grippermotor = inp[7]; 

	std::vector<double> out(16, 0);
	for(int i=0; i<6;i++) {
		out[i] = linSpeed;
	}
	out[6] = angSpeed;
	out[7] = -angSpeed;
	out[8] = -angSpeed;
	out[9] = angSpeed;
	out[10] = basemotor;
	out[11] = shoulderactuator;
	out[12] = elbowmotor;
	out[13] = pitchmotor;
	out[14] = rollmotor
	out[15] = grippermotor

	std_msgs::Float64MultiArray outMsg;
	outMsg.data = out;
	ard_pub.publish(outMsg);
}

int main(int argc, char** argv) {

	ros::init(argc, argv, "mobility_driver");
	ros::NodeHandle _nh;
	
	ard_pub = _nh.advertise<std_msgs::Float64MultiArray>("/rover/ard_directives", 100);
	ros::Subscriber nav_sub = _nh.subscribe("/rover/mobility_directives", 100, navCallback);
	ros::Rate loop_rate(10);

	ros::spin();

	return 0;
}
