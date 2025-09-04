#!/usr/bin/env python3
"""
Blockchain Simulation Script
CS595 Summer 2025 - PROJECT#2

This script simulates a blockchain network with nodes, miners, wallets, and transactions.
Uses a modular architecture for better maintainability and extensibility.
"""

import sys
import os

# Add current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from simulator import main

if __name__ == "__main__":
    main() 