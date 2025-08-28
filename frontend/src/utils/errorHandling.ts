// Centralized error handling for API calls

export interface ApiError {
  message: string;
  type: 'cors' | 'network' | 'server' | 'deployment' | 'unknown';
  details?: string;
  retryable: boolean;
}

export const analyzeApiError = (error: any): ApiError => {
  // CORS error detection
  if (error.message?.includes('CORS') || error.message?.includes('Access-Control-Allow-Origin')) {
    return {
      message: 'Backend deployment in progress',
      type: 'cors',
      details: 'The backend service is updating. Please wait 2-3 minutes and try again.',
      retryable: true
    };
  }

  // Network/fetch errors
  if (error.message?.includes('Failed to fetch') || error.name === 'TypeError') {
    return {
      message: 'Backend service unavailable',
      type: 'deployment',
      details: 'The backend service may be deploying or temporarily unavailable. This usually resolves in 2-3 minutes.',
      retryable: true
    };
  }

  // Server errors (500, 502, 503, 504)
  if (error.status >= 500 && error.status < 600) {
    return {
      message: 'Backend service error',
      type: 'server',
      details: `Server returned ${error.status}. The service may be restarting.`,
      retryable: true
    };
  }

  // Client errors (400-499)
  if (error.status >= 400 && error.status < 500) {
    return {
      message: 'Request error',
      type: 'server',
      details: `Error ${error.status}: ${error.statusText || 'Bad request'}`,
      retryable: false
    };
  }

  // Generic network error
  return {
    message: 'Connection error',
    type: 'network',
    details: error.message || 'Unable to connect to backend service',
    retryable: true
  };
};

export const getRetryDelay = (attemptCount: number): number => {
  // Exponential backoff: 2s, 4s, 8s, 16s, then 30s
  const delays = [2000, 4000, 8000, 16000, 30000];
  return delays[Math.min(attemptCount, delays.length - 1)];
};

export const formatErrorForUser = (error: ApiError): string => {
  let message = error.message;
  
  if (error.details) {
    message += `\n\n${error.details}`;
  }
  
  if (error.retryable) {
    message += '\n\n🔄 Retrying automatically...';
  }
  
  return message;
};