#! /usr/bin/python
import threading
import argparse
import signal
import re
import sys
import hashlib
import os
import time
import json
import shutil
import subprocess
from configparser import ConfigParser
from pymemcache.client.base import Client

# encoding=utf8
reload(sys)
sys.setdefaultencoding('utf8')
def main_hud():
 


    # functions
    def handler(signum, frame):
        print ("")
        print ("[] Since you pressed CTRL+C ")
        print ("[] This program will terminate gracefully ...")
        print """


        The more knowledge you acquire,
    you realize you dont have knowledge,
    hence, the more knowledge you crave
    for.
    Hud Seidu Daannaa
    -----------------
    ---------


    """
        sys.exit()
    def touch(fname, times=None):
        with open(fname, 'a'):
            os.utime(fname, times)
    def install(package):subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    def writer(data, file_):f = open('{0}'.format(file_), "a+");f.write('{}\n'.format(data));f.close()
    def reader(file_): f=open(file_, 'rt'); return [n.strip('\n') for n in f.readlines()];f.close()
    def log(datax, log_path='application.log'):
        timer=str(time.asctime(time.localtime(time.time())))
        data = "{0} {1}".format(timer, datax)
        f = open('{0}'.format(log_path), "a+")
        f.write('{}\n'.format(data))
        f.close()
    def make_key(keyd, data):
        #where data is event
        key_=""
        ev_json= json.loads(data)
        for n in keyd:
            k=str(ev_json[n])+"__"
            key_=key_+k
        return key_
    def hashfile(file_):
        BLOCK_SIZE = 65536              # The size of each read from the file
        file_hash = hashlib.sha256()    # Create the hash object, can use something other than `.sha256()` if you wish
        with open(file_, 'rb') as f:     # Open the file to read it's bytes
            fb = f.read(BLOCK_SIZE)     # Read from the file. Take in the amount declared above
            while len(fb) > 0:          # While there is still data being read from the file
                file_hash.update(fb)    # Update the hash
                fb = f.read(BLOCK_SIZE) # Read the next block from the file
        return (file_hash.hexdigest())  # Get the hexadecimal digest of the hash
    def fcn_v1(address, memory_dir_name, file__):
    
        #memcache params
        host = address.split(':')[0]
        port = address.split(':')[1]
        
        #server log file
        logfilename=os.path.join(memory_dir_name, "{2}_{0}_{1}_log.logger".format(host, port, memory_dir_name))
        #server memmory file
        memfile_add=os.path.join(memory_dir_name, ".{0}_{1}_{2}.tracker".format(memory_dir_name, host, port))
        
        #create reg/memmory files that will be read from at first, we dont create logfilename bcos
        # at its first instance, is a write, so the file is created automaticaly
        touch(memfile_add)
        
        #logs
        log("", logfilename)
        log("[+] Server: {}".format(address), logfilename)
        log("[+] =====================", logfilename)
        log("", logfilename)

        #connect to mb
        try:
            client = Client((str(host), int(port)))
            log ("[+] Connection established to Memcache DB", logfilename)
        except Exception as err:
            log ("[+] Whilst using: SET | Could not connect to server, due to ..", logfilename)
            log (err, logfilename)                           

        hashed_intel_file = hashfile(file__)
        log("[+] {0} with hash value:{1} is been loaded".format(file__, hashed_intel_file), logfilename)
        log ("[+] _______________________________", logfilename)

        #for reading mem file
        logxxx=""
        try:
            log ("[+] Using MEMCACHED: SET cmd", logfilename)
            logxxx=reader(file__)
        except:print ("[+] The input file cannot be read !!!", logfilename)
        for events in logxxx:
            ev_str = events.replace("u'",'"').replace("'",'"')

            #file validation
            try:ev_json= json.loads(ev_str)
            except:
                print ("")
                print ("[+] File not VALID !!!/!")
                print ("[+] Hence, File must contain json")
                print ("")
            keyx = make_key(key, ev_str)
            dubs = reader(memfile_add)

            output='False'
            #dubs stands for duplicates file, which is the memmory file of already sent events to memdb,
            #hence below is saying is it is 0 meanin, nothing has been sent to it yet and that it is a new
            #file
            if len(dubs) == 0:
                try:
                    output = client.set(str(ev_json[document_key_field]), ev_str)
                    log ("[+] {0} pushed to {2} | success: {1}".format(ev_json[document_key_field], output, address), logfilename)
                    writer(keyx, memfile_add)
                except Exception as err:
                    log ("[+] {0} NOT pushed to {2} | success: {1}".format(ev_json[document_key_field], output, address), logfilename)
                    log (err, logfilename)

            else:
                if keyx in dubs: log ("[+] {0} Already pushed to {2} | success: {1}".format(ev_json[document_key_field], output, address), logfilename)
                else:
                    try:
                        output = client.set(str(ev_json[document_key_field]), ev_str)
                        log ("[+] {0} pushed to {2} | success: {1}".format(ev_json[document_key_field], output, address), logfilename)
                        writer(keyx, memfile_add)
                    except Exception as err:
                        log ("[+] {0} NOT pushed to {2} | success: {1}".format(ev_json[document_key_field], output, address), logfilename)
                        log (err, logfilename)
                
    def fcn_v2(address, memory_dir_name, intel_dir):
    
        #memcache params
        host = address.split(':')[0]
        port = address.split(':')[1]
        
        #server log file
        logfilename=os.path.join(memory_dir_name, "{2}_{0}_{1}_log.logger".format(host, port, memory_dir_name))
        #server memmory file
        memfile_add=os.path.join(memory_dir_name, ".{0}_{1}_{2}.tracker".format(memory_dir_name, host, port))
        #intel.intel, file hash repo
        filehashfile_=os.path.join(memory_dir_name, ".{0}_{1}_{2}.hasher".format(memory_dir_name, host, port))
        
        #create reg/memmory files that will be read from at first, we dont create logfilename bcos
        # at its first instance, is a write, so the file is created automaticaly
        touch(memfile_add)
        touch(filehashfile_)

        #logs
        log("", logfilename)
        log("[+] Server: {}".format(address), logfilename)
        log("[+] =====================", logfilename)
        log("", logfilename)

        #connect to mb
        try:
            client = Client((str(host), int(port)))
            log ("[+] Connection established to Memcache DB", logfilename)
        except Exception as err:
            log ("[+] Whilst using: SET | Could not connect to server, due to ..", logfilename)
            log (err, logfilename)                           
        
        # for reading file hash
        filehashes_reader=""
        try:
            filehashes_reader=reader(filehashfile_)
            log ("[+] Accessing intel hash registry", logfilename)
        except Exception as err:
            print ("[+] The input hash file cannot be read !!!", logfilename)
            log (err, logfilename) 
        
        #check for files in dir
        dirs=os.listdir(intel_dir)
        #print intel_dir
        if len(dirs) == 0:
            log ("[+] Intel directory is empty", logfilename)
            pass
        else:
            log ("[+] Intel directory is not empty", logfilename)
            log ("[+] Application will proceed ...", logfilename)
            for intel_file in dirs:
                log ("[+] _______________________________", logfilename)
                log ("[+] ", logfilename)
                log ("[+] Operating on intel file: {} ...".format(intel_file), logfilename)
                log ("[+] _______________________________", logfilename)
                log ("[+]", logfilename)
                #check for intel files
                #for intel_file in re.findall(r'\d+_\w+', filehsh)
                # hashr is the result of the hash file listed from dirs
                #get hash of files and compare
                intel_file_path=os.path.join(intel_dir, intel_file)                
                hashed_intel_file = hashfile(intel_file_path)
                #filehashes_reader is the file hash repo, of stored hashes of already processed intel files to memdb
                if hashed_intel_file in filehashes_reader:
                    log("[+] {0} with hash value:{1} has already been loaded".format(intel_file, hashed_intel_file), logfilename)
                    log ("[+] _______________________________", logfilename)
                else:
                    log("[+] {0} with hash value:{1} is been loaded".format(intel_file, hashed_intel_file), logfilename)
                    log ("[+] _______________________________", logfilename)

                    #for reading mem file
                    logxxx=""
                    try:
                        log ("[+] Using MEMCACHED: SET cmd", logfilename)
                        logxxx=reader(intel_file_path)
                    except:print ("[+] The input file cannot be read !!!", logfilename)
                    for events in logxxx:
                        ev_str = events.replace("u'",'"').replace("'",'"')

                        #file validation
                        try:ev_json= json.loads(ev_str)
                        except:
                            print ("")
                            print ("[+] File not VALID !!!/!")
                            print ("[+] Hence, File must contain json")
                            print ("")
                        keyx = make_key(key, ev_str)
                        dubs = reader(memfile_add)

                        output='False'
                        #dubs stands for duplicates file, which is the memmory file of already sent events to memdb,
                        #hence below is saying is it is 0 meanin, nothing has been sent to it yet and that it is a new
                        #file
                        if len(dubs) == 0:
                            try:
                                output = client.set(str(ev_json[document_key_field]), ev_str)
                                log ("[+] {0} pushed to {2} | success: {1}".format(ev_json[document_key_field], output, address), logfilename)
                                writer(keyx, memfile_add)
                            except Exception as err:
                                log ("[+] {0} NOT pushed to {2} | success: {1}".format(ev_json[document_key_field], output, address), logfilename)
                                log (err, logfilename)

                        else:
                            if keyx in dubs: log ("[+] {0} Already pushed to {2} | success: {1}".format(ev_json[document_key_field], output, address), logfilename)
                            else:
                                try:
                                    output = client.set(str(ev_json[document_key_field]), ev_str)
                                    log ("[+] {0} pushed to {2} | success: {1}".format(ev_json[document_key_field], output, address), logfilename)
                                    writer(keyx, memfile_add)
                                except Exception as err:
                                    log ("[+] {0} NOT pushed to {2} | success: {1}".format(ev_json[document_key_field], output, address), logfilename)
                                    log (err, logfilename)
                    #after intel file is loaded, register its file hash
                    writer(hashed_intel_file, filehashfile_)
           
            log("", logfilename)
            log("[+] Done ...", logfilename)



    ##############################################33

    #log ("[+] ")
    #params
    sparser = ConfigParser()
    sparser.read('settings.ini')

    addresses = [t.strip() for t in sparser.get('Memcache_config', 'address').split(',')]
    key  = [e.strip() for e in sparser.get('Application', 'primary_key').split(',')]
    memory_dir_name = sparser.get('Application', 'memdir',fallback='.register')
    document_key_field = sparser.get('Application','document_key_field')

    pce    = argparse.ArgumentParser(description=""" Events in text to Memcache  |By Hud Seidu Daannaa """)
    pce.add_argument('-f', '--file', type=str, metavar='',  help='Specify a file')
    pce.add_argument('-d', '--dir', type=str, metavar='',  help='Specify a intel dir')
    pce.add_argument('-X', '--flush', action='store_true',  help="Flush will reset the application logs and registry/memfile")
    pce.add_argument('-R', '--readme', action='store_true',  help="README")
    pce.add_argument('-g', '--get', type=str, metavar='',  help='Specify a key get a value stored in memcache')
    args   = pce.parse_args()

    file__ = args.file
    readme = args.readme
    flush  = args.flush
    get    = args.get
    intel_dir = args.dir

    signal.signal(signal.SIGINT, handler)

