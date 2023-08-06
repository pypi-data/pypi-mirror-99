Feature: eikon login test
	Set of functional tests on the connection to the daemon
	Typically, what happens when the Application ID is not set
	When the daemon is disconnected...
	
	Scenario: Set the application ID and send a request
		Given the daemon is running
		And application ID is set with a valid EPAID
		When a JSON request is sent
		Then a successful response is received

# following scenario cannot succeed because all App IDs are valid
#	Scenario: Invalid application ID
#		Given the daemon is running
#		And application ID is set with an invalid EPAID
#		When a JSON request is sent
#		Then an exception EikonError is raised with text: "Application ID is not valid"

	Scenario: Application ID not set
		Given the daemon is running
		And application ID is not set		
		When a JSON request is sent
		Then an exception EikonError is raised with text: 'EPAID not set'

	Scenario: Send a request while daemon is not running
		Given the daemon is not running
		When a JSON request is sent
		Then an exception EikonError is raised with text: 'EPAID not set'
