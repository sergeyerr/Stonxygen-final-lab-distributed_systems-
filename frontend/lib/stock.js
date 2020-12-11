import { API, DEFAULT_TIMEOUT, moderateResponse } from './api';
import timeout from './timeout';

export default class Stock {
    constructor(code, price, organization, statistic) {
        this.code = code;
        this.price = price;
        this.organization = organization;
        this.statistic = statistic;
    }

    static allAvailable() {
        return timeout(DEFAULT_TIMEOUT, fetch(API + '/stock/list'))
            .then(moderateResponse)
            .then(response => response.json())
            .then(response => response.stocks)
            .then(stocks =>
                stocks.map(s => new Stock(s.code, s.price, s.organization))
            );
    }

    async variance() {
        return "?";
    }
}
