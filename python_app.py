# this application will fetch crypto currency data from coingeko website
# find the top 10 to sell
# find bottom 10 to buy
# send mail to me everyday at 8:00 am

### Libraries to be used
#schedule
#smtplib
#requests
#datetime
#pandas
#time

###TASK###
#1.Download the datasets from coingecko website
#2.Send mail
#3.Schedule the application to run every day at 8:00 am

#importing libraries
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

import requests
import schedule
from datetime import datetime
import pandas as pd
import time

def send_mail(subject, body, filename):

    #setup email configuration 
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "royalsingha50@gmail.com"
    email_password ="vtqh ihbr xlsg ctvm" #app password
    receiver_email = ["royal.singha700@gmail.com", "common.user.uj@gmail.com"]

    #compose the email
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(receiver_email) #if multiple receivers
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))


    #attach csv file
    with open(filename,'rb') as file:
        part = MIMEBase('application','octet-stream')
        part.set_payload(file.read())
        encoders.encode_base64(part) #this line encodes the file base64
        part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
        message.attach(part)

    #start server
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, email_password)
            #sending mail
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email sent successful")

    except Exception as e:
        print(f"Unable to send Email {e}")
                        


#getting crypto data

def get_crypto_data():
    

    #API information
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    param = {
        'vs_currency' : 'usd',
        'order' : 'market_cap_desc',
        'per_page': 250,
        'page': 1
    }

    #send request to the website
    response= requests.get(url, params=param)

    if response.status_code == 200:
        print(f"Connection Successful ! \n Gettting the data...")

        #store the data in json format
        data = response.json()

        #creating dataframe
        df = pd.DataFrame(data)

        #selection of coloumns we need
        df = df[[
                'id','current_price','market_cap','price_change_percentage_24h',
                'high_24h', 'low_24h', 'ath','atl'
                ]]

        #Creating new coloumms

        today = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        filename_time = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")  # safe for Windows filenames
        df['Time_stamp'] = today
    
        #top 10 negative crypto currency
        top_negative_10 = df.sort_values(by='price_change_percentage_24h', ascending=True)
        top_negative_10 = top_negative_10.head(10)
        top_negative_10.to_csv(f'crypto_price_negative_top10_{filename_time}.csv', index=False)

        # top 10 positive crypto currency
        top_positive_10 = df.sort_values(by='price_change_percentage_24h', ascending=False)
        top_positive_10 = top_positive_10.head(10)
        top_positive_10.to_csv(f'crypto_price_positive_top10_{filename_time}.csv', index=False)

        
        #save the data as csv file
        file_name = f'crypto_price_{filename_time}.csv'
        df.to_csv(file_name, index=False)
        #df.to_csv(f'crypto_price_{filename_time}.csv', index=False)

        print(f"Data saved as {file_name}.csv file successfully in local directory")

        #Call email function to send the reports
        subject= f"Top 10 crypto currency data to invest for {filename_time}"
        body= f"""
        Good Morning !\n\n

        Your Crypto Reports is Here !

        Top 10 crypto with higest price increase in last 24 hour ! \n
        {top_positive_10}\n\n\n

        Top 10 crypto with the highest price decrease in last 24 hour ! \n
        {top_negative_10}

        Attached 250 plus crypto currency lattest reports\n

        Regards! \n
        Your Crypto python application
        """

        #sending mail
        send_mail(subject,body,file_name)


    else:
        print(f"Connection failed {response.status_code}")

#this get executed only if we run this script directly
if __name__ == "__main__":

    get_crypto_data()


# Schedule the task at 8:00 AM
    schedule.every().day.at('21:39').do(get_crypto_data)

    while True:
        schedule.run_pending()
        


