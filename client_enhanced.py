# This file contains test code for the API created in the file api_server.py
print("Please be patient, it might take some time until the server responses.\nUsually it does not take more than a couple of seconds.")


### ###

# import libraries
import requests


# 3.1 Retrieve the whole DataFrame in json format
# retrieve all characters from the API

url = 'http://localhost:5000/characters'

response = requests.get(url)

if response.status_code == 200:
    character_data = response.json()['response']
    print("\n\nResult for step 3.1. - The whole dataframe is retrieved in JSON format:")
    print(character_data)
else:
    print("\n\nResult for step 3.1. - The whole dataframe is retrieved in JSON format:")
    print(f"Error: {response.status_code} - {response.json()['response']}")


# 3.2 Retrieve information for a single entry or for a list of entries identified
# retrieve singular character from the API using character id

url = 'http://localhost:5000/characters'
char_id = 1009146

params = {'char_ids': char_id}

response = requests.get(url, params=params)

if response.status_code == 200:
    character_data = response.json()['response']
    print("\n\nResult for step 3.2.1. - Information for one character is retrieved based on his/her ID:")
    print(character_data)
else:
    print("\n\nResult for step 3.2.1. - Information for one character is retrieved based on his/her ID:")
    print(f"Error: {response.status_code} - {response.json()['response']}")


# get singular character from the API using character name

url = 'http://localhost:5000/characters'
char_id = 1009146

params = {'char_names': 'Ajak'}

response = requests.get(url, params=params)
if response.status_code == 200:
    character_data = response.json()['response']
    print("\n\nResult for step 3.2.2. - Information for one character is retrieved based on his/her name:")
    print(character_data)
else:
    print("\n\nResult for step 3.2.2. - Information for one character is retrieved based on his/her name:")
    print(f"Error: {response.status_code} - {response.json()['response']}")


# get multiple characters from AI using list of character ids

url = 'http://localhost:5000/characters'
char_id = [1009146, 1009148]

params = {'char_ids': ','.join(map(str, char_id))}
                              
response = requests.get(url, params=params)
if response.status_code == 200:
    print("\n\nResult for step 3.2.3. - Information for multiple characters is retrieved, using multiple character IDs in a list as input:")
    character_data = response.json()['response']
    print(character_data)
else:
    print("\n\nResult for step 3.2.3. - Information for multiple characters is retrieved, using multiple character IDs in a list as input:")
    print(f"Error: {response.status_code} - {response.json()['response']}")


# get mulitple characters from API using list of character names

url = 'http://localhost:5000/characters'
char_name = ['Ajak', 'Absorbing Man']

params = {'char_names': ','.join(map(str, char_name))}

response = requests.get(url, params=params)
if response.status_code == 200:
    character_data = response.json()['response']
    print("\n\nResult for step 3.2.4. - Information for multiple characters is retrieved, using multiple character names in a list as input:")
    print(character_data)
else:
    print("\n\nResult for step 3.2.4. - Information for multiple characters is retrieved, using multiple character names in a list as input:")
    print(f"Error: {response.status_code} - {response.json()['response']}")


# 3.3 Add a new character to the existing DataFrame by specifying its characteristics
# (Character Name, Character ID, Available Events, Available Series, Available Comics,
# and Price of Comic). The API should restrict addition of characters with pre-existing
# Character IDs.

# Add new character 'Thor' to the API

url = 'http://localhost:5000/characters'
data = {
    'Character Name': 'Thor',
    'Character ID': 1234567,
    'Total Available Events': 10,
    'Total Available Series': 5,
    'Total Availabe Comics': 20,
    'Price of the Most Expensive Comic': 9.99
}
response = requests.post(url, json=data)

print("\n\nResult for step 3.3.1. - A new character (Thor) is added to the database including all relevant information about this character:")
print(response.status_code)
print(response.json())


# If run again, should get a 400 error code because Character ID already exists in the database which is based on the csv
# created in part 1. of Assignment 1

url = 'http://localhost:5000/characters'
data = {
    'Character Name': 'Thor',
    'Character ID': 1234567,
    'Total Available Events': 10,
    'Total Available Series': 5,
    'Total Availabe Comics': 20,
    'Price of the Most Expensive Comic': 9.99
}
response = requests.post(url, json=data)

print("\n\nResult for step 3.3.2. - The code tries to add Thor a second time to the database. This should return an error because each ID should be unique in the database.:")
print(response.status_code)
print(response.json())


# 3.4 Add a new character to the existing DataFrame by specifying only the Character ID
# Add character only with Character ID. We connect to the Marvel API to fill in the remaining information apart from the ID.

url = 'http://localhost:5000/characters'
data = {  
    'Character ID': 1009351,
}
response = requests.post(url, json=data)

print("""\n\nResult for step 3.4.1. - A new character is added to the database. Only the ID is provided with the related post-request.\n The remaining infomration is retrieved conncecting to the Marvel API and asking for the needed information:""")
print(response.status_code)
print(response.json())


# Does not work if ID does not exits in Marvel API

url = 'http://localhost:5000/characters'
data = {  
    'Character ID': 10102021914819,
}
response = requests.post(url, json=data)

print("""\n\nResult for step 3.4.2. - Trying to add a new character to the database only specifying the ID,\n should trigger an error if the ID cannot be found in the original Marvel character database communicating with the Marvel API (see below):""")
print(response.status_code)
print(response.json())


