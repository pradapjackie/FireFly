import React from 'react';
import { Provider } from 'react-redux';
import { Router, Switch, Route } from 'react-router-dom';
import history from './history';
import Layout from 'components/Layout';
import GlobalTheme from 'styles/GlobalTheme/GlobalTheme';
import GlobalCss from 'styles/GlobalCss';
import { store } from 'reduxStore';
import { sessionRoutes } from './routes/session';
import AuthGuard from './containers/auth/AuthGuard';
import { CustomSuspense } from './components/CustomSuspense';

const App = () => (
    <Provider store={store}>
        <GlobalTheme>
            <GlobalCss />
            <Router history={history}>
                <CustomSuspense>
                    <Switch>
                        {sessionRoutes.map((item, i) => (
                            <Route key={i} path={item.path} component={item.component} />
                        ))}
                        <AuthGuard>
                            <CustomSuspense>
                                <Layout />{' '}
                            </CustomSuspense>
                        </AuthGuard>
                    </Switch>
                </CustomSuspense>
            </Router>
        </GlobalTheme>
    </Provider>
);

export default App;
