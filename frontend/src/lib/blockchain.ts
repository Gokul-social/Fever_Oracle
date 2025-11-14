/**
 * Blockchain API client
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

export interface BlockchainInfo {
  chain_length: number;
  is_valid: boolean;
  latest_hash: string;
  difficulty: number;
}

export interface AuditLog {
  timestamp: string;
  data: {
    type: string;
    event_type: string;
    user_id: string;
    action: string;
    resource: string;
    metadata?: Record<string, any>;
  };
  hash: string;
  previous_hash: string;
}

class BlockchainClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async fetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options?.headers,
        },
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || `API error: ${response.status} ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      // Handle network errors
      if (error instanceof TypeError && error.message.includes('fetch')) {
        console.error(`Blockchain API request failed: Network error - ${endpoint}`, error);
        throw new Error('Network error: Unable to connect to blockchain service. Please check if the backend is running.');
      }
      console.error(`Blockchain API request failed: ${endpoint}`, error);
      throw error;
    }
  }

  async getBlockchainInfo(): Promise<BlockchainInfo> {
    return this.fetch<BlockchainInfo>('/api/blockchain/info');
  }

  async getAuditTrail(userId?: string, resource?: string): Promise<{ audit_logs: AuditLog[]; count: number }> {
    const params = new URLSearchParams();
    if (userId) params.append('user_id', userId);
    if (resource) params.append('resource', resource);
    const query = params.toString() ? `?${params.toString()}` : '';
    return this.fetch<{ audit_logs: AuditLog[]; count: number }>(`/api/blockchain/audit-trail${query}`);
  }

  async verifyBlockchain(): Promise<{ is_valid: boolean; chain_length: number }> {
    return this.fetch<{ is_valid: boolean; chain_length: number }>('/api/blockchain/verify');
  }

  async addAuditLog(eventType: string, userId: string, action: string, resource: string, metadata?: Record<string, any>) {
    return this.fetch('/api/blockchain/audit', {
      method: 'POST',
      body: JSON.stringify({
        event_type: eventType,
        user_id: userId,
        action,
        resource,
        metadata,
      }),
    });
  }
}

export const blockchainClient = new BlockchainClient();
export default blockchainClient;

