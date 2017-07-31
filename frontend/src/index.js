import React from 'react';
import ReactDOM from 'react-dom';

import './index.css';

fetch('/api/').then(
    rep => {
        console.log('fetch api success', rep);
    },
    err => {
        console.log('fetch api failed', err);
    }
);

ReactDOM.render(<div>Hello world</div>, document.getElementById('root'));
