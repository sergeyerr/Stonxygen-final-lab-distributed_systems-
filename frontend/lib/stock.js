import { API, DEFAULT_TIMEOUT, sieve } from './api';
import timeout from './timeout';

export default class Stock {
    constructor(code, price, organization, statistic) {
        this.code = code;
        this.price = price;
        this.organization = organization;
        this.statisticValue = "?"
    }

    static allAvailable() {
        console.debug('Fetching all available stocks...');
        return timeout(DEFAULT_TIMEOUT, sieve(fetch(API + '/stock/list')))
            .then(response => response.stocks)
            .then(stocks =>
                stocks.map(s => new Stock(s.code, s.price, s.organization))
            );
    }

    async statistic() {
        console.debug(`Fetching statistic for ${this.code}`);
        this.statisticPromise = sieve(timeout(DEFAULT_TIMEOUT, 
            fetch(API + `/stock/statistic?code=${this.code}`)
        ))

        return this.statisticPromise;
    }
}
