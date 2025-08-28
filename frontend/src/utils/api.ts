import { analyzeApiError, getRetryDelay, type ApiError } from './errorHandling';

// API configuration utility
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const apiUrl = (endpoint: string): string => {
  // Remove leading slash if present to avoid double slashes
  const cleanEndpoint = endpoint.startsWith('/') ? endpoint.slice(1) : endpoint;
  return `${API_BASE_URL}/${cleanEndpoint}`;
};

export const apiConfig = {
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
};

// Enhanced fetch with retry logic and better error handling
export const apiFetch = async (
  endpoint: string, 
  options: RequestInit = {}, 
  maxRetries = 3
): Promise<Response> => {
  const url = apiUrl(endpoint);
  
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          ...apiConfig.headers,
          ...options.headers,
        },
      });

      // If successful, return response
      if (response.ok) {
        return response;
      }

      // If it's a server error and we have retries left, retry
      if (response.status >= 500 && attempt < maxRetries) {
        await new Promise(resolve => setTimeout(resolve, getRetryDelay(attempt)));
        continue;
      }

      // For other errors, throw with response info
      throw {
        status: response.status,
        statusText: response.statusText,
        message: `HTTP ${response.status}: ${response.statusText}`
      };

    } catch (error: any) {
      const apiError = analyzeApiError(error);
      
      // If retryable and we have retries left, wait and retry
      if (apiError.retryable && attempt < maxRetries) {
        console.log(`API call failed (attempt ${attempt + 1}/${maxRetries + 1}):`, apiError.message);
        await new Promise(resolve => setTimeout(resolve, getRetryDelay(attempt)));
        continue;
      }

      // If no more retries, throw the analyzed error
      throw apiError;
    }
  }

  throw new Error('Max retries exceeded');
};
