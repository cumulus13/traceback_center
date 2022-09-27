class App extends React.Component {
  
    state = {
      tracebacks: [],
      traceback_type: []
    };
  
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

      const t_type = await fetch('http://127.0.0.1:4000/gettracebacktype', {});
      const traceback_type = await t_type.json();
      console.log(traceback_type);
      this.setState({
        tracebacks:datas ,
        traceback_type:traceback_type
      });
      // console.log("TRACEBACK =", this.state.tracebacks)
    } catch (e) {
      console.log(e);
    }
  }

  render() {
    console.log("TRACEBACKS = ", this.state.tracebacks)
    return (
      <div className="App">
        <Table tracebacks={ this.state.tracebacks} traceback_type = {this.state.traceback_type} />
      </div>
    );
  }
}

ReactDOM.render(<App />, document.getElementById('app'));



