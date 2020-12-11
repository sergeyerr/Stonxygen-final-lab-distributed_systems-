import timeout from './timeout';
import { APIError, StatusError, TimeoutError } from './error';

export const DEFAULT_TIMEOUT = 3000;
export const API = 'http://localhost:3000/api';

export function moderateResponse(response) {
    if (!response.ok) {
        throw new StatusError('Server returned error status', response.status)
    }

    const contentType = response.headers.get('content-type')
    if (!contentType.includes('application/json')) {
        throw new APIError('Content Mismatch');
    }

    return response;
}

export async function ping() {
    return timeout(DEFAULT_TIMEOUT, fetch(API + '/ping'));
}
