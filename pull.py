import xmlrpclib

remoteHost = "0.0.0.0"
remoteUser = "username"

remoteDbName = "wordpress_dbname"
remoteDbPass = "pass"
remoteDbUser = "wordpress_dbuser'"

wfDbName = remoteDbName
wfDbPass = remoteDbPass
wfDbUser = remoteDbUser
wfDbType = "mysql"

domainName = "domain.com"
domainNameNoDot = "domain"
domainNameWWW = "www.domain.com"

server = xmlrpclib.ServerProxy("https://api.webfaction.com/")
session_id, account= server.login("wfusername", "wfpassword")
server.create_app(session_id, domainNameNoDot, "static", False, "", False)
server.create_domain(session_id, domainName, "www")
server.create_website(session_id,domainNameNoDot,"wfipaddresshere",False,[domainName, domainNameWWW])

#create the wf db, with a dummy password for the default user that will get created automatically
server.create_db(session_id, wfDbName, wfDbType, 'dontusepassword')
#then, delete that user created automatically with the same name as the db
server.delete_db_user(session_id, wfDbName, wfDbType)
#then create the user we really want
server.create_db_user(session_id, wfDbUser, wfDbPass, wfDbType)
#and give that user perms to the database
server.grant_db_permissions(session_id, wfDbUser, wfDbName, wfDbType)

cmd = "ssh " + remoteUser + "@" + remoteHost +  " 'mysqldump --user=" + remoteDbUser + " -p\"" + remoteDbPass + "\""  + " --add-drop-table --no-create-db --skip-lock-tables " + remoteDbName + "'" + " | mysql --user=" + wfDbUser + " -p\"" + wfDbPass + "\" " + wfDbName

print cmd

# eventually, when this works properly, we will execute the above command.
#todo:
#next we need to perform an rsync to copy the code from the remote over here to WF

