import gspread
import sys
import json
from oauth2client.service_account import ServiceAccountCredentials
scope = "https://spreadsheets.google.com/feeds"
keyfile = "/home/ec2-user/untranslated_items_tool/untranslated-items-report-99371886db1e.json"
credentials = ServiceAccountCredentials.from_json_keyfile_name(keyfile, scope)
gs = gspread.authorize(credentials)
gsheet = gs.open_by_key('1eN-8NGNfxAL0VbW28-TnTnr5TaNQDj2e-1IKNRqf4Bk')
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
    if element['fixed_flag'] == 1:
        fixed_projects.append(element)
    else:
        broken_projects.append(element)
    
row_a = {}
row_b = {}
row_c = {}
row_d = {}
row_e = {}

#wsheet.update_cells('A' + str(boundary), counter)

#wsheet.update_acell('A' + str(boundary), 'PROJECTS WITH UNTRANSLATED ITEMS')

row_a[boundary] = ('PROJECTS WITH UNTRANSLATED ITEMS')

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
            row_a[boundary] = (counter)
            row_b[boundary] = ('https://tripnscan.com/' + project_codes[index])
            boundary += 1
            row_b[boundary] = ('This project contains ' + str(len(items_in_project[project_codes[index]])) + ' untranslated items.')
            for item in items_in_project[project_codes[index]]:
                boundary += 1
                row_b[boundary] = (item['master_name'])            
                if item['repeats'] == 0:
                    new_items_count += 1
                row_c[boundary] = ('untranslated for ' + str(item['repeats'] + 1) + ' day(s)') 
                row_d[boundary] = (item['lang_cd'])
                row_e[boundary] = (float(item['version'])) 

    boundary += 1
    row_b[boundary] = ('versions guide:') 
    boundary += 1
    row_b[boundary] = ("1.000 and below: This item hasn't gone through 4D yet. It should be processed soon so let's hold on.") 
    boundary += 1
    row_b[boundary] = ("1.010 - 2.000: This item went through 4D but something went wrong and it didn't get translated.")
    boundary += 1
    row_b[boundary] = ("Above 2.000: This version is incorrect. Something is wrong here, please report this.")    

else:
    boundary += 2
    row_a[boundary] = ('no projects found')

boundary += 2
row_a[boundary] = ('PROJECTS WITH ITEMS FIXED TODAY')

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
            row_a[boundary] = (counter)
            wsheet.update_acell('B' + str(boundary), 'https://tripnscan.com/' + project_codes[index])
            row_b[boundary] = ('https://tripnscan.com/' + project_codes[index])
            boundary += 1
            row_b[boundary] = (" of this project's items got successfully translated after having previously appeared in this list.")
            for item in items_in_project[project_codes[index]]:
                boundary += 1
                row_b[boundary] = (item['master_name'])
                fixed_items_count += 1
                row_c[boundary] = ('untranslated for ' + str(item['repeats'] + 1) + ' day(s)')
                row_d[boundary] = (item['lang_cd'])
                row_e[boundary] = (float(item['version']))

    boundary += 1
    row_b[boundary] = 'versions guide:'
    boundary += 1
    row_b[boundary] = '1.000 and below: This version is incorrect. Something is wrong here, please report this.'
    boundary += 1
    row_b[boundary] = "1.010 - 2.000: This item was successfully processed by 4D."
    boundary += 1
    row_b[boundary] = "Above 2.000: The translation was handled by the human translation team."

else:
    boundary += 2
    row_a[boundary] = 'no projects found'

cell_list_a = wsheet.range("A1:A" + str(boundary))
cell_list_b = wsheet.range("B1:B" + str(boundary))
cell_list_c = wsheet.range("C1:C" + str(boundary))
cell_list_d = wsheet.range("D1:D" + str(boundary))
cell_list_e = wsheet.range("E1:E" + str(boundary))

for index, cell in enumerate(cell_list_a, start=1):
    if index in row_a:
        cell.value = row_a[index]
for index, cell in enumerate(cell_list_b, start=1):
    if index in row_b:
        cell.value = row_b[index]
for index, cell in enumerate(cell_list_c, start=1):
    if index in row_c:
        cell.value = row_c[index]
for index, cell in enumerate(cell_list_d, start=1):
    if index in row_d:
        cell.value = row_d[index]
for index, cell in enumerate(cell_list_e, start=1):
    if index in row_e:
        cell.value = row_e[index]

wsheet.update_cells(cell_list_a)
wsheet.update_cells(cell_list_b)
wsheet.update_cells(cell_list_c)
wsheet.update_cells(cell_list_d)
wsheet.update_cells(cell_list_e)
sys.stdout.write('' + str(new_items_count) + ' new items were encountered, and ' + str(fixed_items_count) + ' previously broken items were fixed.')
sys.stdout.flush()
sys.exit(0)
