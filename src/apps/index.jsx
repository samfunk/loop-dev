import React from 'react';
import createReactClass from 'create-react-class';
import ReactDOM from 'react-dom';


class Tester extends React.Component {
  render() {
    return (
        <h1>TestingThis!</h1>
    );
  }
}

const render = function() {
    ReactDOM.render(<Tester/>, app);
}

render();
