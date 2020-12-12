export class TimeoutError extends Error {}

export class APIError extends Error {}
export class StatusError extends APIError {
    constructor(message, code) {
        super(message);
        this.code = code;
    }
}
export class ResponseError extends Error {}
