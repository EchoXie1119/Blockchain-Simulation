"""
Data models for blockchain simulation
Contains all data structures and classes used throughout the simulation
"""

import hashlib
import time
from dataclasses import dataclass, field
from typing import List, Set, Dict, Optional
from collections import deque
import logging

logger = logging.getLogger(__name__)


@dataclass
class Block:
    """
    Block structure representing a blockchain block
    
    Attributes:
        block_id: Unique identifier for the block
        timestamp: When the block was created
        time_since_last: Time since the previous block
        transaction_count: Number of transactions in this block
        size: Total size of the block in bytes
        transactions: List of transaction IDs in this block
        miner_reward: Mining reward for this block
        previous_hash: Hash of the previous block
        miner_id: ID of the miner who created this block
        difficulty: Mining difficulty when this block was created
    """
    block_id: str
    timestamp: float
    time_since_last: float
    transaction_count: int
    size: int
    transactions: List[str] = field(default_factory=list)
    miner_reward: float = 0.0
    previous_hash: str = ""
    miner_id: str = ""
    difficulty: float = 0.0
    
    def __post_init__(self):
        """Calculate block hash after initialization"""
        self.hash = self.calculate_hash()
        
    def calculate_hash(self) -> str:
        """Calculate the hash of this block"""
        block_data = f"{self.block_id}{self.timestamp}{self.previous_hash}{self.miner_id}"
        return hashlib.sha256(block_data.encode()).hexdigest()
    
    def to_dict(self) -> Dict:
        """Convert block to dictionary for serialization"""
        return {
            'block_id': self.block_id,
            'timestamp': self.timestamp,
            'time_since_last': self.time_since_last,
            'transaction_count': self.transaction_count,
            'size': self.size,
            'transactions': self.transactions,
            'miner_reward': self.miner_reward,
            'previous_hash': self.previous_hash,
            'miner_id': self.miner_id,
            'difficulty': self.difficulty,
            'hash': self.hash
        }


@dataclass
class Transaction:
    """
    Transaction structure representing a blockchain transaction
    
    Attributes:
        tx_id: Unique identifier for the transaction
        sender: Wallet ID of the sender
        recipient: Wallet ID of the recipient
        amount: Transaction amount
        fee: Transaction fee
        timestamp: When the transaction was created
        status: Current status of the transaction
        priority: Transaction priority (low, normal, high, urgent)
        network_congestion: Network congestion when transaction was created
    """
    tx_id: str
    sender: str
    recipient: str
    amount: float
    fee: float
    timestamp: float
    status: str = "pending"  # pending, confirmed, failed
    priority: str = "normal"  # low, normal, high, urgent
    network_congestion: float = 0.0  # Network congestion level (0.0 to 1.0)
    
    def __post_init__(self):
        """Calculate transaction hash after initialization"""
        self.hash = self.calculate_hash()
        
    def calculate_hash(self) -> str:
        """Calculate the hash of this transaction"""
        tx_data = f"{self.tx_id}{self.sender}{self.recipient}{self.amount}{self.fee}{self.timestamp}{self.priority}"
        return hashlib.sha256(tx_data.encode()).hexdigest()
    
    def to_dict(self) -> Dict:
        """Convert transaction to dictionary for serialization"""
        return {
            'tx_id': self.tx_id,
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'fee': self.fee,
            'timestamp': self.timestamp,
            'status': self.status,
            'priority': self.priority,
            'network_congestion': self.network_congestion,
            'hash': self.hash
        }


@dataclass
class Wallet:
    """
    Wallet structure representing a user wallet
    
    Attributes:
        wallet_id: Unique identifier for the wallet
        balance: Current balance of the wallet
        transactions_sent: Number of transactions sent
        transactions_received: Number of transactions received
        total_sent: Total amount sent
        total_received: Total amount received
        total_fees: Total fees paid
    """
    wallet_id: str
    balance: float = 0.0
    transactions_sent: int = 0
    transactions_received: int = 0
    total_sent: float = 0.0
    total_received: float = 0.0
    total_fees: float = 0.0
    
    def add_balance(self, amount: float):
        """Add amount to wallet balance"""
        self.balance += amount
        self.total_received += amount
        self.transactions_received += 1
        logger.debug(f"Wallet {self.wallet_id} received {amount:.6f}, new balance: {self.balance:.6f}")
        
    def subtract_balance(self, amount: float, fee: float = 0.0):
        """Subtract amount and fee from wallet balance"""
        total_deduction = amount + fee
        if self.balance >= total_deduction:
            self.balance -= total_deduction
            self.total_sent += amount
            self.total_fees += fee
            self.transactions_sent += 1
            logger.debug(f"Wallet {self.wallet_id} sent {amount:.6f} + {fee:.6f} fee, new balance: {self.balance:.6f}")
            return True
        else:
            logger.warning(f"Wallet {self.wallet_id} insufficient balance: {self.balance:.6f} < {total_deduction:.6f}")
            return False
    
    def to_dict(self) -> Dict:
        """Convert wallet to dictionary for serialization"""
        return {
            'wallet_id': self.wallet_id,
            'balance': self.balance,
            'transactions_sent': self.transactions_sent,
            'transactions_received': self.transactions_received,
            'total_sent': self.total_sent,
            'total_received': self.total_received,
            'total_fees': self.total_fees
        }


