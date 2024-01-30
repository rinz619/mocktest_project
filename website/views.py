from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views import View
# from django.http import HttpResponse,JsonResponse
from website.helper import renderhelper,is_ajax
# from django.contrib.auth import login,logout, authenticate
# from django.shortcuts import redirect
# # from website.custom_permision import LoginRequiredMixin,AdminLoginRequiredMixin
# from django.contrib.auth.hashers import check_password
# from django.contrib import messages
from website.models import *
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.template import loader
# from django.db.models import Q
# from datetime import datetime



import csv
import json

import requests
from django.shortcuts import render
from django.http import HttpResponse


import requests
import pandas as pd
import sqlite3
from io import StringIO

from django.db import IntegrityError

import pandas as pd

import requests
# import psycopg2
# from sqlalchemy import create_engine
# import boto3
# import os
from datetime import datetime
from dateutil import parser

class index(View):
    def get(self, request):
        context = {}
        # return  HttpResponse('in')
        return renderhelper(request, 'home', 'index',context)

    def post(self,request):
        # Mock URLs for data files
        customer_data_url = 'https://raw.githubusercontent.com/rinz619/mocktest/main/customer_data.csv'
        booking_data_url = 'https://raw.githubusercontent.com/rinz619/mocktest/main/booking_data.csv'
        destination_data_url = 'https://raw.githubusercontent.com/rinz619/mocktest/main/destination_data.csv'

        # 1. Download CSV files

        download_csv(customer_data_url, 'customer_data.csv')
        download_csv(booking_data_url, 'booking_data.csv')
        download_csv(destination_data_url, 'destination_data.csv')

        # 2. Cleanse and transform data
        # Assuming date formats need conversion and adding a calculated field for total_booking_value
        customer_data = pd.read_csv('customer_data.csv')
        booking_data = pd.read_csv('booking_data.csv')
        destination_data = pd.read_csv('destination_data.csv')

        for index, row in customer_data.iterrows():
            try:
                Customers(customer_id=row['customer_id'],first_name=row['first_name'], last_name=row['last_name'], email=row['email'],phone=row['phone']).save()
            except IntegrityError as e:
                # error_message = f"Database insertion error: {str(e)}"
                print(f"CustomerID {row['customer_id']} already Exists")

        for index, row in destination_data.iterrows():
            try:
                Destinations(destination_id=row['destination_id'],destination_name=row['destination'], country=row['country'], popular_seasion=row['popular_season']).save()
            except IntegrityError as e:
                # error_message = f"Database insertion error: {str(e)}"
                print(f"DestinationID {row['destination_id']} already Exists")

        for index, row in booking_data.iterrows():
            try:
                customer = Customers.objects.get(customer_id=row['customer_id'])
                destination = Destinations.objects.get(destination_id=row['destination'])

                booking_date = identify_date_format(row['booking_date'])
                totalcost = row['number_of_passengers'] * row['cost_per_passenger']
                Bookings(book_id=row['booking_id'],customer_id=customer, destination_id=destination, booking_date=booking_date, passengers=row['number_of_passengers'], costperpassenger=row['cost_per_passenger'], totalcost=totalcost).save()
            except IntegrityError as e:
                # error_message = f"Database insertion error: {str(e)}"
                print(f"DestinationID {row['destination_id']} already Exists")

        # Convert date format
        # booking_data['booking_date'] = pd.to_datetime(booking_data['booking_date'], format='%Y-%m-%d')
        # original_date_str =  booking_data['booking_date']
        # print(original_date_str)
        # Convert to datetime object
        # original_date_obj = datetime.strptime(original_date_str, "%d-%m-%Y")

        # Format as "y-m-d"
        # formatted_date_str = original_date_obj.strftime("%Y-%m-%d")
        # print(booking_data['number_of_passengers'])
        # Handle missing or erroneous data (if any)

        # Add calculated field for total_booking_value
        # booking_data['total_booking_value'] = booking_data['number_of_passengers'] * booking_data['cost_per_passenger']
        # print(booking_data['total_booking_value'])
        return HttpResponse('in')


def download_csv(url, file_name):
    df = pd.read_csv(url)
    df.to_csv(file_name, index=False)

def identify_date_format(date_string):
    try:
        parsed_date = parser.parse(date_string)
        return parsed_date.strftime("%Y-%m-%d")
    except ValueError:
        return "Unknown format"
