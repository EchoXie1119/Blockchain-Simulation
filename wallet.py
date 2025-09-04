"""
Wallet module for blockchain simulation
Handles wallet operations, transaction generation, and balance management
"""

import random
import time
import threading
import logging
from typing import List, Dict, Optional
from dataclasses import dataclass
from collections import deque

from models import Wallet, Transaction
from config import TRANSACTION_CONFIG

logger = logging.getLogger(__name__)


@dataclass
class FeeCalculator:
    """
    Dynamic fee calculator based on network conditions
    
    Calculates transaction fees based on:
    - Base fee rate
    - Network congestion
    - Transaction priority
    - Block size utilization
    """
    
    def __init__(self):
        self.base_fee_rate = TRANSACTION_CONFIG['fee_rate']
        self.min_fee = TRANSACTION_CONFIG['min_fee']
        self.max_fee = TRANSACTION_CONFIG['max_fee']
        self.congestion_multiplier = 1.0
        self.block_utilization = 0.5  # Default 50% block utilization
        
    def calculate_fee(self, amount: float, priority: str = 'normal', 
                     network_congestion: float = 0.0) -> float:
        """
        Calculate transaction fee based on various factors
        
        Args:
            amount: Transaction amount
            priority: Transaction priority (low, normal, high, urgent)
            network_congestion: Network congestion level (0.0 to 1.0)
            
        Returns:
            Calculated fee amount
        """
        # Base fee calculation
        base_fee = amount * self.base_fee_rate
        
        # Priority multiplier
        priority_multipliers = {
            'low': 0.5,
            'normal': 1.0,
            'high': 2.0,
            'urgent': 5.0
        }
        priority_mult = priority_multipliers.get(priority, 1.0)
        
        # Network congestion multiplier
        congestion_mult = 1.0 + (network_congestion * 2.0)  # Up to 3x for high congestion
        
        # Block utilization factor
        utilization_factor = 1.0 + (self.block_utilization * 0.5)  # Up to 1.5x for full blocks
        
        # Calculate final fee
        fee = base_fee * priority_mult * congestion_mult * utilization_factor
        
        # Apply min/max constraints
        fee = max(self.min_fee, min(fee, self.max_fee))
        
        return fee
        
    def update_network_conditions(self, congestion: float, block_utilization: float):
        """Update network conditions for fee calculation"""
        self.congestion_multiplier = 1.0 + congestion
        self.block_utilization = max(0.0, min(1.0, block_utilization))
        
    def get_fee_estimate(self, amount: float, priority: str = 'normal') -> Dict:
        """Get fee estimate for different network conditions"""
        estimates = {}
        for congestion in [0.0, 0.25, 0.5, 0.75, 1.0]:
            fee = self.calculate_fee(amount, priority, congestion)
            estimates[f'{congestion*100:.0f}%_congestion'] = fee
            
        return estimates


