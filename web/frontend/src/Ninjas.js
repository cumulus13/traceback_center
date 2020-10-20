import React, { Component } from 'react';

class Ninjas extends Component{


	render(){
		// const mainstream = this.props;
		const { data } = this.props;
		const  dataList = data.map(x => {
			return(
				<div className="ninjas" key= {x.id}>
				<div>
					<p>name = {x.name}</p>
					<p>age = {x.age}</p>
				</div>
			</div>
			)
		})
		// console.log(mainstream);
		return(
			<div className="result">
			{ dataList }
			</div>	
		);	
	}
}

export default Ninjas;