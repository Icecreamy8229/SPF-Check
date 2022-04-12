import os
import mysql.connector
from datetime import datetime
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date
from datetime import timedelta
count_threshhold = 20
smtp_port = 25
smtp_server = ""
sender_email = ""
smtp_password = ''
smtp_context = ssl.create_default_context()


database = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
  
)
mycursor = database.cursor()
def get_time():
  date = datetime.now()
  time = date.strftime("%Y/%m/%d %H:%M:%S")
  return(time)


def database_domain_lookup():
    domains_registered = []
    mycursor.execute('SELECT domain FROM normbot.spfcheck')
    for x in mycursor:
        remove_characters = "(',)"
        for character in remove_characters:
            x = str(x).replace(character,"")
        domains_registered.append(x)
    return(domains_registered)    
def less_than_10_lookup():
    domains_registered = []
    mycursor.execute('SELECT domain FROM normbot.lessthan10')
    for x in mycursor:
        remove_characters = "(',)"
        for character in remove_characters:
            x = str(x).replace(character,"")
        domains_registered.append(x)
    return(domains_registered)        


def logfile_date():
    current_date = date.today()
    
    yesterday = str(current_date - timedelta(days = 1))
    yesterday = yesterday.replace("/","-")
    return(yesterday)

current_log_file = "/Python-Programs/Syno-Link/xchange3-sendfile/hmailserver_{}.log".format(logfile_date())

print(current_log_file)
List = open(current_log_file, encoding='latin-1').read().splitlines()


Organized_List = []
counting_list = []
cleanup_mail_addresses = '"<>'
for item in List:
    for character in cleanup_mail_addresses:
        item = item.replace(character, "")
        
    if "MAIL FROM:" in item:
        
        
        
        
        item = item.split('MAIL FROM:')[1]
        print('MAIL FROM FOUND' + item)
        item = item.split('@')[-1]
        if "SIZE=" in item:
            item = item.split('SIZE=')[0]
        item = item.lower()
        item = item.replace(' ',"")
        print(item)
        
        
        if item != "" and 'latitudecg.com' not in item and 'latitudelearning.com' not in item:
            
            
            counting_list.append(item)
            
            if item not in Organized_List:
                Organized_List.append(item)
       
for item in Organized_List:
    
    item_count = counting_list.count(item)
    count = int(counting_list.count(item))
    
    if item not in database_domain_lookup() and item_count >= count_threshhold:
        print("{} was FOUND MORE THAN {} TIMES and will be added to the database".format(item, str(count)))
        
                
        mycursor.execute('INSERT INTO normbot.spfcheck (domain, last_time_checked, emails_sent) VALUES (%s,%s,%s)',(item.lower(), get_time(),count))
        database.commit()
    if item not in less_than_10_lookup() and item_count < count_threshhold:
        count = int(counting_list.count(item))
        print("{} was found LESS THAN {} times and will NOT added to the database".format(item, str(count)))
        mycursor.execute('INSERT INTO normbot.lessthan10 (domain, last_time_checked, emails_sent) VALUES (%s,%s,%s)',(item.lower(), get_time(), count))
        database.commit()
for item in Organized_List:
    item_count = int(counting_list.count(item))
    if item_count >= count_threshhold:
        mycursor.execute("UPDATE `normbot`.`spfcheck` SET `emails_sent` = '{}' WHERE (`domain` = '{}');".format(item_count, item))
        database.commit()
    if item_count < count_threshhold:
        mycursor.execute("UPDATE `normbot`.`lessthan10` SET `emails_sent` = '{}' WHERE (`domain` = '{}');".format(item_count, item))
        database.commit()    
    
 
