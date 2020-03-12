Run this script to add frame routes to RADDB2 MYSQL Database.

---Files---

- framed_routes_10.csv - This file contains the routes that are
  configured in the ERX310. 
  EX. Format- 196.12.185.211,196.12.177.184,255.255.255.248
  
- routes - This file contain the same subnets that needs to be
    configured in the database.
    EX. Format 196.12.177.184/29
    
- route.py - This is the main script, it will open the file 
     files/framed_routes_10.csv then it uses the library ipaddress
     to format the subnet mask to CIDR format(/30)
   - The next step is to create a query that will search for
     the ip address and extract the PPPoE username.
   - With the username extracted, we formulate the INSERT Query.
   
   
Usage - python route.py with no arguments.
*REMEMBER TO CHANGE USERNAME AND PASSWORD.


- tools/converter.py
    This tool is used to create a file with the new ip address in CIDR
    Format.
    
-requirements.txt - This file contains the libraries to be installed
to use this script.
    usage:  pip install -r requirements.txt 
     