import { writable } from 'svelte/store';
import { API, DEFAULT_TIMEOUT, sieve } from './api';
import { ResponseError, StatusError } from './error';
import Stock from './stock';
import timeout from './timeout';

export class User {
    static default = new User(null);

    constructor(name, properties) {
        this.name = name;
        this.selectedStocks = [];

        if (properties != null) {
            if (properties.selectedStocks != null) {
                this.selectedStocks = properties.selectedStocks;
            }
        }
    }

    logout() {
        document.cookie = 'token=';
        return User.default;
    }

    async buyStock(stock) {
        console.debug(`${this.name} buys ${stock.code}`);
        return sieve(timeout(
            DEFAULT_TIMEOUT,
            fetch(
                API + `/stock/buy?code="${stock.code}"`,
                { method: "POST" }
            )))
                .then(response => {
                    if (response.success) {
                        console.debug(`Stock ${stock} bought`);
                        this.selectedStocks.push(stock);
                        return response;
                    } else {
                        console.debug(`Failed to buy ${stock}`);
                        console.debug(response);
                        throw new ResponseError(response.reason);
                    }
                });
    }

    async sellStock(stock) {
        console.debug(`${this.name} sells ${stock.code}`);
        return sieve(timeout(
            DEFAULT_TIMEOUT,
            fetch(
                API + `/stock/sell?code="${stock.code}"`,
                { method: "POST" }
            )))
                .then(response => {
                    if (response.success) {
                        this.selectedStocks =
                            this.selectedStocks.filter(s => s.code != stock.code);
                    } else {
                        throw new ResponseError(response.reason);
                    }
                })
    }

    static async signup(name, password) {
        console.debug(`Signing up ${user}`);
        return sieve(fetch(API + '/user/signup', {
            method: 'POST',
            body: JSON.stringify({
                'name': name,
                'password': password
            })
        }))
            .then(response => {
                document.cookie = `token=${response.token}`;
                return new User(
                    response.user.name,
                    {
                        selectedStocks: response.user.stocks.map(
                            s => new Stock(s.code, s.price, s.organization)
                        )
                    }
                )
            })
    }

    static async login(name, password) {
        return sieve(fetch(API + '/user/login', {
            method: 'POST',
            body: JSON.stringify({
                'name': name,
                'password': password 
            })
        }))
            .then(response => {
                document.cookie = `token=${response.token}`;
                return new User(
                    response.user.name,
                    {
                        selectedStocks: response.user.stocks.map(
                            s => new Stock(s.code, s.price, s.organization)
                        )
                    }
                );
            })
    }

    static async authenticate() {
        console.debug('Authenticating user...');
        return sieve(timeout(DEFAULT_TIMEOUT, fetch(API + `/user/info`)))
            .then(response => new User(
                response.user.name, 
                {
                    selectedStocks: response.user.stocks.map(
                        s => new Stock(s.code, s.price, s.organization)
                    )
                }
            ));
    }
}

export const user = writable(User.default);
export const userPromise = User.authenticate()
    .then(u => {
        console.debug(u);
        user.update(() => u);
        return u;
    })
    .catch(error => {
        console.debug('Caught error...')
        console.debug(error);
        if (error.message != 'bad user token') {
            throw error;
        }
    });
