import humps from 'humps';
import {applyMiddleware, combineReducers, createStore} from 'redux';
import thunk from 'redux-thunk';

import {buildURL} from './utils';

function generate(config) {
    let actions = {},
        reducers = {};

    Object.entries(config).forEach(item => {
        const [key, maybeUrl] = item;

        const actionTypes = {
            start: `${key}_START`,
            success: `${key}_SUCCESS`,
            failed: `${key}_FAILED`
        };

        const initialState = {
            loaded: false,
            success: null,
            payload: null
        };

        actions[`${key}Request`] = (...query) => dispatch => {
            let url = typeof maybeUrl === 'function' ? maybeUrl(...query) : maybeUrl;

            dispatch({type: actionTypes.start});

            return fetch(url).then(rep => {
                const json = rep.json();
                return rep.status === 200 ? json : json.then(err => {
                    throw err;
                });
            }).then(
                (payload) => dispatch({
                    type: actionTypes.success,
                    payload: humps.camelizeKeys(payload, {deep: true})
                }),
                (payload) => dispatch({
                    type: actionTypes.failed,
                    payload
                })
            );
        };

        reducers[key] = (state = initialState, {type, payload}) => {
            switch (type) {
                case actionTypes.start:
                    state = initialState;
                    break;
                case actionTypes.success:
                    state = {
                        loaded: true,
                        success: true,
                        payload
                    };
                    break;
                case actionTypes.failed:
                    state = {
                        loaded: true,
                        success: false,
                        payload
                    };
                    break;
                default:
                    break;
            }
            return state;
        };

    });

    return {actions, reducers};
}

const {actions, reducers} = generate({
    artists: params => buildURL('/api/artists', params),
    counters: '/api/counters',
    overview: '/api/overview'
});

const store = createStore(
    combineReducers(reducers),
    applyMiddleware(thunk)
);

export {actions, store};