for x in database_domain_lookup():
    
    check_record = os.popen('dig @8.8.8.8 txt {}'.format(x)).read()
    mycursor.execute('UPDATE normbot.spfcheck SET last_time_checked = "{}" WHERE domain ="{}"'.format(get_time(), x))
    database.commit()
    def check_189():
        if "64.9.204.189" in check_record:
            mycursor.execute('UPDATE normbot.spfcheck SET IP189 = "True" WHERE domain = "{}";'.format(x))
            database.commit()
            
        else:
            mycursor.execute('UPDATE normbot.spfcheck SET IP189 = "False" WHERE domain = "{}";'.format(x))
            database.commit() 
        

    def check_252():
        
        if "64.9.204.252" in check_record:
            mycursor.execute('UPDATE normbot.spfcheck SET IP252 = "True" WHERE domain = "{}";'.format(x))
            database.commit()
            
        else:
            mycursor.execute('UPDATE normbot.spfcheck SET IP252 = "False" WHERE domain = "{}";'.format(x))
            database.commit()   
            
    def check_latitudecg():
        if "latitudecg.com" in check_record:
            mycursor.execute('UPDATE normbot.spfcheck SET latitudecgcom = "True" WHERE domain = "{}";'.format(x))
            database.commit()
        else:
            mycursor.execute('UPDATE normbot.spfcheck SET latitudecgcom = "False" WHERE domain = "{}";'.format(x))
            database.commit()     
    check_189()
    check_252()
    check_latitudecg()

def norm_list_domains():
    domain_space = 40
    id_space = 5
    compliance_space = 12
    
    
    send_message = ""
    mycursor.execute('SELECT * FROM normbot.spfcheck;')
    results = mycursor.fetchall()
    #print('ID:' + '    ' + 'DOMAIN:'+ '    ' + 'COMPLIANCE' + '    ' + 'LAST CHECK')
    row0 = ""
    row1 = ""
    row2 = ""
    row3 = ""
    row4 = ""
    row5 = ""
    
    for row in results:
        row0 = str(row[0])
        row1 = str(row[1])
        row2 = str(row[2])
        row3 = str(row[3])
        row4 = str(row[4])
        row5 = str(row[5])
        x = 0

        
        
        for i in row0:
            
            x += 1
        gap0 = id_space - x    
        while gap0 > 0:
            gap0 -= 1
            row0 += " "   
        x = 0    
        for i in row1:
            x += 1
            
        gap1 = domain_space - x    
        while gap1 > 0:
            gap1 -= 1
            row1 += " "
        x = 0    
        for i in row2:
            x += 1
        gap2 = compliance_space - x   
        while gap2 > 0:
            gap2 -= 1
            row2 += " "
        x = 0     
        for i in row3:
            
            x += 1
        gap3 = compliance_space - x    
        while gap3 > 0:
            gap3 -= 1
            row3 += " "
        x = 0     
        for i in row4:
            
            x += 1
        gap4 = compliance_space - x    
        while gap4 > 0:
            gap4 -= 1
            row4 += " "    
        
        send_message += '\n' + row0 + row1 + row2 + row3 + row4 + row5
        
        
    
    return(send_message)
        
   

def mail_results():
    mail_to = 'networkteam@latitudecg.com'
    try:
        legend = 'ID:   DOMAIN:                                IP252       IP189    LATITUDECG.COM   TIMECHECKED'
        cleanup = "]['"
        message = MIMEMultipart("alternative")
        message["Subject"] = "Daily SPF Check"
        message["From"] = sender_email
        message["To"] = mail_to 
        
        #context = ssl.create_default_context()
        server = smtplib.SMTP(smtp_server,smtp_port)
        server.ehlo() # Can be omitted
        #server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        
        #server.login(sender_email, smtp_password)
        text = "Below list only shows domains with a send count higher than 20 emails.  All others are logged to a seperate database and can be viewed in SQL" + '\n' + legend + norm_list_domains() + "\n" + "\n" + 'Sent at: {}'.format(get_time()) 
        part1 = MIMEText(text, "plain")
        message.attach(part1)
        for x in cleanup:
            text = text.replace(cleanup,"")
        server.sendmail(sender_email, mail_to, message.as_string())
        
        
    except Exception as e:
        # Print any error messages to stdout
        print('something went wrong') 
        print(e)
    finally:
        server = smtplib.SMTP(smtp_server,smtp_port)
        print('SPF-Check Email has been sent')
        server.quit()
    
    print(mail_to)
mail_results()    
        
  
     

        
          
    
   
   
    
    
    
