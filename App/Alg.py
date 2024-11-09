import numpy as np
import pandas as pd
import secrets
import math
import requests
from pprint import pprint
import matplotlib
import matplotlib.pyplot as plt
import io
import datetime
from datetime import date , time , datetime
import os
class Algos():

    def __init__(self,portfolio) -> None:
        self.portfolio=portfolio
    
    def getExcel(self,data):
        data.to_excel("output.xlsx", index=False)

        print("output saved ")


    def displayAnalys(self,data,):
        industry=[i for i in data.industry]
        shares=[i for i in data.Shares_to_Buy]
        print(industry,shares)
        plot={}
        for i in range(len(industry)):
            if industry[i] in plot:
                plot[industry[i]]+=shares[i]
            plot[industry[i]]=shares[i]

        fig, ax = plt.subplots(figsize=(15,15))
        ax.pie(plot.values(), labels=plot.keys(),autopct='%.1f%%')
        ax.set_title('Portfolio analysis',fontsize=30)
        ax.title.set_text(f'Portfolio size = {self.portfolio}')
        # img = io.BytesIO()
        Folder_path="./static/"
        if not os.path.exists(Folder_path):
            os.makedirs(Folder_path)
        image_name="img"+str(date.today()).replace("-","")+str(datetime.now().time()).replace(":","")+".png"
        fig.savefig(Folder_path+image_name, format='png')

        return image_name
    

    def Nifty50EqualW(self,SaveExcel,Analyzer):
        data_nifty=pd.read_csv("src/Data/ind_nifty50list.csv")
        symbols=[i for i in data_nifty.Symbol]
        url = "https://latest-stock-price.p.rapidapi.com/any"

        headers = {
            "X-RapidAPI-Key": "ad8e39827emsh4ea89255472dd78p149f41jsn8c79f4d9c7ff",
            "X-RapidAPI-Host": "latest-stock-price.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers)
        data=response.json()

        Nifty50_data=[]
        for symbol in symbols:
            for i in range(len(data)):
                if symbol==data[i]['symbol']:
                    Nifty50_data.append(data[i])    
        my_columns = ['CompanyName','Ticker','industry', 'Price', 'Shares_to_Buy']
        Final_data=pd.DataFrame(columns=my_columns)


        Top_50=50
        for i in range(1,Top_50):
            Final_data=Final_data.append(
                                        pd.Series([Nifty50_data[i]['meta']['companyName'],
                                                    Nifty50_data[i]['symbol'],
                                                    Nifty50_data[i]['meta']['industry'],
                                                    Nifty50_data[i]['lastPrice'],
                                                'N/A'],
                                                index=my_columns),
                                                ignore_index=True )
        
        ## Distributing stocks on equal weights [Stratergy 1]

        ##Geting user portfolio size

        #portfolio_size=int(input("Enter Portfolio size\n"))
        position_to_be_purchased=abs(self.portfolio//len(Final_data))
        for i in range(len(Final_data.Ticker)):
            Final_data.loc[i,'Shares_to_Buy']=int(position_to_be_purchased//Final_data.loc[i,'Price'])
        
        if  Analyzer:
            img=self.displayAnalys(Final_data)
            return (Final_data,img)

    
    def MomentumTrading(self,portflio):
        return True