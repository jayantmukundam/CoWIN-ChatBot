
# No other modules apart from 'socket', 'BeautifulSoup', 'requests' and 'datetime'
# need to be imported as they aren't required to solve the assignment

# Import required module/s
import socket
from bs4 import BeautifulSoup
import requests
import datetime



# Define constants for IP and Port address of Server
# NOTE: DO NOT modify the values of these two constants
HOST = '127.0.0.1'
PORT = 24680


def fetchWebsiteData(url_website):
	"""Fetches rows of tabular data from given URL of a website with data excluding table headers.

	Parameters
	----------
	url_website : str
		URL of a website

	Returns
	-------
	bs4.element.ResultSet
		All rows of Tabular data fetched from a website excluding the table headers
	"""
	
	web_page_data = ''

	##############	ADD YOUR CODE HERE	##############
	req = requests.get(url_website)
	soup = BeautifulSoup(req.text, 'html.parser')
	web_page_data=soup.tbody.find_all('tr')
	##################################################

	return web_page_data


def fetchVaccineDoses(web_page_data):
	"""Fetch the Vaccine Doses available from the Web-page data and provide Options to select the respective Dose.

	Parameters
	----------
	web_page_data : bs4.element.ResultSet
		All rows of Tabular data fetched from a website excluding the table headers

	Returns
	-------
	dict
		Dictionary with the Doses available and Options to select, with Key as 'Option' and Value as 'Command'
	
	Example
	-------
	>>> url_website = "https://www.mooc.e-yantra.org/task-spec/fetch-mock-covidpage"
	>>> web_page_data = fetchWebsiteData(url_website)
	>>> print(fetchVaccineDoses(web_page_data))
	{'1': 'Dose 1', '2': 'Dose 2'}
	"""

	vaccine_doses_dict = {}

	##############	ADD YOUR CODE HERE	##############
	for i in web_page_data:
		j=i.find_all(class_='dose_num')
		for k in j:
			num_string=k.contents[0]
			dose_string = 'Dose '+num_string
			vaccine_doses_dict[num_string]=dose_string 
	##################################################

	return vaccine_doses_dict


def fetchAgeGroup(web_page_data, dose):
	"""Fetch the Age Groups for whom Vaccination is available from the Web-page data for a given Dose
	and provide Options to select the respective Age Group.

	Parameters
	----------
	web_page_data : bs4.element.ResultSet
		All rows of Tabular data fetched from a website excluding the table headers
	dose : str
		Dose available for Vaccination and its availability for the Age Groups

	Returns
	-------
	dict
		Dictionary with the Age Groups (for whom Vaccination is available for a given Dose) and Options to select,
		with Key as 'Option' and Value as 'Command'
	
	Example
	-------
	>>> url_website = "https://www.mooc.e-yantra.org/task-spec/fetch-mock-covidpage"
	>>> web_page_data = fetchWebsiteData(url_website)
	>>> print(fetchAgeGroup(web_page_data, '1'))
	{'1': '18+', '2': '45+'}
	>>> print(fetchAgeGroup(web_page_data, '2'))
	{'1': '18+', '2': '45+'}
	"""

	age_group_dict = {}

	##############	ADD YOUR CODE HERE	##############
	age_group_set=set()
	for i in range(len(web_page_data)):
		
		dose_tag=web_page_data[i].find_all(class_='dose_num')[0]
		dose_content=dose_tag.contents[0]
		if dose_content==dose:
			age_group_tag=dose_tag.next_sibling.next_sibling
			age_group=age_group_tag.contents[0]
			
			age_group_set.add(age_group)

	age_group_set=sorted(age_group_set)
	j=1	
	for i in age_group_set:
		age_group_dict[str(j)]=i 
		j=j+1

	##################################################

	return age_group_dict


