import praw
from tabulate import tabulate
from datetime import datetime
from twilio.rest import Client


user_agent = "Searchbot_01"
reddit = praw.Reddit(username="Searchbot_01",
                     password ="aaaa1111",
                     client_id="Ai32qfXNqvGuMEvHFFMlAw",
                     client_secret="IG5XKjyUGkcG2cgXfBSwVvalMTxFRg",
                     user_agent=user_agent,
                     check_for_async=False)

subreddit = reddit.subreddit('watchexchange')
posts = subreddit.new(limit=10)

search_terms = ['omega', 'sinn','rolex']  # List of search terms
brands  = ['A. Lange & Sohne', 'Alpina', 'Armani Exchange', 'Audemars Piguet', 
                'Ball', 'Baume et Mercier', 'Bell & Ross', 'Blancpain', 'Breguet', 'Breitling', 
                'Bremont', 'Bulova', 'Bvlgari', 'Cartier', 'Certina', 'Chanel', 'Chopard', 'Citizen', 
                'Corum', 'Daniel Wellington', 'De Bethune', 'Doxa', 'Ebel', 'Eberhard & Co.', 
                'F.P. Journe', 'Fossil', 'Frederique Constant', 'Girard-Perregaux', 'Glashütte Original', 
                'G-Shock', 'Hamilton', 'Harry Winston', 'Hermes', 'Hublot', 'IWC', 'Jaeger-LeCoultre', 'Junghans', 
                'Laco', 'Longines', 'Maurice Lacroix', 'MeisterSinger', 'Montblanc', 'Movado', 'Nomos Glashütte', 'Omega', 
                'Oris', 'Panerai', 'Parmigiani Fleurier', 'Patek Philippe', 'Piaget', 'Rado', 'Raymond Weil', 'Richard Mille', 
                'Rolex', 'Seiko', 'Shinola', 'Sinn', 'Tag Heuer', 'Tissot', 'Tudor', 'Ulysse Nardin', 'Vacheron Constantin', 
                'Victorinox Swiss Army', 'Zenith']

table = []
for post in posts:
    post_name = post.title.lower()  # Convert post name to lowercase
    brand = ''
    for b in brands:
        if b.lower() in post_name:
            brand = b
            break
    # Check if any of the search terms are in the lowercase post name
    if any(term in post_name for term in search_terms):
        # Extract price from post name (assuming price follows after "$" and may include "K", "k", or ".")
        price_str = post_name.split("$")[-1].split()[0]
        try:
            price = float(price_str.replace("k", "000").replace("K", "000").replace(".", ""))
        except ValueError:
            price = ''
        post_time = datetime.utcfromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S')
        table.append([post_name, post_time, post.url, brand, price])

headers = ['Post Name', 'Post Time', 'Post Link', 'Brand', 'Price']

table_str = tabulate(table, headers=headers)  # Convert table to string

# Twilio account information
account_sid = 'ACd2079bd46f13974225b28ef06255af01'
auth_token = '8dc2962417449a63b380cd0fbaec99f0'
client = Client(account_sid, auth_token)

# Send message with table of results using Twilio

phone_numbers = ['14239338894'] #['14232272113','14232814382']
from_numbers = ['18334633894']
for row in table:
    if any(b in row for b in brands):
        #message_body = f"Brand: {row[3]}"
        message_body = f"Brand: {row[3]}\nLink: {row[2]}\nPost Time: {row[1]}"

        message = client.messages.create(
            to='14232814382',
            from_='18334633894',
            body= message_body
        )
        print(f"Message sent with ID: {message.sid}")

print(f"Table:\n{table_str}")
