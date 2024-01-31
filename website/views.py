import json

from django.shortcuts import render
from django.views import View
from website.helper import renderhelper,is_ajax
from website.models import *
from django.http import HttpResponse
from django.db import IntegrityError
import pandas as pd

import requests
import boto3
from dateutil import parser
from django.db.models import Count

class index(View):
    def get(self, request):
        context = {}
        # return  HttpResponse('in')
        context['status'] = False
        return renderhelper(request, 'home', 'index',context)

    def post(self,request):



        #URLs for csv files
        customer_data_url = 'https://raw.githubusercontent.com/rinz619/mocktest/main/customer_data.csv'
        booking_data_url = 'https://raw.githubusercontent.com/rinz619/mocktest/main/booking_data.csv'
        destination_data_url = 'https://raw.githubusercontent.com/rinz619/mocktest/main/destination_data.csv'

        #Download files to localstorage
        download_csv(customer_data_url, 'customer_data.csv')
        download_csv(booking_data_url, 'booking_data.csv')
        download_csv(destination_data_url, 'destination_data.csv')

        #Reading the files
        customer_data = pd.read_csv('customer_data.csv')
        booking_data = pd.read_csv('booking_data.csv')
        destination_data = pd.read_csv('destination_data.csv')

        #Insertoion if Customer datas
        for index, row in customer_data.iterrows():
            try:
                Customers(customer_id=row['customer_id'],first_name=row['first_name'], last_name=row['last_name'], email=row['email'],phone=row['phone']).save()
            except IntegrityError as e:
                # error_message = f"Database insertion error: {str(e)}"
                print(f"CustomerID {row['customer_id']} already Exists")

        # Insertoion if Destination datas
        for index, row in destination_data.iterrows():
            try:
                Destinations(destination_id=row['destination_id'],destination_name=row['destination'], country=row['country'], popular_seasion=row['popular_season']).save()
            except IntegrityError as e:
                # error_message = f"Database insertion error: {str(e)}"
                print(f"DestinationID {row['destination_id']} already Exists")

        # Insertoion if Booking datas
        for index, row in booking_data.iterrows():
            try:
                customer = Customers.objects.get(customer_id=row['customer_id'])
                destination = Destinations.objects.get(destination_id=row['destination'])

                booking_date = identify_date_format(row['booking_date'])
                totalcost = row['number_of_passengers'] * row['cost_per_passenger']
                Bookings(book_id=row['booking_id'],customer_id=customer, destination_id=destination, booking_date=booking_date, passengers=row['number_of_passengers'], costperpassenger=row['cost_per_passenger'], totalcost=totalcost).save()
            except IntegrityError as e:
                # error_message = f"Database insertion error: {str(e)}"
                print(f"DestinationID {row['destination']} already Exists")

        #Accesing the bucket
        s3 = boto3.client('s3', aws_access_key_id='AKIA2UC3EWJOGGZFETUP', aws_secret_access_key='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')

        # Uploading to the bucket
        s3.upload_file('customer_data.csv', 'mocktest2024', 'customer_data.csv')
        s3.upload_file('booking_data.csv', 'mocktest2024', 'booking_data.csv')
        s3.upload_file('destination_data.csv', 'mocktest2024', 'destination_data.csv')
        context = {}
        context['customerdata'] = 'https://mocktest2024.s3.ap-south-1.amazonaws.com/customer_data.csv'
        context['bookingdata'] = 'https://mocktest2024.s3.ap-south-1.amazonaws.com/booking_data.csv'
        context['destinationdata'] = 'https://mocktest2024.s3.ap-south-1.amazonaws.com/destination_data.csv'
        tst =  requests.post('https://nuxrewyhx6mg5twgltwcqht7iu0kfreq.lambda-url.ap-southeast-2.on.aws/',json={'input_data': ''}).text
        context['totalbooks'] = json.loads(tst)
        context['status'] = True
        # return HttpResponse(str(type(tst)))

        return renderhelper(request, 'home', 'index',context)



#Function to download csv files
def download_csv(url, file_name):
    df = pd.read_csv(url)
    df.to_csv(file_name, index=False)

#Function to modify the date to standerd format
def identify_date_format(date_string):
    try:
        parsed_date = parser.parse(date_string)
        return parsed_date.strftime("%Y-%m-%d")
    except ValueError:
        return "Unknown format"