def fetchStates(web_page_data, age_group, dose):
	"""Fetch the States where Vaccination is available from the Web-page data for a given Dose and Age Group
	and provide Options to select the respective State.

	Parameters
	----------
	web_page_data : bs4.element.ResultSet
		All rows of Tabular data fetched from a website excluding the table headers
	age_group : str
		Age Group available for Vaccination and its availability in the States
	dose : str
		Dose available for Vaccination and its availability for the Age Groups

	Returns
	-------
	dict
		Dictionary with the States (where the Vaccination is available for a given Dose, Age Group) and Options to select,
		with Key as 'Option' and Value as 'Command'
	
	Example
	-------
	>>> url_website = "https://www.mooc.e-yantra.org/task-spec/fetch-mock-covidpage"
	>>> web_page_data = fetchWebsiteData(url_website)
	>>> print(fetchStates(web_page_data, '18+', '1'))
	{
		'1': 'Andhra Pradesh', '2': 'Arunachal Pradesh', '3': 'Bihar', '4': 'Chandigarh', '5': 'Delhi', '6': 'Goa',
		'7': 'Gujarat', '8': 'Harayana', '9': 'Himachal Pradesh', '10': 'Jammu and Kashmir', '11': 'Kerala', '12': 'Telangana'
	}
	"""

	states_dict = {}

	##############	ADD YOUR CODE HERE	##############
	state_set=set()
	
	for i in range(len(web_page_data)):
		
		dose_tag=web_page_data[i].find_all(class_='dose_num')[0]
		dose_content=dose_tag.contents[0]
		if dose_content==dose:
			parent_tag=dose_tag.parent
			curr_age_group=parent_tag.find(class_='age').contents[0]
			if curr_age_group==age_group:
				curr_state=parent_tag.find(class_='state_name').contents[0]
				state_set.add(curr_state)
	
	state_set=sorted(state_set)
	j=1	
	for i in state_set:
		states_dict[str(j)]=i 
		j=j+1
		
##################################################

	return states_dict


def fetchDistricts(web_page_data, state, age_group, dose):
	"""Fetch the District where Vaccination is available from the Web-page data for a given State, Dose and Age Group
	and provide Options to select the respective District.

	Parameters
	----------
	web_page_data : bs4.element.ResultSet
		All rows of Tabular data fetched from a website excluding the table headers
	state : str
		State where Vaccination is available for a given Dose and Age Group
	age_group : str
		Age Group available for Vaccination and its availability in the States
	dose : str
		Dose available for Vaccination and its availability for the Age Groups

	Returns
	-------
	dict
		Dictionary with the Districts (where the Vaccination is available for a given State, Dose, Age Group) and Options to select,
		with Key as 'Option' and Value as 'Command'
	
	Example
	-------
	>>> url_website = "https://www.mooc.e-yantra.org/task-spec/fetch-mock-covidpage"
	>>> web_page_data = fetchWebsiteData(url_website)
	>>> print(fetchDistricts(web_page_data, 'Ladakh', '18+', '2'))
	{
		'1': 'Kargil', '2': 'Leh'
	}
	"""

	districts_dict = {}

	##############	ADD YOUR CODE HERE	##############
	district_set=set()
	
	for i in range(len(web_page_data)):
		
		dose_tag=web_page_data[i].find_all(class_='dose_num')[0]
		dose_content=dose_tag.contents[0]
		if dose_content==dose:
			parent_tag=dose_tag.parent
			curr_age_group=parent_tag.find(class_='age').contents[0]
			if curr_age_group==age_group:
				curr_state=parent_tag.find(class_='state_name').contents[0]
				if curr_state==state:
					curr_district=parent_tag.find(class_='district_name').contents[0]
					district_set.add(curr_district)

	district_set=sorted(district_set)
	j=1	
	for i in district_set:
		districts_dict[str(j)]=i 
		j=j+1

	
	##################################################

	return districts_dict