###################################


    #system file (mem)
    #if memory_dir_name:
    #    memory_dir_name = ".{}".format(memory_dir_name)
    #else:pass
    # validation of inputs
    if intel_dir or get or readme or file__ or flush:pass
    else:
        print ("[+] ")
        print ("[+] Please supply input")
        print ("[+] This tool, uses two(2) options")
        print ("[+] -f to specify an intel file")
        print ("[+] -d to specify a directory containing intel files")
        print ("[+] -R to README")
        print ("[+] -g to specify a key stored in memcache to get value")
        print ("[+] -X to flush/reset the application, this will clear all log files")
        print ("[+] ")





    # for readme
    if readme == True:
        rm_="""
    Author: Hud Seidu Daannaa
    README.md
    =========
    This tool, ships data to a specified memcache servers in settings.ini,
    Data is send in parallel, hence this is done to produce availability and
    redundency. a folder is created during operation of the program, which heps
    to save the applications state. the absence of that folder, will trigger the application
    to start all over again (as a new start).
    IMPORTANT: All commands or flags, initiated, will apply to all servers.
    the application takes a file as input. this file should contain data of the
    form:
    'key':'value' # hence the key, values should be strings.
    HENCE, THIS TOOL, TAKES JSON AS INPUT, THIS MEANS TO SEND DATA INTO MEMCACHE,
    TH TEXT FILE LOADED SHOULD BE JSON. OF THE FORM:
        {'name':'hud'}
        {'age':'x~2'}
    //the above format should be the content of the text file ...

    form the settings.ini file, you can specify the key (document_key_field) to 
    use within the documents in the file

    to run tool:
    chmod +x x1.py
    ./x1.py or

    python ./x1.py

    NOTE: use --help to view flags
    """
        print rm_
        sys.exit()


