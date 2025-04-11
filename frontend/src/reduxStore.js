import { configureStore } from '@reduxjs/toolkit';
import { createInjectorsEnhancer, forceReducerReload } from 'redux-injectors';
import createSagaMiddleware from 'redux-saga';
import createReducer from 'reducers';
import rootSaga from 'rootSaga';

function configureAppStore(initialState = {}) {
    const reduxSagaMonitorOptions = {};
    const sagaMiddleware = createSagaMiddleware(reduxSagaMonitorOptions);
    const { run: runSaga } = sagaMiddleware;

    const middlewares = [sagaMiddleware];

    const enhancers = [
        createInjectorsEnhancer({
            createReducer,
            runSaga,
        }),
    ];

    const store = configureStore({
        reducer: createReducer(),
        middleware: (getDefaultMiddleware) => getDefaultMiddleware().concat(middlewares),
        enhancers: (getDefaultEnhancers) => getDefaultEnhancers().concat(enhancers),
        preloadedState: initialState,
        devTools: {
            shouldHotReload: false,
        },
    });

    if (module.hot) {
        module.hot.accept('./reducers', () => {
            forceReducerReload(store);
        });
    }

    sagaMiddleware.run(rootSaga);
    return store;
}

export const store = configureAppStore();