# 3.5 Delete a character or a list of characters by providing either the Character ID
# or the Character Name. The API should return an error if the character you are trying
# to delete does not exist in the DataFrame.


# delete single character (Thor) by name

url = 'http://localhost:5000/characters'
headers = {'Content-Type': 'application/json'}
data = {'char_names': 'Thor'}
response = requests.delete(url, headers=headers, json=data)

print("\n\nResult for step 3.5.1. - We try to delete the character Thor from the database using his name, after he has already been added before:")
print(response.status_code)
print(response.json())


# add character 'Odin' to test delete by ID

url = 'http://localhost:5000/characters'
data = {
    'Character Name': 'Odin',
    'Character ID': 7654321,
    'Total Available Events': 10,
    'Total Available Series': 5,
    'Total Availabe Comics': 20,
    'Price of the Most Expensive Comic': 9.99
}
response = requests.post(url, json=data)

print("\n\nResult for step 3.5.2.1. - We first add the character Odin to the database \n in order to delte it again in the second step relying on the ID:")
print(response.status_code)
print(response.json())

# delete single character by id

url = 'http://localhost:5000/characters'
headers = {'Content-Type': 'application/json'}
data = {'char_ids': 7654321}
response = requests.delete(url, headers=headers, json=data)

print("\n\nResult for step 3.5.2.2. - We delete a single character (Odin) from the database according to his ID:")
print(response.status_code)
print(response.json())


# delete multiple characters by id
# first we add Odin and Thor once agian to delete both of them at once relying on their IDs
# this is shown just below

# add character 'Thor' to test delete

url = 'http://localhost:5000/characters'
data = {
    'Character Name': 'Thor',
    'Character ID': 1234567,
    'Total Available Events': 10,
    'Total Available Series': 5,
    'Total Availabe Comics': 20,
    'Price of the Most Expensive Comic': 9.99
}
response = requests.post(url, json=data)

print("\n\nResult for step 3.5.3.1. - We add the character Thor again to the database. Thor will be delete once more in subsequent steps:")
print(response.status_code)
print(response.json())


# add character 'Odin' to test delete

url = 'http://localhost:5000/characters'
data = {
    'Character Name': 'Odin',
    'Character ID': 7654321,
    'Total Available Events': 10,
    'Total Available Series': 5,
    'Total Availabe Comics': 20,
    'Price of the Most Expensive Comic': 9.99
}
response = requests.post(url, json=data)

print("\n\nResult for step 3.5.3.2. - We add the character Odin again to the database. Odin will be delete once more in subsequent steps:")
print(response.status_code)
print(response.json())

url = 'http://localhost:5000/characters'
headers = {'Content-Type': 'application/json'}
data = {'char_ids': [1234567, 7654321]}
response = requests.delete(url, headers=headers, json=data)

print("\n\nResult for step 3.5.3.3. - We delete multiple characters (Thor and Odin) together in one step from the database according to their IDs.\n IDs are provided within a list:")
print(response.status_code)
print(response.json())


# delete multiple characters by name
# first we add Odin and Thor once agian to delete both of them at once relying on their names below

# add character 'Thor' to test delete

url = 'http://localhost:5000/characters'
data = {
    'Character Name': 'Thor',
    'Character ID': 1234567,
    'Total Available Events': 10,
    'Total Available Series': 5,
    'Total Availabe Comics': 20,
    'Price of the Most Expensive Comic': 9.99
}
response = requests.post(url, json=data)


# add character 'Odin' to test delete

url = 'http://localhost:5000/characters'
data = {
    'Character Name': 'Odin',
    'Character ID': 7654321,
    'Total Available Events': 10,
    'Total Available Series': 5,
    'Total Availabe Comics': 20,
    'Price of the Most Expensive Comic': 9.99
}
response = requests.post(url, json=data)

print("\n\nResult for step 3.5.4.1 - We add Thor and Odin once more to the database.\n In the next step, both shall be deleted from the database based on their names:")
print(response.status_code)
print(response.json())

url = 'http://localhost:5000/characters'
headers = {'Content-Type': 'application/json'}
data = {'char_names': ['Thor', 'Odin']}
response = requests.delete(url, headers=headers, json=data)

print("\n\nResult for step 3.5.4.2 - We delete multiple characters (Odin & Thor) from the database according to their names.\n Names are provided in a list:")
print(response.status_code)
print(response.json())


# 4. Protect both the addition and the deletion of characters using an OAuth
# authentication scheme whereby users can sign up and then log in to obtain an access token
# with limited scope and a duration of 1 hour.

### ////////////////////////////////////////////////////////// ###


### getting exchange rates to exact time of request would require a paid API ###
### making use of a free sign up free exchange rate api ###
### however, api only returns exchange rates on a daily basis and does not provide historic data ###
### so only able to get exchange rates for the current day ###

url = 'http://localhost:5000/characters'  

# define the request payload
payload = {
    'char_names': ['Aaron Stack', 'Ajak'],
    'new_price': [10999.99, 9999.99],
    'currency': ['USD', 'EUR']
}

response = requests.put(url, json=payload)
print("\n\nResult for the test of step 4. of Part 2. of Assignment 1.:")
print(response.status_code)
print(response.json())
