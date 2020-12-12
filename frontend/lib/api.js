import timeout from './timeout';
import {StatusError, ResponseError} from './error';

export const DEFAULT_TIMEOUT = 3000;
export const API = '/api';

export function sieve(fetchPromise) {
    return fetchPromise
        .then(response => {
            console.debug('Fetch successful...');
            const contentType = response.headers.get('content-type');
            console.debug(`Content-Type received: ${contentType}`);

            if (!response.ok) {
                console.debug(`Response status code was ${response.status}`)
                throw new StatusError(
                    'Server returned error status',
                    response.status
                );
            }
            console.debug('Response passed safety checks...');

            return response;
        })
        .then(response => response.json())
        .then(body => {
            if (body.success === false) {
                throw new ResponseError(body.reason);
            }

            return body;
        })
}

export async function ping() {
    return timeout(DEFAULT_TIMEOUT, fetch(API + '/ping'));
}
