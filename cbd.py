import os
import json
import keystoneclient.v2_0.client as ksclient
import MySQLdb
#The following get_id function is used for authenticating and retreiving tokens, the remaining code will work only after retreiving token
def get_id(url, tenant_name, username, password):
	syscall = "curl  'http://" + url + ":5000/v2.0/tokens' -X POST #-H \"Content-Type: application/json\" -H \"Accept: application/json\" -H \"User-Agent: python-keystoneclient\" -d '{\"auth\": {\"tenantName\": ##\"" + tenant_name + "\", \"passwordCredentials\": {\"username\": \"" + username + "\", \"password\": \"" + password + "\"}}}' > response.txt"
	print syscall
	os.system(syscall)

	json_data = open("response.txt")

	data = json.load(json_data)

	json_data.close()
	return data['access']['token']['id']
def get_keystone_creds():
    d = {}
    d['username'] = os.environ['OS_USERNAME']
    d['password'] = os.environ['OS_PASSWORD']
    d['auth_url'] = os.environ['OS_AUTH_URL']
    d['tenant_name'] = os.environ['OS_TENANT_NAME']
    return d
option = 0

#token_id = ""
#image_name=""


#CONNECT TO MYSQL CODE
db = MySQLdb.connect(host = "localhost", user = "root", passwd = "lubna", db = "keystone")
cur = db.cursor()
creds = get_keystone_creds()
keystone = ksclient.Client(**creds)
service = keystone.services.create(name="keystone",
			                   service_type="identity",
				                   description="OpenStack Identity Service")

while option != 5:
	print "1. Create ENDPOINT\n 2. Update endpoint\n 3. Display list\n 4. Delete Endpoint\n 5. Exit\n Enter choice:\n "
	option = int(raw_input()) 
	if option == 1:
		keystone_publicurl = "http://10.1.120.105:5000/v2.0"
		keystone_adminurl = "http://10.1.120.105:35357/v2.0"
		region_name = "RegionOne"
		print "Enter service_id"
		service.id= raw_input()
		

		keystone.endpoints.create(service_id=service.id, region = region_name,
				          publicurl=keystone_publicurl,
				          adminurl=keystone_adminurl)
		
	elif option == 2:#update
			cur.execute("select * from endpoint");
			#print
			rows = cur.fetchall()
			for row in rows:
				for col in row:
					print "%s, " % col
				print "\n"
			#done
			print "Enter the id of the endpoint you want to update "
			legacy_endpoint_id_new = raw_input()
			print "Enter id, interface, region, service_id, url; Enter u in unchanged field"
			id_new = raw_input()
			if id_new != "u" :
				#execute update-set
				cur.execute("update endpoint set id = id_new where legacy_endpoint_id = legacy_endpoint_id_new");
			
			interface_new = raw_input()
			if interface_new != "u" :
				#execute update-set
				cur.execute("update endpoint set interface = interface_new where legacy_endpoint_id = legacy_endpoint_id_new");
			region_new = raw_input()
			if region_new != "u" :
				#execute update-set
				cur.execute("update endpoint set region = region_new where legacy_endpoint_id = legacy_endpoint_id_new");
				
			service_id_new = raw_input()
			if service_id_new != "u" :
				#execute update-set
				cur.execute("update endpoint set service_id = service_id_new where legacy_endpoint_id = legacy_endpoint_id_new");
			url_new = raw_input()
			if url_new != "u" :
				#execute update-set
				cur.execute("update endpoint set url = url_new where legacy_endpoint_id = legacy_endpoint_id_new");
	elif option == 3:#display
			cur.execute("select * from endpoint");
			#print
			#print
			rows = cur.fetchall()
			for row in rows:
				for col in row:
					print "%s, " % col
				print "\n"
			#done
	elif option == 4:#delete
			print "Enter service_id"
			service.id= raw_input()
			cur.execute("delete from endpoint where service_id = service.id");
			cur.execute("select * from endpoint");
			#print
			#print
			rows = cur.fetchall()
			for row in rows:
				for col in row:
					print "%s, " % col
				print "\n"
			#done
	elif option == 5:
			break
