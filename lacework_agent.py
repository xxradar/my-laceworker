#!/usr/bin/env python3
import os
import json
import argparse
import glob
import sys
import logging
import time
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# Import OpenAI Agents SDK (if available)
try:
    from agents import Agent, Runner
    AGENTS_SDK_AVAILABLE = True
except ImportError:
    AGENTS_SDK_AVAILABLE = False

# Set up logging
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
log_filename = os.path.join(LOG_DIR, f"lacework_agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)

# Configuration file to store vector store ID
CONFIG_FILE = "lacework_vector_store_config.json"
DOCS_DIR = "lacework_cli_docs"

def load_config():
    """Load configuration from JSON file or return empty dict if file doesn't exist"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {"vector_store_id": None}

def save_config(config):
    """Save configuration to JSON file"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def create_vector_store(client, name="Lacework CLI Documentation"):
    """Create a new vector store and return its ID"""
    print(f"Creating vector store: {name}")
    vector_store = client.vector_stores.create(name=name)
    print(f"Vector store created with ID: {vector_store.id}")
    return vector_store

def upload_docs_to_vector_store(client, vector_store_id):
    """Upload all markdown files from lacework_cli_docs to the vector store"""
    # Get all markdown files in the docs directory
    file_paths = glob.glob(os.path.join(DOCS_DIR, "*.md"))
    
    if not file_paths:
        print(f"No markdown files found in {DOCS_DIR}")
        return
    
    print(f"Found {len(file_paths)} markdown files to upload")
    
    # Open file streams for all files
    file_streams = [open(path, "rb") for path in file_paths]
    
    try:
        # Upload files to vector store
        print("Uploading files to vector store...")
        file_batch = client.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store_id,
            files=file_streams
        )
        
        # Print status and file counts
        print(f"Upload status: {file_batch.status}")
        print(f"File counts: {file_batch.file_counts}")
        
        return file_batch
    finally:
        # Close all file streams
        for stream in file_streams:
            stream.close()

def attach_file_to_vector_store(client, vector_store_id, file_path):
    """Attach a single file to the vector store and verify completion"""
    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        print(f"Error: File not found: {file_path}")
        return False
    
    filename = os.path.basename(file_path)
    logging.info(f"Attaching file: {filename}")
    print(f"Attaching file: {filename}")
    
    try:
        # Step 1: Upload the file to OpenAI
        logging.info(f"Step 1: Uploading file to OpenAI: {filename}")
        print(f"Step 1: Uploading file to OpenAI...")
        
        with open(file_path, "rb") as file_stream:
            uploaded_file = client.files.create(
                file=file_stream,
                purpose="assistants"
            )
        
        file_id = uploaded_file.id
        logging.info(f"File uploaded with ID: {file_id}")
        print(f"File uploaded with ID: {file_id}")
        
        # Step 2: Attach the file to the vector store
        logging.info(f"Step 2: Attaching file to vector store: {file_id}")
        print(f"Step 2: Attaching file to vector store...")
        
        # Wait a moment before attaching to ensure the file is processed
        time.sleep(1)
        
        vector_store_file = client.vector_stores.files.create(
            vector_store_id=vector_store_id,
            file_id=file_id
        )
        
        # Step 3: Verify the file was attached successfully
        logging.info(f"Verifying file attachment status...")
        print(f"Verifying file attachment status...")
        
        # Wait a moment to allow processing
        time.sleep(1)
        
        # Check the status of the file in the vector store
        file_status = client.vector_stores.files.retrieve(
            vector_store_id=vector_store_id,
            file_id=file_id
        )
        
        status = file_status.status if hasattr(file_status, 'status') else "unknown"
        logging.info(f"File attachment status: {status}")
        print(f"File attachment status: {status}")
        
        if status == "completed":
            logging.info(f"File successfully attached: {filename}")
            print(f"✅ File successfully attached: {filename}")
            return True
        elif status == "in_progress":
            logging.info(f"File attachment in progress: {filename}")
            print(f"⏳ File attachment in progress: {filename}")
            print(f"  The file will continue processing in the background.")
            return True
        else:
            logging.error(f"File attachment has issues: {status}")
            print(f"⚠️ File attachment has issues: {status}")
            
            if hasattr(file_status, 'last_error') and file_status.last_error:
                logging.error(f"Error details: {file_status.last_error}")
                print(f"  Error details: {file_status.last_error}")
            
            return False
    
    except Exception as e:
        logging.exception(f"Error attaching file: {str(e)}")
        print(f"Error attaching file: {str(e)}")
        return False