# SANCTIONS
# Description: Script to parse xml sanctions lists
# Python 3.5

import os
import csv
import xml.etree.ElementTree as ElementTree

# directory where xml lists are held
xml_lists = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'xml_lists')

print(xml_lists)
# directory where lists that need to be imported into sql are held
lists_to_import = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'lists_to_import')
print(lists_to_import)

# set headers for csvs
fields_Name = ['ID', 'Name', 'Description', 'Source']
fields_Alt_Name = ['ID', 'ID1', 'Name1', 'Source']
fields_Address = ['ID', 'ID1', 'Address', 'Source']

# intialize csvs
# # names
# with open(os.path.join(lists_to_import, 'UN_EU_Sanctions_Name.csv'), "w", encoding='utf-16') as csv_name:
#     writer_name = csv.DictWriter(csv_name, delimiter="|", lineterminator="\n", fieldnames=fields_Name)
#     writer_name.writeheader()
#
# # alt names
# with open(os.path.join(lists_to_import, 'UN_EU_Sanctions_Alt_Name.csv'), "w", encoding='utf-16') as csv_alt_name:
#     writer_alt_name = csv.DictWriter(csv_alt_name, delimiter="|", lineterminator='\n', fieldnames=fields_Alt_Name)
#     writer_alt_name.writeheader()
#
# # address
# with open(os.path.join(lists_to_import, 'UN_EU_Sanctions_Address.csv'), "w", encoding='utf-16') as csv_addr:
#     writer_addr = csv.DictWriter(csv_addr, delimiter="|", lineterminator='\n', fieldnames=fields_Address)
#     writer_addr.writeheader()

