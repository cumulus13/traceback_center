import React, { Component } from 'react';


class Search extends Component{
	// constructor(props){
	// 	super(props)
	// }

	render(){
		return(
			<div className="search">
				<table id="table_search">
					<tr>
						<td>Search</td>
						<td>:</td>
						<td><input type="text" id="text_search" /></td>
						<td><input type="button" id="bt_search" value="Search"/></td>
					</tr>
				</table>
			</div>
		)
	}
}

export default Search;