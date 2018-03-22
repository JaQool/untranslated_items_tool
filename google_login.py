import gspread
import sys
import json
from oauth2client.service_account import ServiceAccountCredentials
scope = "https://spreadsheets.google.com/feeds"
credentials = ServiceAccountCredentials.from_json_keyfile_name('untranslated-items-report-99371886db1e.json', scope)
gs = gspread.authorize(credentials)
gsheet = gs.open_by_key('1c5bIqiIz8A_bT595kr_vI9fN7U1dkFDnk6Q3uwl3Tb0')
wsheet = gsheet.worksheet("sheet1")
input = sys.stdin.read()
#if input == '':
#    input = 'untranslated_items.json'
#input = 'test_empty.json'
with open(input, 'r') as fp:
    obj = json.load(fp)

new_items_count = 0
fixed_items_count = 0
boundary = 1
wsheet.update_acell('A' + str(boundary), 'Preparing to update...')
wsheet.clear()

fixed_projects = []
broken_projects = []
for index, element in enumerate(obj['result']):
    print (type(element))
    print (element['fixed_flag'])
    if element['fixed_flag'] == 1:
        fixed_projects.append(element)
    else:
        broken_projects.append(element)
    
wsheet.update_acell('A' + str(boundary), 'PROJECTS WITH UNTRANSLATED ITEMS')

if len(broken_projects) != 0:
    #get the unique project codes
    project_codes = dict()
    items_in_project = dict()
    for index, element in enumerate(broken_projects):
        if element['project_cd'] not in items_in_project.keys():
            items_in_project[element['project_cd']] = []

        items_in_project[element['project_cd']].append(element)

        if element['project_cd'] not in project_codes.values():
            project_codes[index] = element['project_cd']
        else:
            project_codes[index] = 'repeated project code'

    counter = 0
    for index, element in enumerate(broken_projects): 
        if (project_codes[index] is not 'repeated project code'):
            boundary += 2
            counter += 1
            wsheet.update_acell('A' + str(boundary), counter)
            wsheet.update_acell('B' + str(boundary), 'https://tripnscan.com/' + project_codes[index])
            boundary += 1
            wsheet.update_acell('B' + str(boundary), 'This project contains ' + str(len(items_in_project[project_codes[index]])) + ' untranslated items.')
            for item in items_in_project[project_codes[index]]:
                boundary += 1
                wsheet.update_acell('B' + str(boundary), item['master_name'])
                if item['repeats'] == 0:
                    new_items_count += 1
                wsheet.update_acell('C' + str(boundary), 'untranslated for ' + str(item['repeats'] + 1) + ' day(s)')
                wsheet.update_acell('D' + str(boundary), item['lang_cd'])
                wsheet.update_acell('E' + str(boundary), format(float(item['version']), '7.2f'))

    boundary += 1
    wsheet.update_acell('B' + str(boundary), 'versions guide:')
    boundary += 1
    wsheet.update_acell('B' + str(boundary), "1.000 and below: This item hasn't gone through 4D yet. It should be processed soon so let's hold on.")
    boundary += 1
    wsheet.update_acell('B' + str(boundary), "1.010 - 2.000: This item went through 4D but something went wrong and it didn't get translated.") 
    boundary += 1
    wsheet.update_acell('B' + str(boundary), "Above 2.000: This version is incorrect. Something is wrong here, please report this.")

else:
    boundary += 2
    wsheet.update_acell('A' + str(boundary), 'no projects found')

boundary += 2
wsheet.update_acell('A' + str(boundary), 'PROJECTS WITH ITEMS FIXED TODAY')

if len(fixed_projects) != 0:
    #get the unique project codes
    project_codes = dict()
    items_in_project = dict()
    for index, element in enumerate(fixed_projects):
        if element['project_cd'] not in items_in_project.keys():
            items_in_project[element['project_cd']] = []
        
        items_in_project[element['project_cd']].append(element)

        if element['project_cd'] not in project_codes.values():
            project_codes[index] = element['project_cd']
        else:
            project_codes[index] = 'repeated project code'

    counter = 0
    for index, element in enumerate(fixed_projects):
        if (project_codes[index] is not 'repeated project code'):
            boundary += 2
            counter += 1
            wsheet.update_acell('A' + str(boundary), counter)
            wsheet.update_acell('B' + str(boundary), 'https://tripnscan.com/' + project_codes[index])
            boundary += 1
            wsheet.update_acell('B' + str(boundary), str(len(items_in_project[project_codes[index]])) + " of this project's items got successfully translated after having previously appeared in this list.")
            for item in items_in_project[project_codes[index]]:
                boundary += 1
                wsheet.update_acell('B' + str(boundary), item['master_name'])
                fixed_items_count += 1
                wsheet.update_acell('C' + str(boundary), 'untranslated for ' + str(item['repeats'] + 1) + ' day(s)')
                wsheet.update_acell('D' + str(boundary), item['lang_cd'])
                wsheet.update_acell('E' + str(boundary), format(float(item['version']), '7.2f'))

    boundary += 1
    wsheet.update_acell('B' + str(boundary), 'versions guide:')
    boundary += 1
    wsheet.update_acell('B' + str(boundary), '1.000 and below: This version is incorrect. Something is wrong here, please report this.') 
    boundary += 1
    wsheet.update_acell('B' + str(boundary), "1.010 - 2.000: This item was successfully processed by 4D.") 
    boundary += 1
    wsheet.update_acell('B' + str(boundary), "Above 2.000: The translation was handled by the human translation team.") 

else:
    boundary += 2
    wsheet.update_acell('A' + str(boundary), 'no projects found')

sys.stdout.write('' + str(new_items_count) + ' new items were encountered, and ' + str(fixed_items_count) + ' previously broken items were fixed.')
sys.stdout.flush()
sys.exit(0)
