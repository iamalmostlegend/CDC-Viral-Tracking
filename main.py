import json
import requests
from supabase import create_client, Client

# Define the SODA API URL
cdc_api_url = "https://data.cdc.gov/resource/vutn-jzwm.json"
supabase_url = 'https://ijpzslpbqiqdqnxicneg.supabase.co'
supabase_key = '''eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..5I5zieVevpNztTAARK8nTQOk7FMZ944YcaDZlqlQhzk'''
supabase_client = Client(supabase_url, supabase_key)
user='postgres'
password = ['']
host = 'db.ijpzslpbqiqdqnxicneg.supabase.co'
port = 5432
database = 'postgres'
def pull_cdc_data():  #(you may need to include filters or queries)
    params = {'limit':1000}
    response = requests.get(cdc_api_url)

    if response.status_code == 200:  # Check for a successful response
        print("Data Retrieved Successfully")
        return response.json()
    else:
        print("Failed to fetch CDC data from the API.")
        return None

data = pull_cdc_data()

def add_entries_to_table(supabase, table_name, data):
    # Modify this function to handle your real data for the specified table
    main_list = []
    for entry in data:
        value = {
            'week_end': entry['week_end'],  # Replace with actual field names
            'pathogen': entry['pathogen'],  # Replace with actual field names
            'geography': entry['geography'],
            'percent_visits': entry['percent_visits']
        }
        main_list.append(value)

    insert_data = supabase.table(table_name).insert(main_list).execute()
    data_json = json.loads(insert_data.model_dump_json())
    #data_entries = data_json['data']
    data_entries = data_json.get('data', [])
    fk_list = [str(entry['week_end']) for entry in data_entries]

    return fk_list


def main():
    url = supabase_url
    key = supabase_key
    supabase_client: Client = create_client(url, key)  # Create Supabase client

    data = pull_cdc_data()
    if data is not None:
        table_name = 'CDC Viral Data'
        fk_list = add_entries_to_table(supabase_client, table_name, data)
    print(fk_list)

main()


