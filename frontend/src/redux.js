import camelCaseKeys from 'camelcase-keys';
import {applyMiddleware, combineReducers, createStore} from 'redux';
import thunk from 'redux-thunk';

function generate(config) {
    let actions = {},
        reducers = {};

    Object.entries(config).forEach(item => {
        const key = item[0];

        let url = item[1];

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
            if (typeof url === 'function') {
                url = url(...query);
            }

            dispatch({type: actionTypes.start});

            return fetch(url).then(rep => rep.json()).then(
                (payload) => dispatch({
                    type: actionTypes.success,
                    payload: camelCaseKeys(payload, {deep: true})
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
    overview: '/api/overview'
});

const store = createStore(
    combineReducers(reducers),
    applyMiddleware(thunk)
);

export {actions, store};
