Problem Statement:

Write a Program, to do House Keeping activity of your Machine, generate the alert by sending the mail.
Task:
1. CPU utilization
2. Memory Usage
3. Disk Space Utilization
4. Disk File Utilization

Steps:

1. We have to take email address from the user for sending the mail alerts using ArgParse Module
2. Create Logging Configuration object for saving the Events.
3. Parse the Configuration file for fetching the cpu_threshold, ram_threshold, diskusage_threshold, diskfile_threshold, gmail_user and gmail_password
4. Use psutil Module for CPU Utilization using psutil.cpu_percent()
5. For RAM utilization using psutil.virtual_memory().percent
6. For Disk File Utilization, psutil.disk_usage('/').percent
7. For Disk Usage, created a Function to fetch the list of all files having size greater than 1 GB
8. Created a Function for sending the mail using SMTPLIB Module


Help File:


(base) C:\Users\admin\PycharmProjects\HealthCheck>python health_checker.py -h
usage: health_checker.py [-h] -e EMAIL_ID [EMAIL_ID ...]

optional arguments:
  -h, --help            show this help message and exit

Required Named arguments:
  -e EMAIL_ID [EMAIL_ID ...], --email EMAIL_ID [EMAIL_ID ...]


Execution:

(base) C:\Users\admin\PycharmProjects\HealthCheck>python health_checker.py -e <email address>
25-Dec-19 08:01:43 - configuration Options {'cpu_threshold': '10', 'ram_threshold': '30', 'diskusage_threshold': '40', 'diskfile_thr
eshold': '1000000000', 'gmail_user': 'email address', 'gmail_password': '**********'}
25-Dec-19 08:01:43 - CPU value 19.0 is more than Threshold Value 10
25-Dec-19 08:01:43 - Consumed RAM 83.8 is more than Threshold Value 30
25-Dec-19 08:01:43 - Disk File consumed space 50.5 is more than Threshold value 40
25-Dec-19 08:01:50 - Files ['C:\\hiberfil.sys', 'C:\\pagefile.sys', 'C:\\Users\\admin\\Downloads\\v2-plant-seedlings-dataset.zip'] c
onsuming space more than 1 GB
25-Dec-19 08:01:50 - Message Body     <html>
        <head></head>
        <body>
            <p>Hey miteshmakhija@gmail.com,<br>
            <br>
            Following alerts generated:<br>            <br><b>CPU value 19.0 is more than Threshold Value 10 </b><br><br><b>Consumed
 RAM 83.8 is more than Threshold Value 30 </b><br><br><b>Disk File consumed space 50.5 is more than Thresold Value 40 </b><br><br><b
>Files ['C:\\hiberfil.sys', 'C:\\pagefile.sys', 'C:\\Users\\admin\\Downloads\\v2-plant-seedlings-dataset.zip'] consuming space more
than 1GB </b><br>        </p>
        </body>
        </html>
25-Dec-19 08:01:57 - Email Sent!!