# loop through xml lists in directory
for subdir, dirs, files in os.walk(xml_lists):

    # for each xml file
    for x in files:
        print("in foor loop " + x)
        ################################ UN ################################
        # if it's the UN xml
        if 'UN' in x:
            print('UN sanctions list')

            # get xml tree
            tree = ElementTree.parse(os.path.join(xml_lists, x))
            root = tree.getroot()

            name_tags = ['DATAID', 'FIRST_NAME', 'SECOND_NAME', 'THIRD_NAME', 'FOURTH_NAME', 'COMMENTS1']
            alt_name_tags = ['DATAID', 'ALIAS_NAME']
            addr_tags = ['DATAID', 'STREET', 'CITY', 'COUNTRY']

            # go through all individuals
            for i in root.findall('INDIVIDUALS'):
                print('Individuals')

                for indiv in i.findall('INDIVIDUAL'):

                    # NAMES
                    # open csvs for writing
                    with open(os.path.join(lists_to_import, 'UN_EU_Sanctions_Name.csv'), "a",
                              encoding='utf-16') as csv_name:
                        writer_name = csv.DictWriter(csv_name, delimiter="|", lineterminator="\n",
                                                     fieldnames=fields_Name)

                        # declare list to hold results
                        results = []

                        # find and add the id
                        id = indiv.find('DATAID').text
                        results.append(id)

                        # add other fields based on list of tags to look for
                        for f in range(1, len(name_tags)):
                            if indiv.find(name_tags[f]) is None:
                                results.append('')
                            else:
                                results.append(str(indiv.find(name_tags[f]).text).replace('\n', ''))

                        # add name results to csv
                        try:
                            print("Name", results)
                        except:
                            print("Could not print name")

                        writer_name.writerow({fields_Name[0]: str('UN' + results[0]),
                                              fields_Name[1]: str(results[1] + results[2] + results[3] + results[4]),
                                              fields_Name[2]: results[5], fields_Name[3]: 'UN'})

                        # ALT NAMES
                        with open(os.path.join(lists_to_import, 'UN_EU_Sanctions_Alt_Name.csv'), "a",
                                  encoding='utf-16') as csv_alt_name:
                            writer_alt_name = csv.DictWriter(csv_alt_name, delimiter="|", lineterminator='\n',
                                                             fieldnames=fields_Alt_Name)

                            for alias in indiv.findall('INDIVIDUAL_ALIAS'):
                                results = []
                                results.append(id)

                                for f in range(1, len(alt_name_tags)):
                                    if alias.find(alt_name_tags[f]) is None:
                                        results.append('')
                                    else:
                                        results.append(str(alias.find(alt_name_tags[f]).text).replace('\n', ''))

                                try:
                                    print("Alt Name", results)
                                except:
                                    print("Could not print alt name")

                                writer_alt_name.writerow(
                                    {fields_Alt_Name[0]: str('UN' + results[0]), fields_Alt_Name[1]: '',
                                     fields_Alt_Name[2]: results[1], fields_Alt_Name[3]: 'UN'})

                        # ADDRESS NAMES
                        with open(os.path.join(lists_to_import, 'UN_EU_Sanctions_Address.csv'), "a",
                                  encoding='utf-16') as csv_addr:
                            writer_addr = csv.DictWriter(csv_addr, delimiter="|", lineterminator='\n',
                                                         fieldnames=fields_Address)

                            for addr in indiv.findall('INDIVIDUAL_ADDRESS'):
                                results = []
                                results.append(id)

                                for f in range(1, len(addr_tags)):
                                    if addr.find(addr_tags[f]) is None:
                                        results.append('')
                                    else:
                                        results.append(str(addr.find(addr_tags[f]).text).replace('\n', ''))
                                try:
                                    print("Address", results)
                                except:
                                    print("Could not print addr")

                                writer_addr.writerow({fields_Address[0]: str('UN' + results[0]), fields_Address[1]: '',
                                                      fields_Address[2]: str(results[1] + results[2] + results[3]),
                                                      fields_Address[3]: 'UN'})

            name_tags = ['DATAID', 'FIRST_NAME', 'SECOND_NAME', 'THIRD_NAME', 'FOURTH_NAME', 'COMMENTS1']
            alt_name_tags = ['DATAID', 'ALIAS_NAME']
            addr_tags = ['DATAID', 'STREET', 'CITY', 'COUNTRY']

        ################################ EU ################################
        if 'EU' in x:
            print('EU sanctions list')

            # intialize csvs
            # names
            with open(os.path.join(lists_to_import, 'UN_EU_Sanctions_Name.csv'), "w", encoding='utf-16') as csv_name:
                writer_name = csv.DictWriter(csv_name, delimiter="|", lineterminator="\n", fieldnames=fields_Name)
                writer_name.writeheader()

            # alt names
            with open(os.path.join(lists_to_import, 'UN_EU_Sanctions_Alt_Name.csv'), "w",
                      encoding='utf-16') as csv_alt_name:
                writer_alt_name = csv.DictWriter(csv_alt_name, delimiter="|", lineterminator='\n',
                                                 fieldnames=fields_Alt_Name)
                writer_alt_name.writeheader()

            # get xml tree
            tree = ElementTree.parse(os.path.join(xml_lists, x))
            root = tree.getroot()

            # lists of tags to search for in xml
            name_tags = ['Id', 'WHOLENAME', 'FUNCTION']
            alt_name_tags = ['Id', 'WHOLENAME']

            # for all entities in the EU list
            for entity in root.findall('ENTITY'):

                # save the id
                id = entity.attrib['Id'].replace('\n', '')

                n = 0
                for name in entity.findall('NAME'):

                    # add first name in xml to Name csv
                    if n == 0:

                        with open(os.path.join(lists_to_import, 'UN_EU_Sanctions_Name.csv'), "a",
                                  encoding='utf-16') as csv_name:
                            writer_name = csv.DictWriter(csv_name, delimiter="|", lineterminator="\n",
                                                         fieldnames=fields_Name)

                            # declare list to hold results
                            results = []

                            # save the id
                            results.append(id)

                            # add other fields based on list of tags to look for
                            for f in range(1, len(name_tags)):
                                if name.find(name_tags[f]) is None:
                                    results.append('')
                                else:
                                    results.append(str(name.find(name_tags[f]).text).replace('\n', ''))

                            # add name results to csv
                            try:
                                print("Name", results)
                            except:
                                print("Could not print name")

                            writer_name.writerow(
                                {fields_Name[0]: str('EU' + results[0]), fields_Name[1]: str(results[1]),
                                 fields_Name[2]: results[2], fields_Name[3]: 'EU'})

                            n = 1

                    # add the next names to Alt Names
                    else:
                        with open(os.path.join(lists_to_import, 'UN_EU_Sanctions_Alt_Name.csv'), "a",
                                  encoding='utf-16') as csv_name:
                            writer_alt_name = csv.DictWriter(csv_name, delimiter="|", lineterminator="\n",
                                                             fieldnames=fields_Alt_Name)

                            # declare list to hold results
                            results = []

                            # save the id
                            results.append(id)

                            # add other fields based on list of tags to look for
                            for f in range(1, len(alt_name_tags)):
                                if name.find(alt_name_tags[f]) is None:
                                    results.append('')
                                else:
                                    results.append(str(name.find(alt_name_tags[f]).text).replace('\n', ''))

                            # add name results to csv
                            try:
                                print("Alt Name", results)
                            except:
                                print("Could not print alt name")

                            writer_alt_name.writerow(
                                {fields_Alt_Name[0]: str('EU' + results[0]), fields_Alt_Name[1]: '',
                                 fields_Alt_Name[2]: results[1], fields_Alt_Name[3]: 'EU'})






# xml2df = xml_dataframe()