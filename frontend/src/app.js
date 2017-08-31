import React from 'react';
import {BrowserRouter, Route, Switch} from 'react-router-dom';

import Album from './components/album';
import Albums from './components/albums';
import Artist from './components/artist';
import Artists from './components/artists';
import Navigation from './components/navigation';
import NotFound from './components/not-found';
import Overview from './components/overview';
import Plays from './components/plays';
import Track from './components/track';
import Tracks from './components/tracks';

import './app.css';

class App extends React.Component {
    render() {
        return (
            <div>
                <BrowserRouter>
                    <div>
                        <Route path="/:path" component={Navigation} />
                        <div className="app-content">
                            <Switch>
                                <Route exact path="/" component={Overview} />
                                <Route exact path="/artists" component={Artists} />
                                <Route exact path="/artists/:id" component={Artist} />
                                <Route exact path="/albums" component={Albums} />
                                <Route exact path="/albums/:id" component={Album} />
                                <Route exact path="/tracks" component={Tracks} />
                                <Route exact path="/tracks/:id" component={Track} />
                                <Route exact path="/plays" component={Plays} />
                                <Route component={NotFound}/>
                            </Switch>
                        </div>
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
