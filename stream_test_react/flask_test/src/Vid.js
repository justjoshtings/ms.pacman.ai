import React, {Component} from 'react'
import './Vid.css'
import basegame from './basegame.png'

class Vid extends Component {
    constructor(props){
        super(props);
    }


    render(){
        return (
            <div class = 'container'>
                <img className = 'basegame' src={basegame}/>
                <div class = 'textoverimage'>{this.props.title}</div>
            </div>
        )
    }
}

export default Vid