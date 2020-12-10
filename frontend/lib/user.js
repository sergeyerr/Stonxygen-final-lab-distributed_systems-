import { writable } from 'svelte/store';
import { API, DEFAULT_TIMEOUT, moderateResponse } from './api';
import { StatusError } from './error';
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
        return timeout(
            DEFAULT_TIMEOUT,
            fetch(API + `/stock/buy?code="${stock.code}"`)
                .then(moderateResponse)
                .then(response => response.json())
                .then(response => {
                    if (response.success) {
                        this.selectedStocks.push(stock);
                        return response;
                    } else {
                        throw new Error(response.message);
                    }
                })
        );
    }

    static async signup(name, password) {
        return fetch(API + '/user/signup', {
            method: 'POST',
            headers: {
                'name': name,
                'password': password
            }
        })
            .then(moderateResponse)
            .then(response => response.json())
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
        return fetch(API + '/user/login', {
            method: 'POST',
            headers: {
                'name': name,
                'password': password 
            }
        })
            .then(moderateResponse)
            .then(response => response.json())
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
        return timeout(DEFAULT_TIMEOUT, fetch(API + `/user/info`))
            .then(moderateResponse)
            .then(response => response.json())
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
        user.update(() => u);
        return u;
    })
    .catch(error => {
        if (!(error instanceof StatusError) || error.code !== 403) {
            throw error;
        }
    });
