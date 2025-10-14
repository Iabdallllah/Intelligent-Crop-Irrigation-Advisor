import paho.mqtt
print("Loaded paho-mqtt version:", paho.mqtt.__version__)

import json
import os
import ssl 
from contextlib import asynccontextmanager
from typing import Dict, Any

# Libraries
from fastapi import FastAPI
from paho.mqtt import client as mqtt_client
from supabase import create_client, Client
from dotenv import load_dotenv

# --- 1. Load Configuration and Secrets ---
load_dotenv()

# Supabase Configuration
SUPABASE_URL: str = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY: str = os.getenv("SUPABASE_SERVICE_KEY")

# MQTT Configuration (Using environment variables for secure connection)
# Broker and Port will be read from the .env file
MQTT_BROKER: str = os.getenv("MQTT_BROKER") 
MQTT_PORT: int = int(os.getenv("MQTT_PORT")) 
MQTT_USER: str = os.getenv("MQTT_USER") # Username for private broker
MQTT_PASSWORD: str = os.getenv("MQTT_PASSWORD") # Password for private broker
MQTT_TOPIC: str = os.getenv("MQTT_TOPIC")
MQTT_CLIENT_ID: str = "FastAPI_Ingestion_Service_001" # Unique Client ID for the subscriber

# Database client and MQTT client instances
supabase: Client | None = None
mqttc: mqtt_client.Client | None = None

# --- 2. MQTT Callback Functions ---

def on_connect(client, userdata, flags, rc):
    """Callback function for when the client connects to the MQTT broker."""
    if rc == 0:
        print(f"MQTT Connected successfully. Subscribing to topic: {MQTT_TOPIC}")
        client.subscribe(MQTT_TOPIC)
    elif rc == 5:
        # rc=5 means Connection Refused, unauthorized (wrong username/password)
        print("Failed to connect, return code 5: Authentication failed (check MQTT_USER/PASSWORD)")
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    """
    Callback function when a message is received on the subscribed topic.
    This logic assumes the JSON structure matches the fields defined in the payload dictionary.
    """
    global supabase
    if not supabase:
        print("Error: Supabase client not initialized.")
        return

    try:
        # 1. Parse the incoming JSON payload from the ESP32
        data: Dict[str, Any] = json.loads(msg.payload.decode('utf-8'))
        # NOTE: If data coming from ESP32 is NULL, it will still insert, but Supabase might reject
        print(f"Received data: {data}")

        # 2. Structure the data for Supabase insertion 
        # NOTE: Ensure these keys match the columns in your Supabase 'sensor_readings' table
        payload = {
            "temperature": data.get("temperature"),
            "humidity": data.get("humidity"),
            "water_level_raw": data.get("water_level_raw"),
            "rain_status": data.get("rain_status"),
            "servo_angle": data.get("servo_angle"),
        }
        
        # 3. Insert data into the 'sensor_readings' table
        response = supabase.table('Sensor readings').insert(payload).execute()
        
        # Check for insertion errors
        if response.data:
            print(f"Successfully inserted record: {response.data[0]['id']}")
        elif response.error:
             print(f"Supabase error: {response.error}")

    except json.JSONDecodeError:
        print(f"Error decoding JSON payload: {msg.payload}")
    except Exception as e:
        print(f"An unexpected error occurred during insertion: {e}")


# --- 3. FastAPI Lifespan (Startup/Shutdown) ---

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup (DB/MQTT connection) and shutdown (MQTT disconnect) events.
    """
    global supabase, mqttc
    
    # --- Startup Logic ---
    print("--- FastAPI Startup ---")
    
    # Initialize Supabase Client
    supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    
    # Initialize MQTT Client
    # FINAL FIX: Removed CallbackAPIVersion for compatibility with older paho-mqtt versions.
    
    mqttc = mqtt_client.Client(
        mqtt_client.CallbackAPIVersion.VERSION1,
        client_id=MQTT_CLIENT_ID,
        transport="websockets",
        protocol=mqtt_client.MQTTv311
    )

    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    
    # 1. Set Username and Password for Private Broker Authentication
    mqttc.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    
    # 2. Configure TLS/SSL for secure WebSocket connection (required by HiveMQ Cloud)
    mqttc.tls_set(certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS, ciphers=None)
    
    # DIAGNOSTIC PRINT: Check the loaded broker URL 
    print(f"Attempting to connect to: wss://{MQTT_BROKER}:{MQTT_PORT}/mqtt")
    
    # Connect and start the background thread loop
    try:
        # Pass the WebSocket path directly to connect()
        mqttc.connect(
            MQTT_BROKER, 
            MQTT_PORT, 
            60,
        )
        mqttc.loop_start()  # Starts a new thread to handle network traffic
    except Exception as e:
        print(f"Could not connect to MQTT broker: {e}")

    yield
    
    # --- Shutdown Logic ---
    print("--- FastAPI Shutdown ---")
    if mqttc:
        mqttc.loop_stop()
        mqttc.disconnect()

# --- 4. FastAPI Application Setup ---
app = FastAPI(lifespan=lifespan, title="Rain Collector Ingestion Service")

@app.get("/")
def read_root():
    """Simple status check for the API."""
    return {"status": "ok", "service": "MQTT Ingestion Running"}

# --- 5. Run the Service ---
# To run this, use the command: uvicorn data_ingestion:app --reload