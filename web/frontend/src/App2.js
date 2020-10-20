import React, { Component } from 'react'
// import Datas from './datas'
import Ninjas from './Ninjas'

class App extends Component {
	state = {
		mainstream: [
			{'id':1, 'name': 'Alex', 'age': 47},
			{'id':2, 'name': 'Kevin', 'age': 17},
			{'id':3, 'name': 'Roger', 'age': 57},
		]
	}

	render(){

		return(
			<div className="app">
				<Ninjas data = {this.state.mainstream} />
			</div>
		);
	}
}

export default App;