def fetchHospitalVaccineNames(web_page_data, district, state, age_group, dose):
	"""Fetch the Hospital and the Vaccine Names from the Web-page data available for a given District, State, Dose and Age Group
	and provide Options to select the respective Hospital and Vaccine Name.

	Parameters
	----------
	web_page_data : bs4.element.ResultSet
		All rows of Tabular data fetched from a website excluding the table headers
	district : str
		District where Vaccination is available for a given State, Dose and Age Group
	state : str
		State where Vaccination is available for a given Dose and Age Group
	age_group : str
		Age Group available for Vaccination and its availability in the States
	dose : str
		Dose available for Vaccination and its availability for the Age Groups

	Returns
	-------
	dict
		Dictionary with the Hosptial and Vaccine Names (where the Vaccination is available for a given District, State, Dose, Age Group)
		and Options to select, with Key as 'Option' and Value as another dictionary having Key as 'Hospital Name' and Value as 'Vaccine Name'
	
	Example
	-------
	>>> url_website = "https://www.mooc.e-yantra.org/task-spec/fetch-mock-covidpage"
	>>> web_page_data = fetchWebsiteData(url_website)
	>>> print(fetchHospitalVaccineNames(web_page_data, 'Kargil', 'Ladakh', '18+', '2'))
	{
		'1': {
				'MedStar Hospital Center': 'Covaxin'
			}
	}
	>>> print(fetchHospitalVaccineNames(web_page_data, 'South Goa', 'Goa', '45+', '2'))
	{
		'1': {
				'Eden Clinic': 'Covishield'
			}
	}
	"""
	
	hospital_vaccine_names_dict = {}

	##############	ADD YOUR CODE HERE	##############
	j=1
	for i in range(len(web_page_data)):
		
		dose_tag=web_page_data[i].find_all(class_='dose_num')[0]
		dose_content=dose_tag.contents[0]
		if dose_content==dose:
			parent_tag=dose_tag.parent
			curr_age_group=parent_tag.find(class_='age').contents[0]
			if curr_age_group==age_group:
				curr_state=parent_tag.find(class_='state_name').contents[0]
				if curr_state==state:
					curr_district=parent_tag.find(class_='district_name').contents[0]
					if curr_district==district:
						curr_hospital_name=parent_tag.find(class_='hospital_name').contents[0]
						vaccine=parent_tag.find(class_='vaccine_name').contents[0]
						hospital_vaccine_names_dict[str(j)]={curr_hospital_name:vaccine}
						j=j+1
	
	
	
	##################################################

	return hospital_vaccine_names_dict


def fetchVaccineSlots(web_page_data, hospital_name, district, state, age_group, dose):
	"""Fetch the Dates and Slots available on those dates from the Web-page data available for a given Hospital Name, District, State, Dose and Age Group
	and provide Options to select the respective Date and available Slots.

	Parameters
	----------
	web_page_data : bs4.element.ResultSet
		All rows of Tabular data fetched from a website excluding the table headers
	hospital_name : str
		Name of Hospital where Vaccination is available for given District, State, Dose and Age Group
	district : str
		District where Vaccination is available for a given State, Dose and Age Group
	state : str
		State where Vaccination is available for a given Dose and Age Group
	age_group : str
		Age Group available for Vaccination and its availability in the States
	dose : str
		Dose available for Vaccination and its availability for the Age Groups

	Returns
	-------
	dict
		Dictionary with the Dates and Slots available on those dates (where the Vaccination is available for a given Hospital Name,
		District, State, Dose, Age Group) and Options to select, with Key as 'Option' and Value as another dictionary having
		Key as 'Date' and Value as 'Available Slots'
	
	Example
	-------
	>>> url_website = "https://www.mooc.e-yantra.org/task-spec/fetch-mock-covidpage"
	>>> web_page_data = fetchWebsiteData(url_website)
	>>> print(fetchVaccineSlots(web_page_data, 'MedStar Hospital Center', 'Kargil', 'Ladakh', '18+', '2'))
	{
		'1': {'May 15': '0'}, '2': {'May 16': '81'}, '3': {'May 17': '109'}, '4': {'May 18': '78'},
		'5': {'May 19': '89'}, '6': {'May 20': '57'}, '7': {'May 21': '77'}
	}
	>>> print(fetchVaccineSlots(web_page_data, 'Eden Clinic', 'South Goa', 'Goa', '45+', '2'))
	{
		'1': {'May 15': '0'}, '2': {'May 16': '137'}, '3': {'May 17': '50'}, '4': {'May 18': '78'},
		'5': {'May 19': '145'}, '6': {'May 20': '64'}, '7': {'May 21': '57'}
	}
	"""

	vaccine_slots = {}

	##############	ADD YOUR CODE HERE	##############
	
	for i in range(len(web_page_data)):
		
		dose_tag=web_page_data[i].find_all(class_='dose_num')[0]
		dose_content=dose_tag.contents[0]
		if dose_content==dose:
			parent_tag=dose_tag.parent
			curr_age_group=parent_tag.find(class_='age').contents[0]
			if curr_age_group==age_group:
				curr_state=parent_tag.find(class_='state_name').contents[0]
				if curr_state==state:
					curr_district=parent_tag.find(class_='district_name').contents[0]
					if curr_district==district:
						curr_hospital_name=parent_tag.find(class_='hospital_name').contents[0]
						if curr_hospital_name==hospital_name:
							may_15_slots=parent_tag.find(class_='may_15').contents[0]
							may_16_slots=parent_tag.find(class_='may_16').contents[0]
							may_17_slots=parent_tag.find(class_='may_17').contents[0]
							may_18_slots=parent_tag.find(class_='may_18').contents[0]
							may_19_slots=parent_tag.find(class_='may_19').contents[0]
							may_20_slots=parent_tag.find(class_='may_20').contents[0]
							may_21_slots=parent_tag.find(class_='may_21').contents[0]
							
							vaccine_slots['1']={'May 15':may_15_slots}
							vaccine_slots['2']={'May 16':may_16_slots}
							vaccine_slots['3']={'May 17':may_17_slots}
							vaccine_slots['4']={'May 18':may_18_slots}
							vaccine_slots['5']={'May 19':may_19_slots}
							vaccine_slots['6']={'May 20':may_20_slots}
							vaccine_slots['7']={'May 21':may_21_slots}
						
	

	##################################################

	return vaccine_slots


