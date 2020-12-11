import timeout from './timeout';
import { APIError, StatusError, ResponseError } from './error';

export const DEFAULT_TIMEOUT = 3000;
export const API = new URL(document.URL).origin + '/api';

export function sieve(fetchPromise) {
    return fetchPromise
        .then(response => {
            const contentType = response.headers.get('content-type')
            if (!contentType.includes('application/json')) {
                console.log(contentType);
                throw new APIError('Content Mismatch');
            }

            if (!response.ok) {
                throw new StatusError(
                    'Server returned error status',
                    response.status
                );
            }

            return response;
        })
        .then(response => response.json())
        .then(body => {
            console.log(body);
            if (body.success === false) {
                throw new ResponseError(body.reason);
            }

            return body;
        })
}

export async function ping() {
    return timeout(DEFAULT_TIMEOUT, fetch(API + '/ping'));
}