@dataclass
class NetworkStats:
    """
    Network statistics for monitoring network performance
    
    Attributes:
        total_blocks_propagated: Total number of blocks propagated
        total_transactions_propagated: Total number of transactions propagated
        total_network_data: Total data transferred in bytes
        total_io_requests: Total I/O requests made
        average_propagation_time: Average time for block propagation
        network_latency: Current network latency
        packet_loss_rate: Current packet loss rate
    """
    total_blocks_propagated: int = 0
    total_transactions_propagated: int = 0
    total_network_data: int = 0
    total_io_requests: int = 0
    average_propagation_time: float = 0.0
    network_latency: float = 0.0
    packet_loss_rate: float = 0.0
    
    def update_propagation_stats(self, block_size: int, propagation_time: float):
        """Update propagation statistics"""
        self.total_blocks_propagated += 1
        self.total_network_data += block_size
        self.total_io_requests += 1
        
        # Update average propagation time
        if self.total_blocks_propagated == 1:
            self.average_propagation_time = propagation_time
        else:
            self.average_propagation_time = (
                (self.average_propagation_time * (self.total_blocks_propagated - 1) + propagation_time) 
                / self.total_blocks_propagated
            )
    
    def to_dict(self) -> Dict:
        """Convert network stats to dictionary"""
        return {
            'total_blocks_propagated': self.total_blocks_propagated,
            'total_transactions_propagated': self.total_transactions_propagated,
            'total_network_data': self.total_network_data,
            'total_io_requests': self.total_io_requests,
            'average_propagation_time': self.average_propagation_time,
            'network_latency': self.network_latency,
            'packet_loss_rate': self.packet_loss_rate
        }


@dataclass
class MiningStats:
    """
    Mining statistics for monitoring mining performance
    
    Attributes:
        total_blocks_mined: Total number of blocks mined
        total_mining_time: Total time spent mining
        average_mining_time: Average time per block
        current_difficulty: Current mining difficulty
        total_hashrate: Total network hashrate
        blocks_per_miner: Dictionary of blocks mined per miner
    """
    total_blocks_mined: int = 0
    total_mining_time: float = 0.0
    average_mining_time: float = 0.0
    current_difficulty: float = 0.0
    total_hashrate: float = 0.0
    blocks_per_miner: Dict[str, int] = field(default_factory=dict)
    
    def update_mining_stats(self, miner_id: str, mining_time: float, difficulty: float):
        """Update mining statistics"""
        self.total_blocks_mined += 1
        self.total_mining_time += mining_time
        self.current_difficulty = difficulty
        
        # Update blocks per miner
        if miner_id not in self.blocks_per_miner:
            self.blocks_per_miner[miner_id] = 0
        self.blocks_per_miner[miner_id] += 1
        
        # Update average mining time
        self.average_mining_time = self.total_mining_time / self.total_blocks_mined
    
    def to_dict(self) -> Dict:
        """Convert mining stats to dictionary"""
        return {
            'total_blocks_mined': self.total_blocks_mined,
            'total_mining_time': self.total_mining_time,
            'average_mining_time': self.average_mining_time,
            'current_difficulty': self.current_difficulty,
            'total_hashrate': self.total_hashrate,
            'blocks_per_miner': self.blocks_per_miner.copy()
        }


@dataclass
class SimulationStats:
    """
    Overall simulation statistics
    
    Attributes:
        start_time: Simulation start time
        end_time: Simulation end time
        total_blocks: Total blocks created
        total_transactions: Total transactions processed
        total_coins: Total coins created
        network_stats: Network statistics
        mining_stats: Mining statistics
    """
    start_time: float = field(default_factory=time.time)
    end_time: float = 0.0
    total_blocks: int = 0
    total_transactions: int = 0
    total_coins: float = 0.0
    network_stats: NetworkStats = field(default_factory=NetworkStats)
    mining_stats: MiningStats = field(default_factory=MiningStats)
    
    def finish(self):
        """Mark simulation as finished"""
        self.end_time = time.time()
    
    def get_duration(self) -> float:
        """Get simulation duration in seconds"""
        return self.end_time - self.start_time if self.end_time > 0 else time.time() - self.start_time
    
    def get_transactions_per_second(self) -> float:
        """Get transactions per second"""
        duration = self.get_duration()
        return self.total_transactions / duration if duration > 0 else 0.0
    
    def get_blocks_per_second(self) -> float:
        """Get blocks per second"""
        duration = self.get_duration()
        return self.total_blocks / duration if duration > 0 else 0.0
    
    def to_dict(self) -> Dict:
        """Convert simulation stats to dictionary"""
        return {
            'start_time': self.start_time,
            'end_time': self.end_time,
            'duration': self.get_duration(),
            'total_blocks': self.total_blocks,
            'total_transactions': self.total_transactions,
            'total_coins': self.total_coins,
            'transactions_per_second': self.get_transactions_per_second(),
            'blocks_per_second': self.get_blocks_per_second(),
            'network_stats': self.network_stats.to_dict(),
            'mining_stats': self.mining_stats.to_dict()
        } 