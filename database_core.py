import weaviate
import os
import weaviate
import pandas as pd
import requests
from datetime import datetime, timezone
import json
from weaviate.util import generate_uuid5
from tqdm import tqdm
import os
import weaviate.classes.query as wq

import json
import pandas as pd 
import requests
import weaviate
import os
import weaviate.classes.config as wc
import streamlit as st 


openai_api = st.secrets["openai_api"]
headers = {
    "X-OpenAI-Api-Key": openai_api
}  # Replace with your OpenAI API key

def init_weaviate_client():
    
    client = weaviate.connect_to_local(headers=headers)
    return client

client = init_weaviate_client()

def create_login_collection(client):
    client.collections.create(
        name="LoginBeta",
        properties= [
            wc.Property(name="email", data_type=wc.DataType.TEXT),
            wc.Property(name="password", data_type=wc.DataType.TEXT),
        ],
        vectorizer_config=wc.Configure.Vectorizer.text2vec_openai()
    )
    print("Login Collection Created ... ")

def create_users_collection(client):
    client.collections.create (
    name = "UsersBeta",
    properties=[
        wc.Property(name="name", data_type=wc.DataType.TEXT),
        wc.Property(name="email", data_type=wc.DataType.TEXT),
        wc.Property(name="financial_goal", data_type=wc.DataType.TEXT),
        wc.Property(name="health_goal",data_type=wc.DataType.TEXT),
        wc.Property(name="notification_status",data_type=wc.DataType.INT),
        wc.Property(name="user_id", data_type=wc.DataType.INT),
    ],
    vectorizer_config=wc.Configure.Vectorizer.text2vec_openai()
    
    )
    print("Users Collection Created ... ") 




def semantic_search(client,user_input):
    users = client.collections.get("UsersBeta")
    response = users.query.near_text(query=user_input , limit =5, return_metadata=wq.MetadataQuery(distance=True))
    # Inspect the response
    for o in response.objects:
        print(
            o.properties["title"], o.properties["release_date"].year
        )  # Print the title and release year (note the release date is a datetime object)
        print(
            f"Distance to query: {o.metadata.distance:.3f}\n"
        )  # Print the distance of the object from the query
        
    client.close()  # Close the connection & release resources        
        
        
def read_all_objects():
    client = init_weaviate_client()
    collection = client.collections.get("UsersBeta")

    for item in collection.iterator():
        print(item.uuid, item.properties)
        
    client.close()

def add_to_users_collection(client,name,email,financial_goal,health_goal,notification_status,user_id):
    # Get the collection
    users = client.collections.get("UsersBeta")    
    
    # Build the movie object
    user_obj = {
        "name": name,
        "email": email,
        "financial_goal": financial_goal,
        "health_goal":health_goal,
        "notification_status": notification_status,
        "user_id":user_id,
        
    }
    # Use context manager for adding the object
    with users.batch.rate_limit(2400) as batch:
        batch.add_object(
            properties=user_obj,
            uuid=generate_uuid5(user_id)
        )
        # The batcher automatically sends batches

    # Check for failed objects
    if len(users.batch.failed_objects) > 0:
        print(f"Failed to import {len(users.batch.failed_objects)} objects")
    else:
        print("The user object has been successfully added.") 
            
    
    client.close()  # Close the connection & release resources        
    



# Instantiate your client (not shown). e.g.:
# client = weaviate.connect_to_wcs(...) or
# client = weaviate.connect_to_local(...)
def generate_unique_user_id(name,email):
    pass





try:
    # Work with the client here - e.g.:
    assert client.is_live()
    #while client:
    #    assert client.is_live()  # This will raise an exception if the client is not live
    #metainfo = client.get_meta()
    #print(json.dumps(metainfo, indent=2))  # Print the meta information in a readable format
    
    
    
    
    # Run Once to create Users Collections
    #create_users_collection(client)
    #create_login_collection(client=client)
    read_all_objects()
    
    
finally:  # This will always be executed, even if an exception is raised
    client.close()  # Close the connection & release resources





