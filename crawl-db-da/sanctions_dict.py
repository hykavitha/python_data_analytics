types = ('name', 'alt_name', 'addr')

tables = {'name': 'sanctions_names', 'alt_name': 'sanctions_alternatenames', 'addr': 'sanctions_addresses'}

insert_command_types = {
    'name': 'insert into sanctions.sanctions_names  (id, name,description, source, date_added) values',
    'alt_name': 'insert into sanctions.sanctions_alternatenames  (id, id1,name,source, date_added) values',
    'addr': 'insert into sanctions.sanctions_addresses (id, id1,address,source) values'
}



list_dict = [

    {
        'source': 'UN',
        'url': 'https://scsanctions.un.org/al-qaida/',
        'fetch_type': 'xml',
        'name': ['dataid', 'first_name', 'second_name', 'third_name', 'fourth_name', 'comments1'],
        'alt_name': ['dataid', 'alias_name'],
        'addr': ['dataid', 'street', 'city', 'country']
    },
    {
        'source': 'OFAC-NON-SDN',
        'url': 'https://www.treasury.gov/ofac/downloads/consolidated/consall.zip',
        'fetch_type': 'zip',
        'name': 'cons_prim.csv',
        'alt_name': 'cons_alt.csv',
        'addr': 'cons_add.csv',
        "cons_alt.csv": ['ent_num', 'alt_num', 'alt_type', 'alt_name', 'alt_remarks'],
        "cons_add.csv": ['ent_num', 'add_num', 'address', 'city_state_zip', 'country', 'add_remarks'],
        "cons_prim.csv": ['ent_num', 'sdn_name', 'sdn_type', 'program', 'title',
                          'call_sign', 'vess_type', 'tonnage', 'grt', 'vess_flag', 'vess_owner', 'remarks']

    }

]

