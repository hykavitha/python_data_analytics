__author__ = "Kavitha Yogaraj"
__status__ = "Development"

# -------------------------------------------------------------
# Import Packages required for Running Code
# -------------------------------------------------------------

import traceback

import os
import sys
from urllib.request import urlopen
import pandas as pd

import pandas as pd
import zipfile, io
import numpy as np
import re
import datetime
# importing module
import logging

# Create and configure logger
logging.basicConfig(filename="sanctions_etl.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

# Creating an object
log = logging.getLogger()

# Setting the threshold of logger to DEBUG
log.setLevel(logging.INFO)

util_path = os.path.join(os.path.abspath(os.path.dirname("__file__")), os.pardir, os.pardir, os.pardir)
sys.path.insert(0, util_path)

import time
from sanctions_dict import *
from db_wrapper import *


class Sanctions:
    """
        this class gets data for all 4 sources and updates table : https://scsanctions.un.org/resources/xml/en/consolidated.xml

    """
    # xml_urls = [ 'https://scsanctions.un.org/al-qaida/',
    #             'https://scsanctions.un.org/resources/xml/en/consolidated.xml', ]

    """ sources, url sources and whether it is xml sources or not"""
    """ to keep url fetched data so once fetched is available many times"""
    response_data = ''
    xml_response_data = ''
    zipped = ''
    db_connect = ''
    xml2df = ''

    def __init__(self):
        pass

    """ Using db_wrapper.py  data"""

    def db_hndlr(self):
        # Give the table name into which the panda should get appended to
        try:
            log.info("======Creating DB Handler using config.ini to read Db Settings ========")
            self.db_connect = db_wrapper()
            print("after getting db:" )
            print(self.db_connect)
            #self.xml2df = xml_dataframe()
            #print(self.xml2df)

            return True
        except Exception as err:

            log.critical("Error occured while readin the db settings from config.ini file and the error is %s" % (err))
            self.db_connect = None
            log.critical("exiting the process.....")
            return False
        return True

    def single_quote(self, s1):
        return "'%s'" % s1

    #prepare for insert
    def insert_data(self, insert_query):

        log.info("---db_insert, the insert query is :" + insert_query)
        print("---db_insert, the insert query is :" + insert_query)
        message = ''
        stat = False
        try:
            results = self.db_connect.cursor.execute(insert_query)
            self.db_connect.conn.commit()
            log.info("---db_inserted, the insert query is :" + insert_query)


        except Exception as e:
            stat = False
            print("exception at db_insert")
            print(e)
            print(traceback.format_exc())


        if not stat:
            message = 'Error occurred while inserting this record'
        return stat, message

    # """ this function is used for sanction names upload on UN data alone, there is a problem in my xml_dataframe"""

    def get_xml_dataframe(self, source_dict, type):
        # todo parse entities
        stat = False
        df = ''


        try:
            log.info("---get_xml_dataframe, parsing the xml for source: " + source_dict['source'] + " for type: " + type)
            print("before getting xml_dataframe")
            print("---get_xml_dataframe, parsing the xml for source: " + source_dict['source'] + " for type: " + type)
            #print (self.xml_response_data)
            f = open('/Users/KaviAnu/Documents/python_data_analytics/consall/xml_data.txt', 'w')
            f.write(self.xml_response_data)
            exit(10)

            self.xml2df.parse_xml(self.xml_response_data)

        except Exception as e:
            f = open('/Users/KaviAnu/Documents/python_data_analytics/consall/xml_data.txt', 'w')
            f.write(self.xml_response_data)

            print("Error occured in get_xml_dataframe, parsing the xml and error is %s" % (e))
            exit(3)
            return stat, df

        log.info("---get_xml_dataframe, getting individulas & entities for type: " + type)

        if type == 'name':
            for attribute in self.xml2df.root:
                for indiv in attribute.iter('INDIVIDUALS'):
                    df = self.xml2df.process_data(indiv)
                for entity in attribute.iter('ENTITIES'):
                    df2 = self.xml2df.process_data(entity)

            frames = [df, df2]
            df = pd.concat(frames)
            log.info("---get_xml_dataframe, concatenated dataframe  for type " + type)

            return stat, df

        if type == 'alt_name':
            results = dict()
            tags = ['INDIVIDUAL', 'ENTITY']
            frames = []
            for tag in tags:

                for indiv in self.xml2df.root.iter(tag):
                    for i, alias in enumerate(indiv.findall(tag + '_ALIAS')):
                        id = indiv.find('DATAID').text + '_' + str(i)
                        results[id] = []
                        for f in range(1, len(source_dict[type])):
                            if alias.find(source_dict[type][f]) is None:
                                results[id] = ''
                            else:
                                results[id] = str(alias.find(source_dict[type][f]).text).replace('\n', '')
                    frames.append(pd.DataFrame(list(results.items()), columns=['DATAID', 'ALIAS_NAME']))
            df = pd.concat(frames)
            log.info("---get_xml_dataframe, concatenated dataframe  for type " + type)

            if type == 'addr':
                results = dict()
                tags = ['INDIVIDUAL', 'ENTITY']
                frames = []
                for tag in tags:

                    for indiv in self.xml2df.root.iter(tag):
                        for i, alias in enumerate(indiv.findall(tag + 'ADDRESS')):
                            id = indiv.find('DATAID').text + '_' + str(i)
                            results[id] = []
                            for f in range(1, len(source_dict[type])):
                                if alias.find(source_dict[type][f]) is None:
                                    pass
                                else:
                                    results[id] = str(alias.find(source_dict[type][f]).text).replace('\n', '')
                        frames.append(pd.DataFrame(list(results.items()), columns=['DATAID', 'ALIAS_NAME']))

                df = pd.concat(frames)
                #log.info("---get_xml_dataframe, concatenated dataframe  for type " + type)

        return stat, df

    def get_url(self, url):
        # get url, check errors and update
        res = {}
        stat = False
        try:
            #log.info("---get_url, url to fetch is :" + url)
            response = urlopen(url)

            stat = False
        except urlopen.error.HTTPError as e:
            # Return code error (e.g. 404, 501, ...)
            print('HTTPError: {}'.format(e.code))
            #log.critical('HTTPError: {}'.format(e.code))
            stat = False
        except urlopen.error.URLError as e:
            # Not an HTTP-specific error (e.g. connection refused)
            print('URLError: {}'.format(e.reason))
            #log.critical('URLError: {}'.format(e.code))
            stat = False
        else:
            # 200
            #log.info("---get_url, url to fetch is successful")
            response_data = response.read()
            stat = True
        return stat, response_data

    # as logic to get the url data and keep the response
    # in response_data if its xml/ in zipped if it zip data
    def fetch_data(self, source_dict):
        stat = False
        #log.info("---fetch_data, for this source and fetch type {} {}".format(source_dict['source'],source_dict['fetch_type']))
        if source_dict['fetch_type'] == 'xml':
            print("xml url: " +source_dict['url'])

            stat, self.xml_response_data = self.get_url(source_dict['url'])

        else:
            if source_dict['fetch_type'] == 'zip':
                stat, response_data = self.get_url(source_dict['url'])
                self.zipped = zipfile.ZipFile(io.BytesIO(response_data))

        return stat

    def read_file(self, source_dict, file_name):
        source_col_names = source_dict[file_name]
        stat = False
        #log.info("---read_file, for this source and these are the columns {} {}".format(source_dict['source'],                                                                                        source_dict[file_name]))
        try:
            with self.zipped.open(file_name) as f:
                df = pd.read_csv(f, header=None, delimiter=",", names=source_col_names)
        except Exception as e:
            #log.critical("Error occured while reading the file and error is %s" % (e))

            return stat, False
        stat = True
        return stat, df

    def process_df(self, df):
        #log.info("---process_df, for this source and these are the columns")
        stat = False
        try:
            df_obj = df.select_dtypes(['object'])
            # manipulate values in df, trim extra space, replace single quotoes, replace -0- value
            df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
            df[df_obj.columns] = df_obj.apply(lambda x: x.str.replace("'", "\''"))
            df = df.replace({"\n": ' '}, regex=True)
            df = df.replace({"\t": ' '}, regex=True)

            # df = df.replace({'\s+': ' '}, regex=True)
            df = df.replace({'-0-': ''}, regex=True)
            df.columns = map(str.lower, df.columns)
            df = df.replace(np.nan, '', regex=True)
            df.columns = map(str.lower, df.columns)
        except Exception as e:
            #log.critical("Error occured while processing the df and error is %s" % (e))

            return stat, False
        stat = True
        return stat, df

    def datetime_now(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def make_queries_xml(self, df, source_dict, type):

        #log.info("---make_queries_xml, for this source and its xml type {} ".format(source_dict['source']))

        query_list = []
        stat = False
        df['dataid'] = df['dataid'].apply(lambda x: x.split("_")[0])
        df['id'] = df['dataid'].apply(lambda x: 'UN' + str(x))

        for index, row in df.iterrows():
            ID1 = self.single_quote('')

            if type == 'name':
                name = self.single_quote(
                    '{} {} {} {}'.format(row['first_name'], row['second_name'], row['third_name'], row['fourth_name']))

                query_value = "( " \
                              + self.single_quote(row['id']) + ", " \
                              + name + ", " \
                              + self.single_quote(row['comments1']) + ", " \
                              + source_dict['source'] + ", " \
                              + self.single_quote(self.datetime_now()) + ") "

            if type == 'alt_name':
                query_value = "( " + \
                              self.single_quote(row['id']) + ", " \
                              + ID1 + ", " \
                              + self.single_quote(row['alias_name']) + ", " \
                              + self.single_quote(source_dict['source']) + ", " \
                              + self.single_quote(self.datetime_now()) + ") "

            if type == 'addr':
                query_value = "( " + \
                              self.single_quote(row['id']) + ", " \
                              + ID1 + ", " + self.single_quote(row['address']) + ", " \
                              + self.single_quote(source_dict['source']) + ") "

            query = '{} {}'.format(insert_command_types[type], query_value)
            query_list.append(query)
            stat = True
        #log.info("---make_queries_xml, length of query_list  {} ".format(len(query_list)))

        return query_list

    def make_queries(self, df, source_dict, type):
        #log.info("---make_queries, for this source and its zip type  {} ".format(source_dict['source']))

        # alt_names
        query_list = []
        stat = False
        # this is only for altname ID1
        df['ent_num'] = df['ent_num'].apply(lambda x: 'OFAC' + str(x))

        if type == 'alt_name':
            df['alt_num'] = df['alt_num'].apply(lambda x: 'OFAC' + str(int(x)) if x != '' else '')
        if type == 'addr':
            df['add_num'] = df['add_num'].apply(lambda x: 'OFAC' + str(int(x)) if x != '' else '')

        for index, row in df.iterrows():
            query_value = ''
            if type == 'alt_name':
                query_value = "( " + self.single_quote(row['ent_num']) + ", " \
                              + self.single_quote(row['alt_num']) + ", " \
                              + self.single_quote(row['alt_name']) + ", " \
                              + self.single_quote(source_dict['source']) + ", " \
                              + self.single_quote(self.datetime_now()) + ") "

            if type == 'name':
                desc = self.single_quote(
                    '{} {} {} {} {} {} {} {} {} {}'.format(row['sdn_type'], row['program'], row['title'],
                                                           row['call_sign'], row['vess_type'], row['tonnage'],
                                                           row['grt'], row['vess_flag'], row['vess_owner'],
                                                           row['remarks']))
                desc = re.sub('\s+', ' ', desc).strip()
                query_value = "( " + self.single_quote(row['ent_num']) + ", " + self.single_quote(
                    row['sdn_name']) + ", " + desc + ", " + self.single_quote(
                    source_dict['source']) + ", " + self.single_quote(self.datetime_now()) + ") "
            if type == 'addr':
                address = self.single_quote(
                    '{} {} {} {}'.format(row['address'], row['city_state_zip'], row['country'], row['add_remarks']))
                address = re.sub('\s+', ' ', address).strip()
                query_value = "( " + self.single_quote(row['ent_num']) + ", " + self.single_quote(
                    row['add_num']) + ", " + address + ", " + self.single_quote(source_dict['source']) + ")"

            # after everything insert command and inert query list gets appended for each record
            query = '{} {}'.format(insert_command_types[type], query_value)
            query_list.append(query)
            #log.info("---make_queries, length of query_list  {} ".format(len(query_list)))

            stat = True

        return query_list

    def process_data(self, source_dict, type):

        #log.info("---process_data, source and type")
        print("source_dict : " )
        #print("source_dict : " + source_dict )

        print(source_dict)
        print("type :" + type)
        results = ''
        query_list = []
        # for sdn & non-sdn type doesnt matter
        if source_dict['fetch_type'] == 'zip':
            print('zip working fine')

            stat, df = self.read_file(source_dict, source_dict[type])
            stat, df = self.process_df(df)

            if stat:
                query_list = self.make_queries(df, source_dict, type)
                return query_list
            else:
                return query_list

        if source_dict['fetch_type'] == 'xml':

            stat, df = self.get_xml_dataframe(source_dict, type)
            stat, df = self.process_df(df)
            if stat:
                query_list = self.make_queries_xml(df, source_dict, type)
                return query_list
            else:
                return query_list

    def notify_user(self, subject, message):
        """
                This function is used to send email.This will read the email settings from config file\
        :param subject: Subject for the mail\
        :param message: Email body content\
        :return:
        """
        try:
            print("Haven't implemented the email seding details")
        except Exception as e:
            print("Error occured while sending the email and error is %s" % (e))

    def main(self):

        start_time = time.clock()
        start_datetime = self.datetime_now()

        stat = self.db_hndlr()
        #stat = True
        if not stat:
            print("Error occured while connecting to the DB")
            log.critical("Error occured while connecting to the DB exiting sanctions")
            return


        for source_dict in list_dict:
            start_time_event_log = self.datetime_now()
            stat = self.fetch_data(source_dict)
            if stat:

                for type in types:

                    start_time_event_log = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    log_name = self.single_quote("Sanctions_ETL {} {}".format(source_dict['source'], type))
                    print(log_name)
                    log.info(log_name)
                    log.info(log_name + '\tref: ' + tables[type])

                    query_list = []
                    records = 0
                    log.info(" --before processing query list is: {}".format(len(query_list)))
                    try:
                        print("before going to process_data")
                        query_list = self.process_data(source_dict, type)
                        #print(query_list)
                        print("after going to process_data")
                        print(len(query_list))
                        print("db_connect")
                        print(self.db_connect)
                        print("cursor")
                        print(self.db_connect.cursor)

                        #log.info(" --after processing query list is: {}".format(len(query_list)))
                        for query in query_list:
                            log.info(" --query inserting--: {}".format(query))
                            #print(" --query inserting--: {}".format(query))

                            stat, results = self.insert_data(query)
                            if stat:
                                records += 1

                        #log.info(" --number of records inserted--: {}".format(records))
                        end_time = time.clock()
                        totaltimetaken = end_time - start_time

                    except Exception as err:

                        log.critical("Error occured while processing the data: %s" % (err))
                        end_time = time.clock()
                        totaltimetaken = end_time - start_time
                        log.info("totaltimetaken :%s" %(totaltimetaken))

            else:
                message = "Error occurred while fetching source : {} ".format(source_dict['source'])

                log.critical("fetching data had some problem for this source, {} moving on to next soure".format(source_dict['source']))
                continue



if __name__ == "__main__":
    obj = Sanctions()
    print("coming here")
    obj.main()