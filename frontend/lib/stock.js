import { API, DEFAULT_TIMEOUT, sieve } from './api';
import timeout from './timeout';

export default class Stock {
    constructor(code, price, organization, statistic) {
        this.code = code;
        this.price = price;
        this.organization = organization;
    }

    static allAvailable() {
        return timeout(DEFAULT_TIMEOUT, sieve(fetch(API + '/stock/list')))
            .then(response => response.stocks)
            .then(stocks =>
                stocks.map(s => new Stock(s.code, s.price, s.organization))
            );
    }

    async statistic() {
        timeout(DEFAULT_TIMEOUT, sieve(
            fetch(API + `/stock/statistic?code=${this.code}`)
        ))
    }
}
