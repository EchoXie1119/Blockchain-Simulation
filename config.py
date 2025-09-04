"""
Configuration module for blockchain simulation
Contains all blockchain configurations, constants, and default parameters
"""

from dataclasses import dataclass
from typing import Dict, Any

# Global simulation constants
HEADER_SIZE = 1024  # bytes
TRANSACTION_SIZE = 256  # bytes per transaction
DIFFICULTY_ADJUSTMENT_BLOCKS = 2016
MAX_HALVINGS = 35
MIN_REWARD_THRESHOLD = 0.00000001

# Blockchain configurations for different cryptocurrencies
BLOCKCHAIN_CONFIGS = {
    'BTC': {
        'name': 'Bitcoin',
        'reward': 50,
        'halving': 210000,
        'block_time': 600,  # 10 minutes
        'max_tx_per_block': 4000,
        'block_size_limit': 1 * 1024 * 1024,  # 1 MB
        'description': 'Original Bitcoin with 10-minute block time'
    },
    'BCH': {
        'name': 'Bitcoin Cash',
        'reward': 12.5,
        'halving': 210000,
        'block_time': 600,  # 10 minutes
        'max_tx_per_block': 128000,
        'block_size_limit': 32 * 1024 * 1024,  # 32 MB
        'description': 'Bitcoin Cash with larger blocks'
    },
    'LTC': {
        'name': 'Litecoin',
        'reward': 50,
        'halving': 840000,
        'block_time': 150,  # 2.5 minutes
        'max_tx_per_block': 4000,
        'block_size_limit': 1 * 1024 * 1024,  # 1 MB
        'description': 'Litecoin with faster block time'
    },
    'DOGE': {
        'name': 'Dogecoin',
        'reward': 10000,
        'halving': None,  # Static reward
        'block_time': 60,  # 1 minute
        'max_tx_per_block': 4000,
        'block_size_limit': 1 * 1024 * 1024,  # 1 MB
        'description': 'Dogecoin with static reward'
    },
    'MEMO': {
        'name': 'MEMO',
        'reward': 51.8457072,
        'halving': 9644000,
        'block_time': 3.27,  # Very fast blocks
        'max_tx_per_block': 32000,
        'block_size_limit': 8 * 1024 * 1024,  # 8 MB
        'description': 'MEMO with very fast block time'
    }
}

# Workload configurations
WORKLOAD_CONFIGS = {
    'NONE': {
        'wallets': 0,
        'transactions': 0,
        'interval': 1.0,
        'description': 'No user transactions, mining only'
    },
    'SMALL': {
        'wallets': 10,
        'transactions': 10,
        'interval': 10.0,
        'description': 'Small workload: 10 wallets, 10 transactions each, 10s interval'
    },
    'MEDIUM': {
        'wallets': 1000,
        'transactions': 1000,
        'interval': 1.0,
        'description': 'Medium workload: 1000 wallets, 1000 transactions each, 1s interval'
    },
    'LARGE': {
        'wallets': 1000,
        'transactions': 1000,
        'interval': 0.01,
        'description': 'Large workload: 1000 wallets, 1000 transactions each, 0.01s interval'
    }
}

# Default simulation parameters
DEFAULT_CONFIG = {
    'nodes': 10,
    'neighbors': 3,
    'miners': 5,
    'hashrate': 1000,
    'blocktime': 600,
    'difficulty': None,  # Will be calculated as blocktime * miners * hashrate
    'reward': 50,
    'halving': 210000,
    'wallets': 0,
    'transactions': 0,
    'interval': 1.0,
    'blocksize': 4000,
    'blocks': None,
    'print': 144,
    'debug': False
}

# Logging configuration
LOG_CONFIG = {
    'level': 'ERROR',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'blockchain_simulation.log'
}

# Network simulation parameters
NETWORK_CONFIG = {
    'latency_min': 0.001,  # Minimum network latency in seconds
    'latency_max': 0.1,    # Maximum network latency in seconds
    'bandwidth_limit': 100 * 1024 * 1024,  # 100 MB/s bandwidth limit
    'packet_loss_rate': 0.001,  # 0.1% packet loss rate
    'max_propagation_time': 60.0,  # Maximum block propagation time in seconds
    'congestion_threshold': 1024 * 1024,  # Block size threshold for congestion (1MB)
    'congestion_factor': 0.1,  # 10% congestion per MB over threshold
    'processing_delay_min': 0.001,  # Minimum block processing delay
    'processing_delay_max': 0.01,   # Maximum block processing delay
    'distance_variance': 0.2,  # 20% variance for network distance simulation
    'bandwidth_variance': 0.2,  # 20% variance in bandwidth per node
    'packet_loss_variance': 0.5,  # 50% variance in packet loss per node
}

# Mining parameters
MINING_CONFIG = {
    'hashrate_variance': 0.1,  # 10% variance in hashrate
    'difficulty_adjustment_factor': 0.25,  # How much to adjust difficulty
    'max_difficulty_change': 4.0  # Maximum 4x difficulty change
}

# Transaction parameters
TRANSACTION_CONFIG = {
    'min_amount': 0.1,
    'max_amount': 10.0,
    'min_fee': 0.001,
    'max_fee': 0.1,
    'fee_rate': 0.01  # 1% fee rate
}


@dataclass
class SimulationConfig:
    """Configuration class for simulation parameters"""
    nodes: int
    neighbors: int
    miners: int
    hashrate: float
    blocktime: float
    difficulty: float
    reward: float
    halving: int
    wallets: int
    transactions: int
    interval: float
    blocksize: int
    blocks: int
    years: float
    print_interval: int
    debug: bool
    
    @classmethod
    def from_args(cls, args):
        """Create configuration from command line arguments"""
        # Calculate blocks from years if specified
        blocks = args.blocks
        years = getattr(args, 'years', 1.0)
        if hasattr(args, 'years') and args.years and not args.blocks:
            seconds_per_year = 365 * 24 * 60 * 60
            blocks_per_year = seconds_per_year / args.blocktime
            blocks = int(blocks_per_year * args.years)
        
        return cls(
            nodes=args.nodes,
            neighbors=args.neighbors,
            miners=args.miners,
            hashrate=args.hashrate,
            blocktime=args.blocktime,
            difficulty=args.difficulty or (args.blocktime * args.miners * args.hashrate),
            reward=args.reward,
            halving=args.halving,
            wallets=args.wallets,
            transactions=args.transactions,
            interval=args.interval,
            blocksize=args.blocksize,
            blocks=blocks,
            years=years,
            print_interval=args.print,
            debug=args.debug
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            'nodes': self.nodes,
            'neighbors': self.neighbors,
            'miners': self.miners,
            'hashrate': self.hashrate,
            'blocktime': self.blocktime,
            'difficulty': self.difficulty,
            'reward': self.reward,
            'halving': self.halving,
            'wallets': self.wallets,
            'transactions': self.transactions,
            'interval': self.interval,
            'blocksize': self.blocksize,
            'blocks': self.blocks,
            'years': self.years,
            'print_interval': self.print_interval,
            'debug': self.debug
        } 