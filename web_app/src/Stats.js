import React, {Component} from 'react'
import './Stats.css'

class Stats extends Component {
    constructor(props){
        super(props);
    }

    render(){
        return (
            <div class = 'container'>
                <img className = 'statsimg' src="http://192.168.0.181:8080/stats"/>
            </div>
        )
    }

}

export default Stats