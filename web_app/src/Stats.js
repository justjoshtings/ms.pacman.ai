import React, {Component} from 'react'
import './Stats.css'

class Stats extends Component {
    constructor(props){
        super(props);
    }

    render(){
        endpoint = window.location.href
        return (
            <div class = 'container'>
                <img className = 'statsimg' src={endpoint+"/stats"}/>
            </div>
        )
    }

}

export default Stats