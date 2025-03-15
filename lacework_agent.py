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