def openConnection():
	"""Opens a socket connection on the HOST with the PORT address.

	Returns
	-------
	socket
		Object of socket class for the Client connected to Server and communicate further with it
	tuple
		IP and Port address of the Client connected to Server
	"""

	client_socket = None
	client_addr = None

	##############	ADD YOUR CODE HERE	##############
	
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind((HOST,PORT))
	server_socket.listen(1)

	client_socket, client_addr = server_socket.accept()
	
	##################################################
	
	return client_socket, client_addr


def startCommunication(client_conn, client_addr, web_page_data):
	"""Starts the communication channel with the connected Client for scheduling an Appointment for Vaccination.

	Parameters
	----------
	client_conn : socket
		Object of socket class for the Client connected to Server and communicate further with it
	client_addr : tuple
		IP and Port address of the Client connected to Server
	web_page_data : bs4.element.ResultSet
		All rows of Tabular data fetched from a website excluding the table headers
	"""

	##############	ADD YOUR CODE HERE	##############
	
	print('Client is connected at:',client_addr[1])
	
	client_conn.send(b"============================\n" +b"# Welcome to CoWIN ChatBot #\n"+b"============================\n\n")
	quitFlag=False
	count=0
	
	client_conn.send(b"Schedule an Appointment for Vaccination:\n\n")

	#################### DOSE SELECTION ####################
	quitFlag=doseSelection(web_page_data,count,quitFlag,client_conn)
		
	##################################################


def stopCommunication(client_conn):
	"""Stops or Closes the communication channel of the Client with a message.

	Parameters
	----------
	client_conn : socket
		Object of socket class for the Client connected to Server and communicate further with it
	"""

	##############	ADD YOUR CODE HERE	##############
	
	client_conn.send(b"<<< See ya! Visit again :)")
	client_conn.close()

	##################################################


################# ADD UTILITY FUNCTIONS HERE #################
## You can define any utility functions for your code.      ##
## Please add proper comments to ensure that your code is   ##
## readable and easy to understand.                         ##
##############################################################

