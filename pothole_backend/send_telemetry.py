from supabase import create_client, Client
import os
import threading

supabase_url = os.environ.get('SUPABASE_URL')
supabase_key = os.environ.get('SUPABASE_KEY')

supabase: Client = create_client(supabase_url, supabase_key)

def send_data(pred_data):
    response = supabase.table('road_damage_events').insert(pred_data).execute()
    print("data terkirim", response.data)