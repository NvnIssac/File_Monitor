import os,shutil,json,re

#Script searches for the json file in current directory
path1=os.getcwd()+"\API_JSON.json"
path2=os.getcwd()+"\API_JSON.json.bkup"

def json_compare(json1, json2):
    '''
    :param json1: Json been modified
    :param json2: Json content before modification
    :return: Message containing information of the Jsons updated/Created/Removed
    '''

    msg=""
    original_ssid=[i['ssid'] for i in json1]
    modified_ssid=[j['ssid'] for j in json2]

    for i in json1:
        if i['ssid'] not in modified_ssid:
            msg += i['ssid'] + " is added to the list SNR " + str(i['snr']) +" channel "+ str(i['channel']) + "\n"

    for j in json2:
        if j['ssid'] in original_ssid:
            for m in json1:
                if m['ssid']==j['ssid']:
                    for k in j.keys():
                        if j[k]!=m[k]:
                            msg += j['ssid'] + k + " has changed from " + str(m[k]) + " to " + str(j[k]) + "\n"
        else:
            msg += j['ssid'] + " is removed from the list" + "\n"

    return msg

def convert_format(j1):
    '''
    :param j1: Json Content extract read from file in string format is converted into list of dictionaries
    :return: List of Dictionaries
    '''
    lis=["{",'}','[',']',',']
    l=[]
    for i in j1:
        if i.strip() not in lis:
            l.append(i)

    return [json.loads('{' + re.sub(r'\'', '"', i) + '}') for i in l[1:]]

def file_cmp(p1,p2):
    '''
    :param p1: Path of json modified file
    :param p2: Path of json backup
    :return: None
    Post the validation of Json changes, we copy the modified file content to the json backup
    '''
    with open(p1) as infile:
        f1 = infile.read().strip(' ').split('\n')

    with open(p2) as outfile:
        f2 = outfile.read().strip(' ').split('\n')
        
    update_content = convert_format(f1)
    original_content = convert_format(f2)

    print(json_compare(update_content,original_content))

    if update_content or original_content:
        shutil.copy(p1,p2)

if __name__=="__main__":
    file_cmp(path1,path2)