#################### CHECK ELIGIBILITY FOR 2ND DOSE #############
def checkEligibility(client_conn,quitFlag,web_page_data,count):
	client_conn.send(b">>> Provide the date of First Vaccination Dose (DD/MM/YYYY), for e.g. 12/5/2021")
	input_date=client_conn.recv(1024).decode('utf-8')
	if input_date=='q' or input_date=='Q':
		stopCommunication(client_conn)
		quitFlag=True
	
	else:

		if input_date=='b' or input_date=='B':
			quitFlag=doseSelection(web_page_data,count,quitFlag,client_conn)

		if quitFlag:
			return quitFlag
		num_weeks,isInvalid=checkDate(input_date)

		while isInvalid:
			
			client_conn.send(b"<<< Invalid Date provided of First Vaccination Dose: "+input_date.encode('utf-8')+b'\n')
			client_conn.send(b">>> Provide the date of First Vaccination Dose (DD/MM/YYYY), for e.g. 12/5/2021")
			input_date=client_conn.recv(1024).decode('utf-8')
			if input_date=='q' or input_date=='Q':
				stopCommunication(client_conn)
				quitFlag=True
				
			if input_date=='b' or input_date=='B':
				quitFlag=doseSelection(web_page_data,count,quitFlag,client_conn)
				quitFlag=True
			if quitFlag:
				break
			num_weeks,isInvalid=checkDate(input_date)

		if quitFlag:
			return quitFlag

		client_conn.send(b"<<< Date of First Vaccination Dose provided: "+input_date.encode('utf-8')+b'\n')

		client_conn.send(b"<<< Number of weeks from today: "+str(num_weeks).encode('utf-8')+b'\n')

		if num_weeks<4:
			client_conn.send(b"<<< You are not eligible right now for 2nd Vaccination Dose! Try after "+str(4-num_weeks).encode('utf-8')+b" weeks\n")
			stopCommunication(client_conn)
			quitFlag=True
			
		elif num_weeks>8:
			client_conn.send(b"<<< You have been late in scheduling your 2nd Vaccination Dose by "+str(num_weeks-8).encode('utf-8')+b" weeks\n")
		elif num_weeks>=4 and num_weeks<=8:
			client_conn.send(b"<<< You are eligible for 2nd Vaccination Dose and are in the right time-frame to take it."+b"\n")
			
			

	return quitFlag

##################CHECK INVALID DATE FORMAT####################

def checkDate(input_date):
	isInvalid=False
	num_weeks=0
	input_date_list=input_date.split('/')
	today_date = datetime.date.today()
	today_date = today_date.strftime("%d/%m/%Y").split('/')

	if len(input_date_list)<3:
		isInvalid=True
	else:
		try:
			d0=datetime.date(int(input_date_list[2]),int(input_date_list[1]),int(input_date_list[0]))
		except ValueError:
			isInvalid=True
			return num_weeks,isInvalid
		d1=datetime.date(int(today_date[2]),int(today_date[1]),int(today_date[0]))
		num_weeks=(d1-d0).days//7

		
		format = "%d/%m/%Y"
		
		try:
			datetime.datetime.strptime(input_date, format)
			
		except ValueError:
			isInvalid=True
		
		if num_weeks<0:
			isInvalid=True

	return num_weeks,isInvalid

#############CHECK ANY INVALID INPUT#####################
def checkInvalidInput(input,curr_command, curr_dict,quitFlag,count,client_conn):
	count=0
	
	while input not in curr_dict:
		
		if input=='q' or input=='Q':
			quitFlag=True
			break
		if input!='b' and input!='B':
			count=count+1
			
			client_conn.send(b"<<< Invalid input provided "+str(count).encode('utf-8')+b" time(s)! Try again.\n")
			if count==3:
				quitFlag=True
				break
			client_conn.send(b"\n"+curr_command.encode('utf-8')+bytes(str(curr_dict)+'\n','utf-8'))
			input=client_conn.recv(1024).decode('utf-8')
		else:
			break
		
	return input,quitFlag,count


