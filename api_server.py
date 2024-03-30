# This file contains the API server code, creating a local server. Test code (the client) can be found in the client_enhanced.py file.

### ###


# all code related to task 4 (Sign Up, Login, Authentication) are commented out because the authentication does not work
# let's move to the correct directory first

import os

# set the working directory. Please change the path below to the matching path on your system
#os.chir(r"C:\Users\janic\OneDrive\Desktop\_ESADE_Master\_1._Semester_ESADE\_Cloud_Computing_\First_Assignment\Abgabe\Submission_Team_6_Cloud_Computing_Assignment_1_Part_1_and_2_")
#os.chdir(r'C:\Users\brian\OneDrive\Desktop\test_run')
os.chdir(r'your path here')


# import libraries

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import pandas as pd
import datetime
import requests

# import jwt #import from PyJWT
# from functools import wraps

import hashlib


# set up the API

app = Flask(__name__)
api = Api(app)


# class SignUp(Resource):

#     def post(self):
#         global users_data  # Declare the variable as global
#         parser = reqparse.RequestParser()
#         parser.add_argument('email', type=str, help='Email is required', required=True)
#         parser.add_argument('password', type=str, help='Password is required', required=True)
#         args = parser.parse_args()

#         # Read existing user data from the CSV file
#         users_data = pd.read_csv('users.csv')

#         # Check if the provided email already exists in the database
#         if args['email'] in users_data['email'].values:
#             return {'status': 400, 'response': 'Email already exists'}, 400

#         # Create a new DataFrame with the new user data
#         new_user_data = pd.DataFrame({'email': [args['email']], 'password': [args['password']]})

#         # Append the new user data to the existing DataFrame
#         users_data = pd.concat([users_data, new_user_data], ignore_index=True)

#         # Save the modified DataFrame to the CSV file
#         users_data.to_csv('users.csv', index=False)
        
#         return {'status': 200, 'response': 'Successfully signed up'}, 200

# class LogIn(Resource):

#     def get(self):

#         # Read existing user data from the CSV file
#         users_data = pd.read_csv('users.csv')
#         users_data['password'] = users_data['password'].astype(str)

#         parser = reqparse.RequestParser()
#         parser.add_argument('email', type=str, help='Email is required', required=True)
#         parser.add_argument('password', type=str, help='Password is required', required=True)
#         args = parser.parse_args()

#         # Check if the provided email exists in the database
#         user_entry = users_data[users_data['email'] == args['email']]
#         if user_entry.empty:
#             return {'status': 401, 'response': 'Unauthorized - Invalid email'}, 401

#         # Extract the stored password from the user_entry (a DataFrame) and compare
#         stored_password = user_entry['password'].iloc[0]
#         if stored_password != args['password']:
#             return {'status': 401, 'response': 'Unauthorized - Invalid password'}, 401

#         # Create an access token with the user's index as the identifier and expires in 1 day
#         user_index = user_entry.index[0]
#         expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
#         # Generate a JWT token using jwt.encode() method from PyJWT
#         access_token = jwt.encode({'user_id': int(user_index), 'exp': expiration_time}, 'your_secret_key', algorithm='HS256')
        
#         return {'status': 200, 'response': 'Successfully signed up', 'access_token': access_token}, 200
#         # return jsonify(response_data), 200


### everything broke when I tried to protect addition and deletion...

# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None

#         if 'access_token' in request.headers:
#             token = request.headers['access_token']

#         if not token:
#             return {'status': 401, 'response': 'Unauthorized - Access token is missing'}, 401

#         try:
#             data = jwt.decode(token, 'your_secret_key', algorithms=['HS256'])
#             current_user = data['user_id']
#             expiration_time = data['exp']
#             if expiration_time < datetime.datetime.utcnow():
#                 return {'status': 401, 'response': 'Unauthorized - Access token has expired'}, 401
#         except:
#             return {'status': 401, 'response': 'Unauthorized - Invalid access token'}, 401

#         return f(current_user, *args, **kwargs)

#     return decorated

