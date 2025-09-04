"""
Trace loader module for blockchain simulation
Handles loading real-world blockchain data traces for realistic simulation
"""

import json
import csv
import time
import random
import logging
from typing import List, Dict, Optional, Generator
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime, timedelta

# Optional import for API functionality
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    logging.warning("requests module not available. API functionality will be disabled.")

from models import Transaction, Block
from config import TRANSACTION_CONFIG

logger = logging.getLogger(__name__)


@dataclass
class TraceEvent:
    """Represents a single event from a blockchain trace"""
    event_type: str  # transaction, block, miner_join, miner_leave, network_event
    timestamp: float
    data: Dict
    source: str  # Source of the trace data


@dataclass
class TraceLoader:
    """
    Loads and processes blockchain trace data from various sources
    
    Supports:
    - JSON trace files
    - CSV transaction logs
    - Real-time API data
    - Historical blockchain data
    """
    
    def __init__(self, trace_dir: str = "traces"):
        self.trace_dir = Path(trace_dir)
        self.trace_dir.mkdir(exist_ok=True)
        self.loaded_traces: List[TraceEvent] = []
        self.current_index = 0
        
        logger.info(f"Initialized trace loader with directory: {self.trace_dir}")
        
    def load_json_trace(self, filename: str) -> List[TraceEvent]:
        """Load trace data from JSON file"""
        filepath = self.trace_dir / filename
        
        if not filepath.exists():
            logger.warning(f"Trace file not found: {filepath}")
            return []
            
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                
            events = []
            for item in data:
                event = TraceEvent(
                    event_type=item.get('type', 'unknown'),
                    timestamp=item.get('timestamp', time.time()),
                    data=item.get('data', {}),
                    source=filename
                )
                events.append(event)
                
            logger.info(f"Loaded {len(events)} events from {filename}")
            return events
            
        except Exception as e:
            logger.error(f"Error loading JSON trace {filename}: {e}")
            return []
            
    def load_csv_trace(self, filename: str) -> List[TraceEvent]:
        """Load trace data from CSV file"""
        filepath = self.trace_dir / filename
        
        if not filepath.exists():
            logger.warning(f"Trace file not found: {filepath}")
            return []
            
        try:
            events = []
            with open(filepath, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Parse timestamp
                    timestamp = float(row.get('timestamp', time.time()))
                    
                    # Determine event type from data
                    event_type = 'transaction'
                    if 'block_hash' in row:
                        event_type = 'block'
                    elif 'miner_id' in row and 'action' in row:
                        event_type = f"miner_{row['action']}"
                        
                    event = TraceEvent(
                        event_type=event_type,
                        timestamp=timestamp,
                        data=row,
                        source=filename
                    )
                    events.append(event)
                    
            logger.info(f"Loaded {len(events)} events from {filename}")
            return events
            
        except Exception as e:
            logger.error(f"Error loading CSV trace {filename}: {e}")
            return []
            
    def load_bitcoin_api_data(self, start_date: str, end_date: str, 
                            limit: int = 1000) -> List[TraceEvent]:
        """
        Load real Bitcoin transaction data from public APIs
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            limit: Maximum number of transactions to load
        """
        if not REQUESTS_AVAILABLE:
            logger.warning("requests module not available. Cannot load Bitcoin API data.")
            return []
            
        try:
            # Use a public Bitcoin API (example with blockchain.info)
            # Note: In production, you might want to use a more reliable API
            url = f"https://blockchain.info/rawaddr/1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
            
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                logger.warning(f"Failed to fetch Bitcoin data: {response.status_code}")
                return []
                
            data = response.json()
            events = []
            
            # Process transactions
            for tx in data.get('txs', [])[:limit]:
                # Parse timestamp
                timestamp = tx.get('time', time.time())
                
                # Create transaction event
                event = TraceEvent(
                    event_type='transaction',
                    timestamp=timestamp,
                    data={
                        'tx_hash': tx.get('hash', ''),
                        'amount': tx.get('result', 0) / 100000000,  # Convert satoshis to BTC
                        'fee': 0.0,  # Fee not directly available
                        'inputs': len(tx.get('inputs', [])),
                        'outputs': len(tx.get('out', [])),
                        'size': tx.get('size', 0)
                    },
                    source='bitcoin_api'
                )
                events.append(event)
                
            logger.info(f"Loaded {len(events)} Bitcoin transactions from API")
            return events
            
        except Exception as e:
            logger.error(f"Error loading Bitcoin API data: {e}")
            return []
            
    def generate_synthetic_trace(self, duration_hours: int = 24, 
                               transaction_rate: float = 10.0) -> List[TraceEvent]:
        """
        Generate synthetic trace data for testing
        
        Args:
            duration_hours: Duration of the trace in hours
            transaction_rate: Transactions per second
        """
        events = []
        start_time = time.time()
        end_time = start_time + (duration_hours * 3600)
        
        current_time = start_time
        while current_time < end_time:
            # Generate transaction
            event = TraceEvent(
                event_type='transaction',
                timestamp=current_time,
                data={
                    'sender': f"wallet_{random.randint(0, 100)}",
                    'recipient': f"wallet_{random.randint(0, 100)}",
                    'amount': random.uniform(0.001, 1.0),
                    'fee': random.uniform(0.0001, 0.01),
                    'priority': random.choices(['low', 'normal', 'high'], weights=[0.2, 0.7, 0.1])[0]
                },
                source='synthetic'
            )
            events.append(event)
            
            # Generate miner events occasionally
            if random.random() < 0.01:  # 1% chance
                miner_event = TraceEvent(
                    event_type='miner_join' if random.random() < 0.5 else 'miner_leave',
                    timestamp=current_time,
                    data={
                        'miner_id': f"miner_{random.randint(0, 20)}",
                        'hashrate': random.uniform(100, 1000)
                    },
                    source='synthetic'
                )
                events.append(miner_event)
                
            # Generate network events occasionally
            if random.random() < 0.005:  # 0.5% chance
                network_event = TraceEvent(
                    event_type='network_event',
                    timestamp=current_time,
                    data={
                        'event': random.choice(['partition', 'heal', 'congestion']),
                        'severity': random.uniform(0.1, 1.0)
                    },
                    source='synthetic'
                )
                events.append(network_event)
                
            # Move to next event time
            current_time += random.exponential(1.0 / transaction_rate)
            
        # Sort events by timestamp
        events.sort(key=lambda x: x.timestamp)
        
        logger.info(f"Generated {len(events)} synthetic trace events")
        return events
        
    def load_all_traces(self) -> List[TraceEvent]:
        """Load all available trace files"""
        all_events = []
        
        # Load JSON traces
        for json_file in self.trace_dir.glob("*.json"):
            events = self.load_json_trace(json_file.name)
            all_events.extend(events)
            
        # Load CSV traces
        for csv_file in self.trace_dir.glob("*.csv"):
            events = self.load_csv_trace(csv_file.name)
            all_events.extend(events)
            
        # Sort all events by timestamp
        all_events.sort(key=lambda x: x.timestamp)
        
        logger.info(f"Loaded {len(all_events)} total trace events")
        return all_events
        
    def get_events_by_type(self, event_type: str) -> List[TraceEvent]:
        """Get all events of a specific type"""
        return [event for event in self.loaded_traces if event.event_type == event_type]
        
    def get_events_in_timerange(self, start_time: float, end_time: float) -> List[TraceEvent]:
        """Get events within a specific time range"""
        return [
            event for event in self.loaded_traces
            if start_time <= event.timestamp <= end_time
        ]
        
    def convert_to_transaction(self, event: TraceEvent) -> Optional[Transaction]:
        """Convert a trace event to a Transaction object"""
        if event.event_type != 'transaction':
            return None
            
        data = event.data
        
        # Handle different data formats
        if 'sender' in data and 'recipient' in data:
            # Direct transaction format
            return Transaction(
                tx_id=data.get('tx_hash', f"tx_{event.timestamp}"),
                sender=data['sender'],
                recipient=data['recipient'],
                amount=float(data.get('amount', 0.0)),
                fee=float(data.get('fee', 0.0)),
                timestamp=event.timestamp,
                priority=data.get('priority', 'normal'),
                network_congestion=data.get('network_congestion', 0.0)
            )
        elif 'tx_hash' in data:
            # Bitcoin API format
            return Transaction(
                tx_id=data['tx_hash'],
                sender="unknown",
                recipient="unknown",
                amount=float(data.get('amount', 0.0)),
                fee=float(data.get('fee', 0.0)),
                timestamp=event.timestamp,
                priority='normal',
                network_congestion=0.0
            )
            
        return None
        
    def convert_to_block(self, event: TraceEvent) -> Optional[Block]:
        """Convert a trace event to a Block object"""
        if event.event_type != 'block':
            return None
            
        data = event.data
        
        return Block(
            block_id=data.get('block_hash', f"block_{event.timestamp}"),
            timestamp=event.timestamp,
            time_since_last=float(data.get('time_since_last', 0.0)),
            transaction_count=int(data.get('transaction_count', 0)),
            size=int(data.get('size', 0)),
            miner_reward=float(data.get('miner_reward', 0.0)),
            miner_id=data.get('miner_id', 'unknown')
        )
        
    def stream_events(self, start_time: float = None, 
                     end_time: float = None) -> Generator[TraceEvent, None, None]:
        """
        Stream events in real-time simulation
        
        Args:
            start_time: Start time for streaming (None for current time)
            end_time: End time for streaming (None for no end)
        """
        if start_time is None:
            start_time = time.time()
            
        # Load all traces if not already loaded
        if not self.loaded_traces:
            self.loaded_traces = self.load_all_traces()
            
        # Filter events by time range
        events = self.loaded_traces
        if start_time:
            events = [e for e in events if e.timestamp >= start_time]
        if end_time:
            events = [e for e in events if e.timestamp <= end_time]
            
        # Stream events
        for event in events:
            # Wait until the event's timestamp
            wait_time = event.timestamp - time.time()
            if wait_time > 0:
                time.sleep(wait_time)
                
            yield event
            
    def save_trace(self, events: List[TraceEvent], filename: str):
        """Save trace events to a file"""
        filepath = self.trace_dir / filename
        
        try:
            data = []
            for event in events:
                data.append({
                    'type': event.event_type,
                    'timestamp': event.timestamp,
                    'data': event.data,
                    'source': event.source
                })
                
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
                
            logger.info(f"Saved {len(events)} events to {filename}")
            
        except Exception as e:
            logger.error(f"Error saving trace {filename}: {e}")
            
    def get_trace_statistics(self) -> Dict:
        """Get statistics about loaded traces"""
        if not self.loaded_traces:
            return {'total_events': 0}
            
        event_types = {}
        sources = {}
        time_range = {
            'start': min(e.timestamp for e in self.loaded_traces),
            'end': max(e.timestamp for e in self.loaded_traces)
        }
        
        for event in self.loaded_traces:
            # Count event types
            event_types[event.event_type] = event_types.get(event.event_type, 0) + 1
            
            # Count sources
            sources[event.source] = sources.get(event.source, 0) + 1
            
        return {
            'total_events': len(self.loaded_traces),
            'event_types': event_types,
            'sources': sources,
            'time_range': time_range,
            'duration_hours': (time_range['end'] - time_range['start']) / 3600
        }
        
    def to_dict(self) -> Dict:
        """Convert trace loader to dictionary"""
        return {
            'trace_dir': str(self.trace_dir),
            'loaded_traces': len(self.loaded_traces),
            'current_index': self.current_index,
            'statistics': self.get_trace_statistics()
        } 