def doseSelection(web_page_data,count,quitFlag,client_conn):
	vaccine_doses_dict=fetchVaccineDoses(web_page_data)
	client_conn.send(b">>> Select the Dose of Vaccination: \n"+bytes(str(vaccine_doses_dict)+'\n','utf-8'))
	dose_option=client_conn.recv(1024).decode('utf-8')

	curr_command=">>> Select the Dose of Vaccination: \n"
	dose_option,quitFlag,count=checkInvalidInput(dose_option,curr_command,vaccine_doses_dict,quitFlag,count,client_conn)

	if dose_option=='q' or dose_option=='Q':
		stopCommunication(client_conn)
		quitFlag=True

	if not quitFlag:
		if dose_option=='b' or dose_option=='B':
			doseSelection(web_page_data,count,quitFlag,client_conn)
			return
	
		if quitFlag:
			return quitFlag

		
		client_conn.send(b"\n<<< Dose selected: "+dose_option.encode('utf-8')+b'\n\n')
		print("Dose selected:",dose_option)

		if dose_option=='2':
			quitFlag=checkEligibility(client_conn,quitFlag,web_page_data,count)
		
		if quitFlag:
			return quitFlag

		quitFlag=ageSelection(web_page_data,dose_option,count,quitFlag,client_conn)

	return quitFlag
	


###########################################################
def ageSelection(web_page_data,dose_option,count,quitFlag,client_conn):
	age_group_dict=fetchAgeGroup(web_page_data,dose_option)
	client_conn.send(b">>> Select the Age Group:\n"+bytes(str(age_group_dict)+'\n','utf-8'))
	
	age_group=client_conn.recv(1024).decode('utf-8')

	curr_command=">>> Select the Age Group:\n"
	age_group,quitFlag,count=checkInvalidInput(age_group,curr_command,age_group_dict,quitFlag,count,client_conn)

	if age_group=='q' or age_group=='Q':
		stopCommunication(client_conn)
		quitFlag=True

	if not quitFlag:

		if age_group=='b' or age_group=='B':
			return doseSelection(web_page_data,count,quitFlag,client_conn)
			
		

		if quitFlag:
			return quitFlag
		
		
		client_conn.send(b"\n<<< Selected Age Group: "+age_group_dict[age_group].encode('utf-8')+b"\n\n")
		print("Age Group selected:",age_group_dict[age_group])

		quitFlag=stateSelection(web_page_data,age_group_dict[age_group],dose_option,count,quitFlag,client_conn)
	
	return quitFlag

##############################################################
def stateSelection(web_page_data,age_group,dose_option,count,quitFlag,client_conn):
	states_dict=fetchStates(web_page_data,age_group, dose_option)
	client_conn.send(b">>> Select the State:\n"+bytes(str(states_dict)+'\n','utf-8'))
	
	state=client_conn.recv(1024).decode('utf-8')

	curr_command=">>> Select the State:\n"
	state,quitFlag,count=checkInvalidInput(state,curr_command,states_dict,quitFlag,count,client_conn)
	
	if state=='q' or state=='Q':
		stopCommunication(client_conn)
		quitFlag=True

	if not quitFlag:

		if state=='b' or state=='B':
			ageSelection(web_page_data,dose_option,count,quitFlag,client_conn)
			return quitFlag
		
		

		if quitFlag:
			return quitFlag
		
		
		client_conn.send(b"\n<<< Selected State: "+states_dict[state].encode('utf-8')+b"\n\n")
		print("State selected:",states_dict[state])

		quitFlag=districtSelection(web_page_data,states_dict[state],age_group,dose_option,count,quitFlag,client_conn)

	return quitFlag

##################################################################

def districtSelection(web_page_data,state,age_group,dose_option,count,quitFlag,client_conn):
	district_dict=fetchDistricts(web_page_data, state, age_group, dose_option)
	client_conn.send(b">>> Select the District:\n"+bytes(str(district_dict)+'\n','utf-8'))
	
	district=client_conn.recv(1024).decode('utf-8')

	curr_command=">>> Select the District:\n"
	district,quitFlag,count=checkInvalidInput(district,curr_command,district_dict,quitFlag,count,client_conn)

	if district=='q' or district=='Q':
		stopCommunication(client_conn)
		quitFlag=True

	if not quitFlag:

		if district=='b' or district=='B':
			stateSelection(web_page_data,age_group,dose_option,count,quitFlag,client_conn)
			return quitFlag
	
		if quitFlag:
			return quitFlag
		
		client_conn.send(b"\n<<< Selected District: "+district_dict[district].encode('utf-8')+b"\n\n")
		print("District selected:",district_dict[district])
		quitFlag=hospitalSelection(web_page_data, district_dict[district],state, age_group, dose_option,count,quitFlag,client_conn)

	return quitFlag
