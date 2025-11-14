"""
Blockchain service API endpoints
"""

from flask import Blueprint, jsonify, request
from models.blockchain import blockchain, privacy_blockchain
from datetime import datetime

blockchain_bp = Blueprint('blockchain', __name__)

@blockchain_bp.route('/api/blockchain/info', methods=['GET'])
def get_blockchain_info():
    """Get blockchain information"""
    try:
        # Ensure blockchain is initialized
        if not blockchain.chain:
            blockchain.chain = [blockchain.create_genesis_block()]
            blockchain._cache_valid = False  # Reset cache
        
        info = blockchain.get_chain_info()
        return jsonify(info)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            "error": str(e),
            "chain_length": len(blockchain.chain) if blockchain.chain else 0,
            "is_valid": False
        }), 500

@blockchain_bp.route('/api/blockchain/audit', methods=['POST'])
def add_audit_log():
    """Add an audit log entry to blockchain"""
    try:
        data = request.get_json()
        event_type = data.get('event_type', 'unknown')
        user_id = data.get('user_id', 'anonymous')
        action = data.get('action', '')
        resource = data.get('resource', '')
        metadata = data.get('metadata', {})
        
        block = blockchain.add_audit_log(event_type, user_id, action, resource, metadata)
        return jsonify({
            "success": True,
            "block": block.to_dict()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@blockchain_bp.route('/api/blockchain/audit-trail', methods=['GET'])
def get_audit_trail():
    """Get audit trail from blockchain"""
    try:
        user_id = request.args.get('user_id')
        resource = request.args.get('resource')
        
        audit_logs = blockchain.get_audit_trail(user_id, resource)
        return jsonify({
            "audit_logs": audit_logs,
            "count": len(audit_logs)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@blockchain_bp.route('/api/blockchain/verify', methods=['GET'])
def verify_blockchain():
    """Verify blockchain integrity"""
    try:
        is_valid = blockchain.verify_chain()
        return jsonify({
            "is_valid": is_valid,
            "chain_length": len(blockchain.chain)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@blockchain_bp.route('/api/blockchain/data-hash', methods=['POST'])
def add_data_hash():
    """Store data integrity hash on blockchain"""
    try:
        data = request.get_json()
        data_id = data.get('data_id')
        data_hash = data.get('data_hash')
        data_type = data.get('data_type', 'unknown')
        
        block = blockchain.add_data_hash(data_id, data_hash, data_type)
        return jsonify({
            "success": True,
            "block": block.to_dict()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@blockchain_bp.route('/api/blockchain/zk-proof', methods=['POST'])
def create_zk_proof():
    """Create a zero-knowledge proof"""
    try:
        data = request.get_json()
        proof = privacy_blockchain.create_zk_proof(data)
        return jsonify({
            "success": True,
            "proof": proof
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

