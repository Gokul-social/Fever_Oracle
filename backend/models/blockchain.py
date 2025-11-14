"""
Blockchain service for enhanced data security and privacy
Provides immutable audit logging, data integrity verification, and privacy-preserving features
"""

from datetime import datetime
from typing import Dict, List, Optional
import hashlib
import json

class BlockchainNode:
    """Represents a single block in the blockchain"""
    
    def __init__(self, data: Dict, previous_hash: str = None):
        self.timestamp = datetime.now().isoformat()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
        self.nonce = 0
    
    def calculate_hash(self) -> str:
        """Calculate SHA-256 hash of the block"""
        block_string = json.dumps({
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int = 2):
        """Proof of Work - mine the block"""
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
    
    def to_dict(self) -> Dict:
        """Convert block to dictionary"""
        return {
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash,
            'hash': self.hash,
            'nonce': self.nonce
        }


class Blockchain:
    """Blockchain implementation for audit logging and data integrity"""
    
    def __init__(self, difficulty: int = 2):
        self.chain: List[BlockchainNode] = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.pending_transactions: List[Dict] = []
    
    def create_genesis_block(self) -> BlockchainNode:
        """Create the first block in the chain"""
        return BlockchainNode({
            'type': 'genesis',
            'message': 'Fever Oracle Blockchain Initialized',
            'version': '1.0.0'
        }, "0")
    
    def get_latest_block(self) -> BlockchainNode:
        """Get the most recent block"""
        return self.chain[-1]
    
    def add_block(self, data: Dict) -> BlockchainNode:
        """Add a new block to the chain"""
        previous_hash = self.get_latest_block().hash
        new_block = BlockchainNode(data, previous_hash)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        return new_block
    
    def add_audit_log(self, event_type: str, user_id: str, action: str, 
                     resource: str, metadata: Optional[Dict] = None) -> BlockchainNode:
        """Add an audit log entry to the blockchain"""
        audit_data = {
            'type': 'audit_log',
            'event_type': event_type,
            'user_id': user_id,
            'action': action,
            'resource': resource,
            'metadata': metadata or {},
            'timestamp': datetime.now().isoformat()
        }
        return self.add_block(audit_data)
    
    def add_data_hash(self, data_id: str, data_hash: str, data_type: str) -> BlockchainNode:
        """Store data integrity hash on blockchain"""
        integrity_data = {
            'type': 'data_integrity',
            'data_id': data_id,
            'data_hash': data_hash,
            'data_type': data_type,
            'timestamp': datetime.now().isoformat()
        }
        return self.add_block(integrity_data)
    
    def verify_chain(self) -> bool:
        """Verify the integrity of the blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Verify current block hash
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Verify previous hash link
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True
    
    def get_audit_trail(self, user_id: Optional[str] = None, 
                       resource: Optional[str] = None) -> List[Dict]:
        """Get audit trail from blockchain"""
        audit_logs = []
        for block in self.chain:
            if block.data.get('type') == 'audit_log':
                if user_id and block.data.get('user_id') != user_id:
                    continue
                if resource and block.data.get('resource') != resource:
                    continue
                audit_logs.append(block.to_dict())
        return audit_logs
    
    def get_chain_info(self) -> Dict:
        """Get blockchain information"""
        return {
            'chain_length': len(self.chain),
            'is_valid': self.verify_chain(),
            'latest_hash': self.get_latest_block().hash,
            'difficulty': self.difficulty
        }


class PrivacyBlockchain:
    """Privacy-preserving blockchain with zero-knowledge features"""
    
    def __init__(self, blockchain: Blockchain):
        self.blockchain = blockchain
    
    def create_zk_proof(self, data: Dict) -> Dict:
        """Create a zero-knowledge proof for data (simplified implementation)"""
        # In production, this would use actual ZK-SNARKs or ZK-STARKs
        data_hash = hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()
        return {
            'proof_hash': data_hash,
            'timestamp': datetime.now().isoformat(),
            'type': 'zk_proof'
        }
    
    def verify_zk_proof(self, proof: Dict, expected_hash: str) -> bool:
        """Verify a zero-knowledge proof"""
        return proof.get('proof_hash') == expected_hash
    
    def add_encrypted_audit(self, encrypted_data: str, user_id: str) -> BlockchainNode:
        """Add encrypted audit log to blockchain"""
        audit_data = {
            'type': 'encrypted_audit',
            'encrypted_data': encrypted_data,
            'user_id': user_id,
            'timestamp': datetime.now().isoformat()
        }
        return self.blockchain.add_block(audit_data)


# Global blockchain instance
blockchain = Blockchain(difficulty=2)
privacy_blockchain = PrivacyBlockchain(blockchain)

