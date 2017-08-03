import React from 'react';
import {BrowserRouter, Route, Switch} from 'react-router-dom';

import Navigation from './components/navigation';
import NotFound from './components/not-found';
import Overview from './components/overview';

import './app.css';

class App extends React.Component {
    render() {
        return (
            <div>
                <BrowserRouter>
                    <div>
                        <Route path="/:path" component={Navigation} />
                        <Switch>
                            <Route exact path="/" component={Overview} />
                            <Route component={NotFound}/>
                        </Switch>
                    </div>
                </BrowserRouter>
                <div className="app-footer">
                    Development and support &mdash; Ross Nomann, 2017
                </div>
            </div>
        );
    }
}

export default App;
