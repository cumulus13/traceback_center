// App.js
import React, { Component } from 'react';
import Table from './table';
import Search from './search';
// import Main from './main';

class App extends Component {
  // constructor(props){
    // super(props)
    // this.state = {
    //   tracebacks: []
    // }
    state = {
      tracebacks: [],
      logs: [
        {'id': 222, 'age':55, 'hobby':'hack'}
      ]
    };
  // }
/* 
   This is where the magic happens
*/
  
  async componentDidMount() {
    try {
      const res = await fetch('http://127.0.0.1:4000/getall', {
        // headers: {
        //   'Content-Type':'application/json',
        // }
      }); // fetching the data from api, before the page loaded
      console.log(res);
      
      const datas = await res.json();
      console.log(datas);
      this.setState({
        tracebacks:datas 
      });
      console.log("TRACEBACK =", this.state.tracebacks)
    } catch (e) {
      console.log(e);
    }
  }

  render() {
    return (
      <div className="App">
      <Search />
      <Table tracebacks={ this.state.tracebacks} logs={this.state.logs}/>
      </div>
    );
  }
}

export default App;

// <Table tracebacks={ this.state.tracebacks} logs={this.state.logs}/>

// <Table tracebacks={ this.state.tracebacks} logs={this.state.logs}/>