############################################################

def hospitalSelection(web_page_data, district,state, age_group, dose_option,count,quitFlag,client_conn):
	vaccine_center_dict=fetchHospitalVaccineNames(web_page_data,district,state, age_group, dose_option)
	client_conn.send(b">>> Select the Vaccination Center Name:\n"+bytes(str(vaccine_center_dict)+'\n','utf-8'))
	
	vaccine_center=client_conn.recv(1024).decode('utf-8')

	curr_command=">>> Select the Vaccination Center Name:\n"
	vaccine_center,quitFlag,count=checkInvalidInput(vaccine_center,curr_command,vaccine_center_dict,quitFlag,count,client_conn)

	if vaccine_center=='q' or vaccine_center=='Q':
		stopCommunication(client_conn)
		quitFlag=True

	if not quitFlag:
		if vaccine_center=='b' or vaccine_center=='B':
			districtSelection(web_page_data,state,age_group,dose_option,count,quitFlag,client_conn)
			return quitFlag
		
		if quitFlag:
			return quitFlag
		hospital_name=list(vaccine_center_dict[vaccine_center].keys())[0]
		client_conn.send(b"\n<<< Selected Vaccination Center: "+hospital_name.encode('utf-8')+b"\n\n")
		print("Hospital selected:",hospital_name)
		quitFlag=slotSelection(web_page_data, hospital_name, district,state, age_group, dose_option,count,quitFlag,client_conn)
	return quitFlag
	###########################################################

def slotSelection(web_page_data, hospital_name, district,state, age_group, dose_option,count,quitFlag,client_conn):
	slots_dict=fetchVaccineSlots(web_page_data, hospital_name, district,state, age_group, dose_option)
	client_conn.send(b">>> Select one of the available slots to schedule the Appointment:\n"+bytes(str(slots_dict)+'\n','utf-8'))
	
	slot=client_conn.recv(1024).decode('utf-8')

	curr_command=">>> Select one of the available slots to schedule the Appointment:\n"
	slot,quitFlag,count=checkInvalidInput(slot,curr_command,slots_dict,quitFlag,count,client_conn)

	if slot=='q' or slot=='Q':
		stopCommunication(client_conn)
		quitFlag=True

	if not quitFlag:
		if slot=='b' or slot=='B':
			hospitalSelection(web_page_data, district,state, age_group, dose_option,count,quitFlag,client_conn)
			return quitFlag
		
		if quitFlag:
			return quitFlag
		selected_date=list(slots_dict[slot].keys())[0]
		client_conn.send(b"\n<<< Selected Vaccination Appointment Date: "+selected_date.encode('utf-8')+b"\n")
		print("Vaccination Date selected:",selected_date)
		client_conn.send(b"<<< Available Slots on the selected Date: "+slots_dict[slot][selected_date].encode('utf-8')+b"\n")
		print("Available Slots on that date:",slots_dict[slot][selected_date])
		if int(slots_dict[slot][selected_date])==0:
			client_conn.send(b"<<< Selected Appointment Date has no available slots, select another date!\n")
		else:
			client_conn.send(b"<<< Your appointment is scheduled. Make sure to carry ID Proof while you visit Vaccination Center!\n")
		
		stopCommunication(client_conn)
	return quitFlag

	
##############################################################

if __name__ == '__main__':
	"""Main function, code begins here
	"""
	url_website = "https://www.mooc.e-yantra.org/task-spec/fetch-mock-covidpage"
	web_page_data = fetchWebsiteData(url_website)
	client_conn, client_addr = openConnection()
	startCommunication(client_conn, client_addr, web_page_data)
