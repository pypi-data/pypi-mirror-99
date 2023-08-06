#import libraies which will be used throughout 

import pandas as pd
import os 
import json
import datetime
import nltk
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
from collections import defaultdict 
from tabulate import tabulate

class IndividualMesseges():
    """
    A library which allows users to you easily run some simple Data Analytics on their Facebook Messenger Data

    
    :param PATH: The Path which conatins the convsersation you want to analyze
    :type number: str

    """

    def __init__(self, PATH):
        self.directory = PATH
        self.message_file_paths =  [PATH +"\\"+ x for x in next(os.walk(PATH))[2]]


    ###############################################################################################################################
    def list_of_messages_objects(self, **kwargs ):
        """
        Creates a list and pandas DataFrame which contians all the messages and interactions present without your conversation 
        
        :param add_date: Default true, highly recommended but optional if you want to have a smaller data frame. OTHER FUNCTIONS WILL NOT WORK IF THIS IS FALSE
        :type number: bool
        
        :param as_DF: Default is True. If set to false, the method will return a dictionary rather than a pandas DataFrame 
        :type muiltiplier: bool

        :param as_DF: Default is True. If set to false, the method will not return any data to the user, it will only add it to the object 
        :type muiltiplier: bool
        """
        
        #Default Kwargs 
        defaultKwargs = { 'add_date': True, 'as_DF' : True, 'to_return' : True}
        kwargs = { **defaultKwargs, **kwargs }
        
        
        # initializing empty list for a messenger JSONs
        JSON= [] 
        
        #load all files and put their content into one list
        for i in range(len(self.message_file_paths)):
            with open(self.message_file_paths[i]) as file:
                JSON.append(json.load(file))


        # initializing empty list for message objects
        all_messages_dictionary=  []

        #loop through all the loaded json object and extract the message objects
        for i in range(len(JSON)):
            all_messages_dictionary+= JSON[i]["messages"]

        
        #add the dictionary to the object
        self.all_messages_dictionary = all_messages_dictionary

        if kwargs['add_date']:

            #date format: dd/mm/yyyy
            format_date = "%d/%m/%Y"

            #Time format:HH:MM:SS
            format_time = "%H:%M:%S"
    
            #loop through each message object and add a datetime object, the month, year, day, and time 
            for i in all_messages_dictionary:
                ts = i["timestamp_ms"]
                date_time = datetime.datetime.fromtimestamp(ts/1000.0)
                i["date"] = date_time.strftime(format_date)
                i["Time"] = date_time.strftime(format_time)
                i['year'] = date_time.year
                i['month'] = date_time.month
                i["day"]= date_time.day

        #add the pandas DF to the object
        self.all_messages_DF = pd.DataFrame.from_dict(self.all_messages_dictionary)

        if kwargs['to_return'] & kwargs['as_DF']:
            return self.all_messages_DF
        if kwargs['to_return']:
            return self.all_messages_dictionary
        
    ###############################################################################################################################
    def counter(self, total=True):
        """
        Count the number of messages sent in the conversation
        
        :param Total: Default as True which return the count of ALL messages sent, if False, it will return a dict with the count each participant sent
        :type number: bool
        """
        #checking if count has already run to save comptational requirements. If not, pass and run the count
        try:
            if total:
                return sum(self.count.values())
            else:
                return dict(self.count)
        except:
            pass

        # Use a default Dict incase there is a participant with NO messages sent but in the chat. A set helps keep track of the participants 
        self.count =  defaultdict(lambda: 0)
        self.senders = set()

        try:
            #Checking if dictionary of messages already exist, if not, need to run that method in the except 
            self.all_messages_dictionary

        except:
            self.list_of_messages_objects(to_return = False)

        # a simple counter of the number of messages and the senders     
        for messeges in self.all_messages_dictionary:
            self.senders.add(messeges['sender_name'])
            self.count[messeges['sender_name']]+=1
        
        #if statment to check if we are returning total or dictionary  
        if total:
            return sum(self.count.values())
        else:
            return dict(self.count)

    ###############################################################################################################################

    def participants(self):
        """
        Simple method to grab the participants if needed. Very similar to counter 
        """
        try:
            return self.senders
        except:
            pass

        self.senders = set()

        try:
            self.all_messages_dictionary

        except:
            self.list_of_messages_objects(to_return = False)
            
        for messeges in self.all_messages_dictionary:
            self.senders.add(messeges['sender_name'])
        
        return list(self.senders)
       
     ###############################################################################################################################

    
    def describe(self,  print_=True):
        """
        This method will provide a summary of the convseration to the user. Metric like:
        Total Messages Sent
        Messages Sent by Each Participant 
        The date when the First and Last Messages were sent
        The Difference between the First and Last Messages (In days)
        The Total Days actually spoken on 
        The Average Message Count Per Day when Messages were actively Exchanged 
        
        :param print_: Default is True, To print out a table of the measures(if true) or to return a dictionary of the metrics
        :type number: bool
        """
        #Use a Default dict to excase error messages
        self.describe = defaultdict(lambda: 0)

        #grab the total amount sent from the counter method
        self.describe["Total Messages"] = self.counter(True)

        #grad the total amount sent by each participant from the counter method
        for sender in self.counter(False):
            self.describe["Messages Sent by %s" % sender]= self.counter(False)[sender]

        #Grab dates from the pandas Data Frame
        first_message = datetime.datetime.fromtimestamp(self.all_messages_DF["timestamp_ms"].min()/1000.0)
        last_message = datetime.datetime.fromtimestamp(self.all_messages_DF["timestamp_ms"].max()/1000.0)
        total_time =last_message - first_message

        #add the dates to the dictionary 
        self.describe["First Messsage"] = str(first_message)
        self.describe["Last Messsage"] = str(last_message)
        self.describe["Difference Between First and Last"] = total_time.days

        #Use the unique function within pandas to grab the unique dates as the days conversation was conducted
        self.describe["Total Days Spoken"]= len(pd.unique(self.all_messages_DF["date"]))

        #Total messages over the days of active conversation 
        self.describe["Average Message Count Per Day"] = self.describe["Total Messages"] / self.describe["Total Days Spoken"]

        #To print a nice a table or return a dictionary of values
        if print_:
            headers = ['Metric', 'Value']
            data = [x for x in self.describe.items()]
            print(tabulate(data, headers=headers))
        else:
            return dict(self.describe)

     ###############################################################################################################################

    def first_x_messages(self, first_x_messages=10):
        """
        Returns a data frame of the first X interactions 
        
        :param first_x_messages: The number of messages to return
        :type number: int
        
        """

        #Checking if the method with the dictionary of messages has already run 
        try:
            self.all_messages_DF
        except:
            self.list_of_messages_objects(to_return = False)

        #retusna dict of the first X messages
        return self.all_messages_DF.sort_values(by=["timestamp_ms"]).head(first_x_messages)


     ###############################################################################################################################

    def sent_analyzer(self):
        '''
        VADER Sentiment Analysis. 
        VADER (Valence Aware Dictionary and sEntiment Reasoner) is a lexicon and rule-based sentiment analysis tool that is specifically attuned to 
        sentiments expressed in social media, and works well on texts from other domains.
        The VADER lexicon is an empirically validated by multiple independent human judges, VADER incorporates a "gold-standard"  sentiment lexicon that is 
        especially attuned to microblog-like contexts. 
        
        This method runs this sentiments analysis on all messages in the Pandas Data Frame
        '''

        #making sure the vader lexicon is downloaded and available 
        nltk.download("vader_lexicon")

        #Checking if the method with the dictionary of messages has already run 
        try:
            self.all_messages_DF
        except:
            self.list_of_messages_objects(to_return = False)

        #initializer the NLTK Sentiment Inentisity Analyzer
        sentiment_analyzer =  SentimentIntensityAnalyzer()
    
        #This fucntion will use the NLTK Sentiment Inentisity Analyzer and assine a score to the text it receives 
        def polarity_score_on_df(content):
            
            #check if it is a string as the NLTK Sentiment Inentisity Analyzer will not work
            if type(content)== str:
                return sentiment_analyzer.polarity_scores(content)["compound"]
            
            #if not string, return a NAN value
            else:
                return np.NAN 
            
        self.all_messages_DF["sentiment"] = self.all_messages_DF["content"].apply(polarity_score_on_df)
        
        #setting a flag as the sentiment analysis is important later in the class
        self.sentiment_done = -1
 
     ###############################################################################################################################
    def date_backbone_function(self):
        """
        This backbone dataframe will be useful for plotting as those months where no conversation was done will be set to zero and not omitted as originally
        """
        #Checking if the method with the dictionary of messages has already run 
        try:   
            ALL_MESSAGES_DF = self.all_messages_DF
        except:
            self.list_of_messages_objects(to_return = False)
            ALL_MESSAGES_DF = self.all_messages_DF

        #determing the first year, lst year and last month of conversation  
        first_year_of_convo = ALL_MESSAGES_DF['year'].min()
        last_year_of_convo = ALL_MESSAGES_DF['year'].max()
        last_month_of_convo = ALL_MESSAGES_DF[ALL_MESSAGES_DF.year == last_year_of_convo]["month"].max()
        
        #grab the unique senders
        participants = list( self.participants())
        
        #The basic structure 
        date_backbone ={"month":[], "year":[], "sender_name":[] }
        
        #for each year, created 12 months of each sender
        for i in range(first_year_of_convo, last_year_of_convo+1):
            
            for k in range( len(participants)):
                
                for j in range (1,13):
                    
                    date_backbone['month'].append(j)
                    date_backbone['year'].append(i)
                    date_backbone['sender_name'].append(participants[k])

        #Convert this dictionary to a data frame
        date_backbone = pd.DataFrame(date_backbone) 
        
        #a method to cut the back boine table at the last month of interaction  
        today_month = int(datetime.date.today().strftime("%m"))
        today_year = int(datetime.date.today().strftime("%Y"))
        
        if today_year == last_year_of_convo:
            
            index = date_backbone[(date_backbone.year==today_year) & (date_backbone.month> today_month)].index
            date_backbone.drop(index, inplace=True)
            date_backbone = date_backbone.reset_index()
            date_backbone.drop("index",axis=1, inplace=True)
            
        else:
            
            index = date_backbone[(date_backbone.year==last_year_of_convo) & (date_backbone.month> last_month_of_convo)].index
            date_backbone.drop(index, inplace=True)
            date_backbone = date_backbone.reset_index()
            date_backbone.drop("index",axis=1, inplace=True)

         #Set the date backbone to be part of the object   
        self.date_backbone= date_backbone
    ###############################################################################################################################

    def aggreagte_by_month_year(self, to_return=False):
        """
        This method will aggregate results by the month (count and sentiments) to provide visuals for historic conversation data without being too volitile. 
        A Day Aggregator is in the works
    
        
        :param to_return: Default is False. Change to True to return the dataframe
        :type number: bool
        """
        
        #Checking if the sentiment was done
        try:
            self.sentiment_done
        except:
            self.sent_analyzer()

        #Checking if the datebackbone was created
        try:   
            date_backbone = self.date_backbone
            
        except:
            self.date_backbone_function()
            date_backbone = self.date_backbone

        #checking if the aggregation was done to save commutational requirements
        try:
            if to_return==True:
                return self.Final_year_month
            else:
                self.Final_year_month
        except:
        #All messages Data frame
            ALL_MESSAGES_DF = self.all_messages_DF
        
        #Group the data by month, year and sender name to be a bit less volatile 
            year_month= ALL_MESSAGES_DF.groupby(["month", 'year',"sender_name"])["sentiment"].describe().reset_index()

        #merge the aggregated DataFrame with the Back bone to fill in the holes with zero messages
            Final_year_month = date_backbone.merge(year_month, right_on= ["month", "year", "sender_name"], left_on= ["month", "year", "sender_name"], how ="left" )
            Final_year_month = Final_year_month.replace(np.nan,0)

        #Change the date object to a year/month object for graphing  
            Final_year_month['date'] = pd.to_datetime(Final_year_month['year'].astype("str") + Final_year_month['month'].astype("str"),format='%Y%m')

        #Sort the data my date
            Final_year_month= Final_year_month.sort_values(by ="date", ignore_index=True)

        #set the results to the object and then return if requested 
            self.Final_year_month = Final_year_month
            if to_return==True:
                return self.Final_year_month
     ###############################################################################################################################
    
    def plot_sentiments(self, toReturn = False):
        """
        This method will provide a plot of the aggregated sentiment data discussed in the aggreagte_by_month_year method
        
        :param to_return: Default is False. If True will return the user setiments per months, per user
        :type number: bool
        """
        #Checking if the method with the dictionary of messages has already run 
        try:
            Final_year_month = self.Final_year_month
        except:
            self.aggreagte_by_month_year()
            Final_year_month= self.Final_year_month
            

        #Unique members   
        members = list(self.participants())

        #Extract the date for each user to provide seperate lines rather than one summation line
        member_setiments= {}

        for i in range(len(members)):
            member_data= Final_year_month[Final_year_month.sender_name == members[i]]
            member_setiments[members[i]]= [
                pd.to_datetime(member_data['year'].astype("str") + member_data['month'].astype("str"),format='%Y%m'),
                member_data['mean'] ]
            
        #If the user wnats the date returned and not the plot
        if toReturn== True:
            return member_setiments
        else:
            pass
    
        #Plot the data            
        plt.clf()
        plt.figure(figsize=(20,10))
            
        for member in members:
                
             plt.plot(member_setiments[member][0], member_setiments[member][1], label = member)
                
        plt.legend()

        plt.show()

     ###############################################################################################################################
    def plot_counts(self, toReturn = False):
        """
        This method will provide a plot of the aggregated message count data discussed in the aggreagte_by_month_year method
        
        :param to_return: Default is False. If True will return the user setiments per months, per user
        :type number: bool
        """
        #Checking if the method with the dictionary of messages has already run 
        try:
            Final_year_month = self.Final_year_month
        except:
            self.aggreagte_by_month_year()
            Final_year_month= self.Final_year_month
            

        #Unique members   
        members = list(self.participants())

        #Extract the date for each user to provide seperate lines rather than one summation line
        member_setiments= {}

        for i in range(len(members)):
            member_data= Final_year_month[Final_year_month.sender_name == members[i]]
            member_setiments[members[i]]= [
                pd.to_datetime(member_data['year'].astype("str") + member_data['month'].astype("str"),format='%Y%m'),
                member_data['count'] ]

        #If the user wnats the date returned and not the plot    
        if toReturn== True:
            return member_setiments
        else:
            pass
    
        #Plot the data               
        plt.clf()
        plt.figure(figsize=(20,10))
            
        for member in members:
                
             plt.plot(member_setiments[member][0], member_setiments[member][1], label = member)
                
        plt.legend()
        plt.show()
    