####################################33




    #to clean application files
    if flush == True:
    
        tof = ''
        while True:

            signal.signal(signal.SIGINT, handler)
            print ("")
            tof = str(raw_input("[X]To continue enter [Y/N]: "))
            print ("")
            tof = tof.upper()
            if tof == 'Y':
                try:                                      
                    time.sleep(1)
                    #os.remove(memory_dir_name)
                    shutil.rmtree(memory_dir_name)
                    print ("[+] Flushing complete for mem file !")
                    #break
                    sys.exit()
                except Exception as e:
                    print ("[+] File might been already cleaned")
                    print ("")
                    #print e
                    sys.exit()
                    #print ("[+] Memory file already cleaned")
                
            elif tof == 'N':
                print ("")
                print ("[+] Exiting ...")
                print ("")
                time.sleep(1)
                sys.exit()
            else:
                print ("")
                print ("            !!! You have to specify [Y/N] for Yes or no /Damb damb/ !!!")
                print ("")
                pass





    #check log file (set)
    if intel_dir:
        try:os.mkdir(memory_dir_name)       
        except:pass

        threads = list()
        for address in addresses:
            #signal.signal(signal.SIGINT, handler)        
            #fcn(address, memory_dir_name, file__)
            x = threading.Thread(target=fcn_v2, args=(address, memory_dir_name, intel_dir,))
            threads.append(x)
            x.start()
            
    if file__:
        try:os.mkdir(memory_dir_name)       
        except:pass

        threads = list()
        for address in addresses:
            #signal.signal(signal.SIGINT, handler)        
            #fcn(address, memory_dir_name, file__)
            x = threading.Thread(target=fcn_v1, args=(address, memory_dir_name, file__,))
            threads.append(x)
            x.start()



        
    
    #to cross validate, (get)
    if get:
        
        try:os.mkdir(memory_dir_name)       
        except:pass
        
        for address in addresses:
        
            host = address.split(':')[0]
            port = address.split(':')[1]
            logfilename=os.path.join(memory_dir_name, "{}_operation_log.log".format(memory_dir_name))
            #touch(memfile_add)
            
            log("", logfilename)
            log("[+] ", logfilename)
            log("[+] Server: {}".format(address), logfilename)
            log("[+] =====================", logfilename)
            log("[+] =====================", logfilename)
            log("", logfilename)
            
            try:
                ky = str(get.strip())
                log ("[+] Query/GET for key: {0} | in memcache [SERVER]: {1}".format(str(ky), address), logfilename)               
                #print ("")
                #print ("[+] Checking memcache to key: {}".format(str(ky)))
                #print ("[+] ======")
                #print ("value:")
                client = Client((str(host), int(port)))
                result = client.get(ky)
                #print ("")
                #print (result)
                log (result, logfilename)
                #print ("")
            except Exception as err:
                log ("[+] Whilst using: GET | Could not connect to server, due to ..", logfilename)
                log (err, logfilename)
            log("[+] =====================", logfilename)
            log("", logfilename)

if __name__ == "__main__":
    main_hud()
    #pass