#movies = client.collections.get("Movie")
# Enter context manager
#    with movies.batch.rate_limit(2400) as batch:
        # Loop through the data
#        for i, movie in tqdm(df.iterrows()):
            # Convert data types
            # Convert a JSON date to `datetime` and add time zone information
#            release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d").replace(
#                tzinfo=timezone.utc
#            )
            # Convert a JSON array to a list of integers
#            genre_ids = json.loads(movie["genre_ids"])

            # Build the object payload
#            movie_obj = {
#                "title": movie["title"],
#                "overview": movie["overview"],
#                "vote_average": movie["vote_average"],
#                "genre_ids": genre_ids,
#                "release_date": release_date,
#                "tmdb_id": movie["id"],
#            }

            # Add object to batch queue
#            batch.add_object(
#                properties=movie_obj,
#                uuid=generate_uuid5(movie["id"])
                # references=reference_obj  # You can add references here
#            )
            # Batcher automatically sends batches

# Check for failed objects
#    if len(movies.batch.failed_objects) > 0:
#        print(f"Failed to import {len(movies.batch.failed_objects)} objects")





#    data_url = "https://raw.githubusercontent.com/weaviate-tutorials/edu-datasets/main/movies_data_1990_2024.json"
#    resp = requests.get(data_url)
#    df = pd.DataFrame(resp.json())    
    #print(df.head())
    
    

            
               
# Adding Objects to Weaviate 
    # Enter context manager
#    with movies.batch.rate_limit(2400) as batch:
        # Loop through the data
#        for i, movie in tqdm(df.iterrows()):
            # Convert data types
            # Convert a JSON date to `datetime` and add time zone information
#            release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d").replace(
#                tzinfo=timezone.utc
#            )
            # Convert a JSON array to a list of integers
#            genre_ids = json.loads(movie["genre_ids"])

            # Build the object payload
#            movie_obj = {
#                "title": movie["title"],
#                "overview": movie["overview"],
#                "vote_average": movie["vote_average"],
#                "genre_ids": genre_ids,
#                "release_date": release_date,
#                "tmdb_id": movie["id"],
#            }

            # Add object to batch queue
#            batch.add_object(
#                properties=movie_obj,
#                uuid=generate_uuid5(movie["id"])
                # references=reference_obj  # You can add references here
#            )
            # Batcher automatically sends batches

# Check for failed objects
#    if len(movies.batch.failed_objects) > 0:
#        print(f"Failed to import {len(movies.batch.failed_objects)} objects")

# Semantic Search 
    # Perform query
#    response = movies.query.near_text(
#        query="wars stargaze", limit=5, return_metadata=wq.MetadataQuery(distance=True)
#    )    

    # Inspect the response
#    for o in response.objects:
#        print(
#            o.properties["title"], o.properties["release_date"].year
#        )  # Print the title and release year (note the release date is a datetime object)
#        print(
#            f"Distance to query: {o.metadata.distance:.3f}\n"
#        )  # Print the distance of the object from the query    



# Hybrid Search
    # Perform query
    #response = movies.query.bm25(
    #    query="history", limit=5, return_metadata=wq.MetadataQuery(score=True)
    #)

    # Inspect the response
    #for o in response.objects:
    #    print(
    #        o.properties["title"], o.properties["release_date"].year
    #    )  # Print the title and release year (note the release date is a datetime object)
    #    print(
    #        f"BM25 score: {o.metadata.score:.3f}\n"
    #    )  # Print the BM25 score of the object from the query    
    
    
# Filter Searchs     
    # Perform query
    #response = movies.query.near_text(
    #    query="dystopian future",
    #    limit=5,
    #    return_metadata=wq.MetadataQuery(distance=True),
    #    filters=wq.Filter.by_property("release_date").greater_than(datetime(2020, 1, 1))
    #)

    # Inspect the response
    #for o in response.objects:
    #    print(
    #        o.properties["title"], o.properties["release_date"].year
    #    )  # Print the title and release year (note the release date is a datetime object)
    #    print(
    #        f"Distance to query: {o.metadata.distance:.3f}\n"
    #    )  # Print the distance of the object from the query    
    
    