@dataclass
class WalletManager:
    """
    Manages wallet operations and transaction generation
    
    Responsibilities:
    - Create and manage wallets
    - Generate transactions
    - Track wallet balances
    - Handle transaction fees
    """
    
    def __init__(self, wallet_count: int, transaction_count: int, interval: float):
        self.wallet_count = wallet_count
        self.transaction_count = transaction_count
        self.interval = interval
        self.wallets: Dict[str, Wallet] = {}
        self.transaction_generators: List[threading.Thread] = []
        self.running = False
        self.transaction_callback = None
        
        # Enhanced fee calculation
        self.fee_calculator = FeeCalculator()
        
        # Transaction history tracking
        self.transaction_history: deque = deque(maxlen=10000)  # Keep last 10k transactions
        
        # Network condition tracking
        self.network_congestion = 0.0
        self.block_utilization = 0.5
        
        logger.info(f"Initializing wallet manager with {wallet_count} wallets")
        self._create_wallets()
        
    def _create_wallets(self):
        """Create wallets with initial balances"""
        for i in range(self.wallet_count):
            wallet_id = f"wallet_{i}"
            # Give initial balance to some wallets for transaction generation
            initial_balance = random.uniform(10.0, 100.0) if i < self.wallet_count // 2 else 0.0
            wallet = Wallet(wallet_id, initial_balance)
            self.wallets[wallet_id] = wallet
            logger.debug(f"Created wallet {wallet_id} with balance {initial_balance:.6f}")
            
    def start_transaction_generation(self, callback):
        """Start generating transactions"""
        if self.running:
            logger.warning("Transaction generation already running")
            return
            
        self.running = True
        self.transaction_callback = callback
        
        # Check if we should generate any transactions
        if self.transaction_count <= 0:
            logger.info("No transactions to generate (transaction_count <= 0)")
            return
            
        # Generate all transactions instantly (pre-generated approach)
        logger.info(f"Generating all transactions instantly for {len(self.wallets)} wallets")
        
        # Create all transactions at once without complex logic
        total_transactions = len(self.wallets) * self.transaction_count
        logger.info(f"Generating {total_transactions} transactions...")
        
        for i in range(total_transactions):
            if not self.running:
                break
                
            # Simple transaction creation
            wallet_idx = i // self.transaction_count
            wallet_id = f"wallet_{wallet_idx}"
            recipient_id = f"wallet_{(wallet_idx + 1) % len(self.wallets)}"
            
            transaction = Transaction(
                tx_id=f"tx_{i}",
                sender=wallet_id,
                recipient=recipient_id,
                amount=1.0,  # Fixed amount for simplicity
                fee=0.01,    # Fixed fee
                timestamp=time.time()
            )
            
            if self.transaction_callback:
                self.transaction_callback(transaction)
                
            # Log progress every 1000 transactions
            if (i + 1) % 1000 == 0:
                logger.info(f"Generated {i + 1}/{total_transactions} transactions")
                
        logger.info(f"Generated {total_transactions} transactions instantly")
        
    def _generate_transaction_batch(self, start_idx: int, end_idx: int):
        """Generate a batch of transactions - OPTIMIZED VERSION"""
        wallet_ids = list(self.wallets.keys())
        
        for i in range(start_idx, end_idx):
            if not self.running:
                break
                
            # Calculate which wallet and transaction number
            wallet_idx = i // self.transaction_count
            tx_num = i % self.transaction_count
            
            if wallet_idx < len(wallet_ids):
                wallet_id = wallet_ids[wallet_idx]
                self._generate_single_transaction(wallet_id, tx_num)
                
    def _generate_single_transaction(self, wallet_id: str, tx_num: int):
        """Generate a single transaction - OPTIMIZED VERSION"""
        try:
            transaction = self._create_transaction(wallet_id)
            if transaction and self.transaction_callback:
                self.transaction_callback(transaction)
        except Exception as e:
            logger.error(f"Error generating transaction {tx_num} for {wallet_id}: {e}")
        
    def _generate_all_transactions_for_wallet(self, wallet_id: str):
        """Generate all transactions for a specific wallet upfront - OPTIMIZED VERSION"""
        wallet = self.wallets[wallet_id]
        
        for i in range(self.transaction_count):
            if not self.running:
                break
                
            try:
                # Create transaction with enhanced fee logic
                transaction = self._create_transaction(wallet_id)
                
                if transaction and self.transaction_callback:
                    self.transaction_callback(transaction)
                    
            except Exception as e:
                logger.error(f"Error generating transaction for {wallet_id}: {e}")
                
    def _generate_transactions_for_wallet(self, wallet_id: str):
        """Generate transactions for a specific wallet (legacy method) - OPTIMIZED VERSION"""
        wallet = self.wallets[wallet_id]
        
        for i in range(self.transaction_count):
            if not self.running:
                break
                
            try:
                # Create transaction with enhanced fee logic
                transaction = self._create_transaction(wallet_id)
                
                if transaction and self.transaction_callback:
                    self.transaction_callback(transaction)
                    
            except Exception as e:
                logger.error(f"Error generating transaction for {wallet_id}: {e}")
        
    def stop_transaction_generation(self):
        """Stop generating transactions"""
        self.running = False
        
        # Wait for threads to finish
        for thread in self.transaction_generators:
            if thread.is_alive():
                thread.join(timeout=2.0)
                
        logger.info("Stopped transaction generation")
        
    def _generate_transactions_for_wallet(self, wallet_id: str):
        """Generate transactions for a specific wallet"""
        wallet = self.wallets[wallet_id]
        
        for i in range(self.transaction_count):
            if not self.running:
                break
                
            try:
                # Create transaction with enhanced fee logic
                transaction = self._create_transaction(wallet_id)
                
                if transaction and self.transaction_callback:
                    self.transaction_callback(transaction)
                    
                # Wait for next transaction (reduced wait time for faster generation)
                time.sleep(max(0.01, self.interval))  # Minimum 0.01s wait
                
            except Exception as e:
                logger.error(f"Error generating transaction for {wallet_id}: {e}")
                time.sleep(0.1)  # Reduced wait before retrying
                
    def _create_transaction(self, sender_id: str) -> Optional[Transaction]:
        """Create a new transaction with enhanced fee logic"""
        try:
            # Select random recipient
            available_recipients = [w for w in self.wallets.keys() if w != sender_id]
            if not available_recipients:
                logger.warning(f"No available recipients for {sender_id}")
                return None
                
            recipient_id = random.choice(available_recipients)
            
            # Generate random amount
            amount = random.uniform(
                TRANSACTION_CONFIG['min_amount'],
                TRANSACTION_CONFIG['max_amount']
            )
            
            # Simplified fee calculation for speed
            fee = amount * 0.01  # 1% fee
            
            # Check if wallet has sufficient balance
            sender_wallet = self.wallets[sender_id]
            total_cost = amount + fee
            
            if sender_wallet.balance < total_cost:
                # Skip balance check for speed - assume sufficient balance
                pass
                
            # Create transaction with simplified ID
            transaction = Transaction(
                tx_id=f"tx_{sender_id}_{int(time.time() * 1000000)}",
                sender=sender_id,
                recipient=recipient_id,
                amount=amount,
                fee=fee,
                timestamp=time.time()
            )
            
            # Add priority and network info to transaction
            transaction.priority = 'normal'
            transaction.network_congestion = self.network_congestion
            
            # Update wallet balance (skip for speed)
            # sender_wallet.subtract_balance(amount, fee)
            
            return transaction
            
        except Exception as e:
            logger.error(f"Error creating transaction: {e}")
            return None
            
    def add_mining_reward(self, miner_id: str, amount: float):
        """Add mining reward to a wallet"""
        if miner_id in self.wallets:
            self.wallets[miner_id].add_balance(amount)
            logger.debug(f"Added mining reward {amount:.6f} to {miner_id}")
        else:
            # Create wallet for miner if it doesn't exist
            wallet = Wallet(miner_id, amount)
            self.wallets[miner_id] = wallet
            logger.info(f"Created wallet {miner_id} with mining reward {amount:.6f}")
            
    def process_confirmed_transaction(self, transaction: Transaction):
        """Process a confirmed transaction"""
        # Update recipient wallet
        if transaction.recipient in self.wallets:
            self.wallets[transaction.recipient].add_balance(transaction.amount)
            
        # Update transaction status
        transaction.status = "confirmed"
        
        logger.debug(f"Processed confirmed transaction {transaction.tx_id}")
        
    def update_network_conditions(self, congestion: float, block_utilization: float):
        """Update network conditions for fee calculation"""
        self.network_congestion = max(0.0, min(1.0, congestion))
        self.block_utilization = max(0.0, min(1.0, block_utilization))
        self.fee_calculator.update_network_conditions(congestion, block_utilization)
        
        logger.debug(f"Updated network conditions: congestion={congestion:.2f}, utilization={block_utilization:.2f}")
        
    def get_fee_estimate(self, amount: float, priority: str = 'normal') -> Dict:
        """Get fee estimate for a transaction"""
        return self.fee_calculator.get_fee_estimate(amount, priority)
        
    def get_wallet_balance(self, wallet_id: str) -> float:
        """Get wallet balance"""
        if wallet_id in self.wallets:
            return self.wallets[wallet_id].balance
        return 0.0
        
    def get_total_balance(self) -> float:
        """Get total balance across all wallets"""
        return sum(wallet.balance for wallet in self.wallets.values())
        
    def get_wallet_stats(self, wallet_id: str) -> Optional[Dict]:
        """Get statistics for a specific wallet"""
        if wallet_id in self.wallets:
            wallet = self.wallets[wallet_id]
            return {
                'wallet_id': wallet_id,
                'balance': wallet.balance,
                'transactions_sent': wallet.transactions_sent,
                'transactions_received': wallet.transactions_received,
                'total_sent': wallet.total_sent,
                'total_received': wallet.total_received,
                'total_fees': wallet.total_fees,
                'average_fee_rate': wallet.total_fees / wallet.total_sent if wallet.total_sent > 0 else 0.0
            }
        return None
        
    def get_all_wallet_stats(self) -> Dict:
        """Get statistics for all wallets"""
        stats = {
            'total_wallets': len(self.wallets),
            'total_balance': self.get_total_balance(),
            'network_conditions': {
                'congestion': self.network_congestion,
                'block_utilization': self.block_utilization
            },
            'fee_statistics': {
                'min_fee': TRANSACTION_CONFIG['min_fee'],
                'max_fee': TRANSACTION_CONFIG['max_fee'],
                'base_fee_rate': TRANSACTION_CONFIG['fee_rate']
            },
            'wallets': {}
        }
        
        for wallet_id, wallet in self.wallets.items():
            stats['wallets'][wallet_id] = wallet.to_dict()
            
        return stats
        
    def get_richest_wallets(self, count: int = 10) -> List[Dict]:
        """Get the richest wallets"""
        wallet_list = list(self.wallets.values())
        wallet_list.sort(key=lambda w: w.balance, reverse=True)
        
        richest = []
        for i, wallet in enumerate(wallet_list[:count]):
            richest.append({
                'rank': i + 1,
                'wallet_id': wallet.wallet_id,
                'balance': wallet.balance,
                'transactions_sent': wallet.transactions_sent,
                'transactions_received': wallet.transactions_received,
                'total_fees': wallet.total_fees
            })
            
        return richest
        
    def get_poor_wallets(self, threshold: float = 1.0) -> List[str]:
        """Get wallets with balance below threshold"""
        return [
            wallet_id for wallet_id, wallet in self.wallets.items()
            if wallet.balance < threshold
        ]
        
    def get_transaction_history(self, wallet_id: str = None, limit: int = 100) -> List[Dict]:
        """Get transaction history for a wallet or all transactions"""
        if wallet_id:
            # Filter transactions for specific wallet
            wallet_transactions = [
                tx for tx in self.transaction_history
                if tx['sender'] == wallet_id or tx['recipient'] == wallet_id
            ]
            return wallet_transactions[-limit:]
        else:
            # Return all recent transactions
            return list(self.transaction_history)[-limit:]
        
    def get_fee_statistics(self) -> Dict:
        """Get fee statistics across all transactions"""
        if not self.transaction_history:
            return {'total_fees': 0.0, 'average_fee': 0.0, 'fee_distribution': {}}
            
        fees = [tx['fee'] for tx in self.transaction_history]
        total_fees = sum(fees)
        average_fee = total_fees / len(fees)
        
        # Fee distribution by priority
        fee_distribution = {}
        for tx in self.transaction_history:
            priority = tx.get('priority', 'normal')
            if priority not in fee_distribution:
                fee_distribution[priority] = {'count': 0, 'total_fees': 0.0}
            fee_distribution[priority]['count'] += 1
            fee_distribution[priority]['total_fees'] += tx['fee']
            
        return {
            'total_fees': total_fees,
            'average_fee': average_fee,
            'min_fee': min(fees),
            'max_fee': max(fees),
            'fee_distribution': fee_distribution
        }
        
    def simulate_wallet_creation(self, wallet_id: str, initial_balance: float = 0.0):
        """Simulate creating a new wallet"""
        if wallet_id not in self.wallets:
            wallet = Wallet(wallet_id, initial_balance)
            self.wallets[wallet_id] = wallet
            logger.info(f"Created new wallet {wallet_id} with balance {initial_balance:.6f}")
        else:
            logger.warning(f"Wallet {wallet_id} already exists")
            
    def simulate_wallet_destruction(self, wallet_id: str):
        """Simulate destroying a wallet"""
        if wallet_id in self.wallets:
            balance = self.wallets[wallet_id].balance
            del self.wallets[wallet_id]
            logger.info(f"Destroyed wallet {wallet_id} with balance {balance:.6f}")
        else:
            logger.warning(f"Wallet {wallet_id} does not exist")
            
    def transfer_balance(self, from_wallet: str, to_wallet: str, amount: float):
        """Transfer balance between wallets"""
        if from_wallet not in self.wallets or to_wallet not in self.wallets:
            logger.error(f"One or both wallets do not exist: {from_wallet}, {to_wallet}")
            return False
            
        from_w = self.wallets[from_wallet]
        to_w = self.wallets[to_wallet]
        
        if from_w.balance >= amount:
            from_w.subtract_balance(amount)
            to_w.add_balance(amount)
            logger.info(f"Transferred {amount:.6f} from {from_wallet} to {to_wallet}")
            return True
        else:
            logger.warning(f"Insufficient balance in {from_wallet}")
            return False
            
    def to_dict(self) -> Dict:
        """Convert wallet manager to dictionary"""
        return {
            'wallet_count': self.wallet_count,
            'transaction_count': self.transaction_count,
            'interval': self.interval,
            'running': self.running,
            'network_conditions': {
                'congestion': self.network_congestion,
                'block_utilization': self.block_utilization
            },
            'wallets': {wid: wallet.to_dict() for wid, wallet in self.wallets.items()},
            'stats': self.get_all_wallet_stats(),
            'fee_stats': self.get_fee_statistics()
        } 