class Characters(Resource):
    # get request to retrieve information
    def get(self):
        # user can specify either the Character IDs or the Character Names
        # if none specified, return the whole DataFrame in json format
        char_id = request.args.get('char_ids')
        char_name = request.args.get('char_names')
        data = pd.read_csv('data.csv')
        if char_id:
            char_id = list(map(int, char_id.split(',')))
            data = data[data['Character ID'].isin(char_id)]
        elif char_name:
            char_name = list(map(str, char_name.split(',')))
            data = data[data['Character Name'].isin(char_name)]            
        data = data.to_dict(orient='records')
        return {'status': 200, 'response': data}, 200
    
    # @token_required
    # def post(self, current_user, access_token):
    # post request to add new characters
    def post(self):
        # Gain access to the Marvel developer API for requests
        public_key = "421c79c0182d2f8abc174eb29a2cdbd1"
        private_key = "ebdd8f2d94cf65d84dd011b33243a3b3d01df02c"

        base_url = "https://gateway.marvel.com/v1/public/"

        params = {
            "apikey": public_key,
            "ts": "1",
            "hash": hashlib.md5(f"1{private_key}{public_key}".encode('utf-8')).hexdigest(),
            "limit": 100                                                                        # 100 is max limit
                                                                                                # let's hope no request ever exceeds 100
        }

        # request information on new character. Only Character ID is required. 
        # The rest of the information can be extracted from the Marvel API
        parser = reqparse.RequestParser()
        parser.add_argument('Character Name', type=str, help='Missing argument Character Name', required=False)
        parser.add_argument('Character ID', type=int, help='Missing argument Character ID', required=True)
        parser.add_argument('Total Available Events', type=int, help='Missing argument Total Available Events', required=False)
        parser.add_argument('Total Available Series', type=int, help='Missing argument Total Available Series', required=False)
        parser.add_argument('Total Availabe Comics', type=int, help='Missing argument Total Availabe Comics', required=False)
        parser.add_argument('Price of the Most Expensive Comic', type=float, help='Missing argument Price of the Most Expensive Comic', required=False)
        args = parser.parse_args()  # parse arguments to dictionary
    
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv('data.csv')

        # Convert the 'Character ID' column to integers
        df['Character ID'] = df['Character ID'].astype(int)

        # Convert the DataFrame to a list of dictionaries
        data = df.to_dict(orient='records')

        # Check if the provided Character ID already exists in the dataset
        char_id_list = [d['Character ID'] for d in data]
        if args['Character ID'] in char_id_list:
            return {'status': 400, 'response': 'ID already exists'}, 400
    
        # Check if the provided Character ID exists in the Marvel API
        # If Character IDs, retrieve the missing data
        if requests.get(base_url + "characters/" + str(args['Character ID']), params=params).json()['code'] == 404 and args['Character Name'] == None and args['Total Available Events'] == None and args['Total Available Series'] == None and args['Total Availabe Comics'] == None and args['Price of the Most Expensive Comic'] == None:
            return {'status': 400, 'response': 'ID does not exist in Marvel Database'}, 400
        else:
            # If the Character ID exists, extract the remaining information from the Marvel API
            if args['Character Name'] == None:
                args['Character Name'] = requests.get(base_url + "characters/" + str(args['Character ID']), params=params).json()['data']['results'][0]['name']

            if args['Total Available Events'] == None:
                args['Total Available Events'] = requests.get(base_url + "characters/" + str(args['Character ID']) + "/events", params=params).json()['data']['total']

            if args['Total Available Series'] == None:
                args['Total Available Series'] = requests.get(base_url + "characters/" + str(args['Character ID']) + "/series", params=params).json()['data']['total']

            if args['Total Availabe Comics'] == None:
                args['Total Availabe Comics'] = requests.get(base_url + "characters/" + str(args['Character ID']) + "/comics", params=params).json()['data']['total']

            if args['Price of the Most Expensive Comic'] == None:
                comics = requests.get(base_url + "characters/" + str(args['Character ID']) + "/comics", params=params).json()['data']['results']
                prices = []
                for comic in comics:
                    prices += comic['prices']
                if len(prices) > 0:
                    max_price = max([float(price['price']) for price in prices])
                else:
                    max_price = None
                args['Price of the Most Expensive Comic'] = max_price

        # Add the new entry to the DataFrame
        new_entry = {
            'Character Name': args['Character Name'],
            'Character ID': args['Character ID'],
            'Total Available Events': args['Total Available Events'],
            'Total Available Series': args['Total Available Series'],
            'Total Availabe Comics': args['Total Availabe Comics'],
            'Price of the Most Expensive Comic': args['Price of the Most Expensive Comic']
        }
        df.loc[len(data)] = new_entry
    
        # Save the modified DataFrame to the CSV file
        df.to_csv('data.csv', index=False)
    
        return {'status': 201, 'response': new_entry}, 201
    
    # @token_required
    # def delete(self, current_user, access_token):
    # delete request to delete characters
    def delete(self):
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv('data.csv')
        # Convert the 'Character ID' column to integers
        df['Character ID'] = df['Character ID'].astype(int)
        # Convert the DataFrame to a list of dictionaries
        data = df.to_dict(orient='records')
        
        # Create a list of Character IDs and Character Names for easy lookup
        char_id_list = [d['Character ID'] for d in data]
        char_name_list = [d['Character Name'] for d in data]

        # delete a character or a list of characters by providing either the Character ID or the Character Name
        parser = reqparse.RequestParser()
        parser.add_argument('char_names', type=str, action='append')
        parser.add_argument('char_ids', type=int, action='append')
        args = parser.parse_args()

        if args['char_ids'] is not None:
            # delete characters by IDs
            not_found_ids = []
            for char_id in args['char_ids']:
                if char_id in char_id_list:
                    df = df[df['Character ID'] != char_id]
                else:
                    not_found_ids.append(char_id)
            # Save the modified DataFrame to the CSV file
            df.to_csv('data.csv', index=False)
            if not_found_ids:
                return {'message': 'Characters with IDs {} not found'.format(not_found_ids)}, 404
            else:
                return {'message': 'Characters with IDs {} deleted successfully'.format(args['char_ids'])}, 200
        elif args['char_names'] is not None:
            # delete characters by names
            not_found_names = []
            for char_name in args['char_names']:
                if char_name in char_name_list:
                    df = df[df['Character Name'] != char_name]
                else:
                    not_found_names.append(char_name)
            # Save the modified DataFrame to the CSV file
            df.to_csv('data.csv', index=False)
            if not_found_names:
                return {'message': 'Characters with names {} not found'.format(not_found_names)}, 404
            else:
                return {'message': 'Characters with names {} deleted successfully'.format(args['char_names'])}, 200
        else:
            return {'message': 'Please provide either the Character ID or the Character Name to delete'}, 400
        

    # Write the code to enable users to modify the Price of the Most Expensive Comic by providing 
    # either the Character ID or the Character Name. The API should accept new prices in different 
    # currencies, including USD, EUR, GBP and CAD and transform them to the right values 
    # to the exchange rate of the considered date and time (+/- an hour).

    ### getting exchange rates to exact time of request would require a paid API ###
    ### making use of a free sign up free exchange rate api ###
    ### however, api only returns exchange rates on a daily basis and does not provide historic data ###
    ### so only able to get exchange rates for the current day ###

    # put request to modify the price of the most expensive comic
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('char_names', type=str, action='append')
        parser.add_argument('char_ids', type=int, action='append')
        parser.add_argument('new_price', type=float, action = 'append', required=True)
        parser.add_argument('currency', type=str, action = 'append', required=True)
        args = parser.parse_args()

        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv('data.csv')
                
        # Convert the 'Character ID' column to integers
        df['Character ID'] = df['Character ID'].astype(int)
        # Convert the DataFrame to a list of dictionaries
        data = df.to_dict(orient='records')
        
        # Create a list of Character IDs and Character Names for easy lookup
        char_id_list = [d['Character ID'] for d in data]
        char_name_list = [d['Character Name'] for d in data]

        # get current exchange rate info
        # couldn't find a good api without signing up for an account
        # this api is free, does not require signup, however, exchange rates are only updated once a day
        # also the api, at least without an account, does not support historic requests,
        # so i can only get the exchange rates for the day of the request...

        ex_rates = requests.get('https://open.er-api.com/v6/latest/USD').json()['rates']

        # check if character id or name is provided
        if args['char_ids']:
            char_ids = args['char_ids']
            char_names = [char_name_list[char_id_list.index(char_id)] for char_id in char_ids]
        elif args['char_names']:
            char_names = args['char_names']
            char_ids = [char_id_list[char_name_list.index(char_name)] for char_name in char_names]
        else:
            return {'status': 400, 'response': 'Bad Request - Character ID or Name is missing'}, 400

        # check if all characters exist
        for char_name in char_names:
            if char_name not in char_name_list:
                return {'status': 404, 'response': 'Not Found - Character does not exist'}, 404

        # convert new prices to USD
        new_prices = args['new_price']
        currencies = args['currency']
        for i in range(len(new_prices)):
            if currencies[i] != 'USD':
                new_prices[i] = new_prices[i] / ex_rates[currencies[i]]

        # update the most expensive comic prices
        for i in range(len(char_ids)):
            if args['char_ids']:
                df.loc[df['Character ID'] == char_ids[i], 'Price of the Most Expensive Comic'] = new_prices[i]
            elif args['char_names']:
                df.loc[df['Character Name'] == char_names[i], 'Price of the Most Expensive Comic'] = new_prices[i]

        # save the updated DataFrame to the CSV file
        df.to_csv('data.csv', index=False)

        return {'status': 200, 'response': 'Successfully updated the prices of the most expensive comics'}, 200
    

# api.add_resource(LogIn, '/login')
# api.add_resource(SignUp, '/signup')
api.add_resource(Characters, '/characters', endpoint='characters')

if __name__ == '__main__':
    app.run()
    