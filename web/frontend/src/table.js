import React, { Component } from 'react'

class Table extends Component {
   constructor(props) {
      super(props) //since we are extending class Table so we have to use super in order to override Component class constructor
      this.state = { //state is by default an object
         students: [
            { id: 1, name: 'Wasif', age: 21, email: 'wasif@email.com' },
            { id: 2, name: 'Ali', age: 19, email: 'ali@email.com' },
            { id: 3, name: 'Saad', age: 16, email: 'saad@email.com' },
            { id: 4, name: 'Asad', age: 25, email: 'asad@email.com' }
         ],

         severity: [
            {'error': 'red'},
            {'alert': 'green'},
            {'emergency': 'magenta'},
            {'debug': 'orange'},
            {'info': 'black'},
            {'notice': 'cyan'},
            {'critical': 'blue'}
         ],

         headers: [
            { date: '', host: '', traceback: '', type: '', value: '' },
         ]
      }
   }

   re_color = (id, date, host, tb, tp, vl) => {
      const { traceback_type } = this.props;
      var ttype = null
      var color = null
      // console.log("traceback_type =", traceback_type);
      traceback_type.forEach((x) => {
         if (JSON.stringify(vl).includes(x.name)){
            ttype = x.name
            color = x.color
         }
      });
      if(ttype){
         return (
            <tr key={id} id="severity" className={color}>
               <td>{date}</td>
               <td>{host}</td>
               <td>{tb}</td>
               <td>{tp}</td>
               <td>{vl}</td>
            </tr>
         )
      }
   }
      
   showData() {
      const {tracebacks} = this.props;
      return tracebacks.map((x) => {
         const { id, date, host, tb, tp, vl } = x //destructuring
         return(
            this.re_color(id, date, host, tb, tp, vl)
         )
      })
   }

   setHeader() {
      let header = Object.keys(this.state.headers[0])
      return header.map((key, index) => {
         return <th key={index}>{key.toUpperCase()}</th>
      })
   }

   renderTableData() {
      return this.state.students.map((student, index) => {
         const { id, name, age, email } = student //destructuring
         return (
            <tr key={id}>
               <td>{id}</td>
               <td>{name}</td>
               <td>{age}</td>
               <td>{email}</td>
            </tr>
         )
      })
   }

   renderTableHeader() {
      let header = Object.keys(this.state.students[0])
      return header.map((key, index) => {
         return <th key={index}>{key.toUpperCase()}</th>
      })
   }

   render() {
      return (
         <div className='tracebacks'>
            <h1 id='title'>Traceback Logs</h1>
            <table id='students'>
               <tbody>
                  <tr className="header" id='header'>{ this.setHeader() }</tr>
                  { this.showData() }
               </tbody>
            </table>
         </div>
      )
   }

}

export default Table //exporting a component make it reusable and this is the beauty of react