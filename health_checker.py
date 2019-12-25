import psutil, logging, smtplib, os
import configparser, argparse, textwrap
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def get_size(start_path = '.', disk_usage_threshold = 0):
    '''
    Method finds list of files consuming space more than 1GB
    return: list
    '''
    file_names = []
    for dirpath, dirnames, filenames in os.walk(start_path, topdown = True):
        dirnames[:] = [d for d in dirnames if d not in ['Temp','AppData','Windows']] #Excluding following directory
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.getsize(fp) > disk_usage_threshold:
                file_names.append(fp)
    return file_names

def config_reader(filepath = None):
    '''
    Method parses config file, return dictionary of all the sections
    return: dictionary and section
    '''
    dict_option = {}
    config = configparser.ConfigParser()
    config.read(filepath)
    sections = config.sections()
    options = config.options(sections[0])
    for option in options:
        try:
            dict_option[option] = config.get(sections[0], option)
            if dict_option[option] == -1:
                logger.error("Please check Threshold Configuration File")
        except:
            dict_option[option] = None
    return sections[0] , dict_option

def send_mail(user, password, to_list, subject, body):
    '''
    Method sends mail to List of users using GMAIL credentials
    '''
    msg = MIMEMultipart()
    msg['From'] = user
    msg['To'] = ",".join(to_list)
    msg['Subject'] = subject

    msg_body = MIMEText(body, 'html')
    msg.attach(msg_body)
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(user, password)
        server.sendmail(user, ",".join(to_list), msg.as_string())
        server.quit()
        logger.info("Email Sent!!")
    except Exception as e:
        logger.error("Error: {}".format(e))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('Required Named arguments')
    requiredNamed.add_argument('-e', '--email', dest='email_id', required=True,
                               type=str, nargs='+')
    args = parser.parse_args()
    
    #Logger Configuration
    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    fileHandler = logging.FileHandler(filename = 'app.log') #Relative Path
    fileHandler.setFormatter(formatter)
    logger.setLevel(level = logging.DEBUG) #Logging Level
    
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    
    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)
    
    #Threshold Configuration Parser
    machine_name, dict_config = config_reader('threshold.ini') #Relative Path
    logging.debug("configuration Options {}".format(dict_config))
    
    mail_flag = False
    file_names = ''
    
    msg_body = '''\
    <html>
        <head></head>
        <body>
            <p>Hey {},<br>
            <br>
            Following alerts generated:<br>\
            '''.format(",".join(args.email_id))
    
    #CPU Utilization
    cpu_utilization = psutil.cpu_percent()
    if cpu_utilization > float(dict_config['cpu_threshold']):
        logging.warning("CPU value {} is more than Threshold Value {}"
                        .format(cpu_utilization, dict_config['cpu_threshold']))
        mail_flag = mail_flag or True
        msg_body += "<br><b>CPU value {} is more than Threshold Value {} </b><br>"\
            .format(cpu_utilization, dict_config['cpu_threshold'])

    #RAM Utilization
    ram_utilization = psutil.virtual_memory().percent
    if ram_utilization > float(dict_config['ram_threshold']):
        logging.warning("Consumed RAM {} is more than Threshold Value {}"
                        .format(ram_utilization, dict_config['ram_threshold']))
        mail_flag = mail_flag or True
        msg_body += "<br><b>Consumed RAM {} is more than Threshold Value {} </b><br>"\
            .format(ram_utilization, dict_config['ram_threshold'])
        
    #DISK File Utilization
    disk_utilization = psutil.disk_usage('/').percent
    if disk_utilization > float(dict_config['diskusage_threshold']):
        logging.warning("Disk File consumed space {} is more than Threshold value {}"
                        .format(disk_utilization, dict_config['diskusage_threshold']))
        mail_flag = mail_flag or True
        msg_body += "<br><b>Disk File consumed space {} is more than Thresold Value {} </b><br>".\
            format(disk_utilization, dict_config['diskusage_threshold'])
        
    #DISK Usage
    #Looking for files consuming space more than 1 GB under c:\
    file_names = get_size('C:\\', int(dict_config['diskfile_threshold']))
    if file_names:
        logging.warning("Files {} consuming space more than 1 GB".format(file_names))
        mail_flag = mail_flag or True
        msg_body += "<br><b>Files {} consuming space more than 1GB </b><br>".format(file_names)

    #Send Mail
    if mail_flag:
        msg_body += '''\
        </p>
        </body>
        </html>
        '''
        logging.debug("Message Body {}".format(msg_body))
        send_mail(dict_config['gmail_user'], dict_config['gmail_password'], args.email_id,
                  'Health Checkup Report of Machine {}'.format(machine_name), msg_body)