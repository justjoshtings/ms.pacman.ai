import React, {Component} from 'react'
import './Game.css'
import basegame from './basegame.png'

class Game extends Component {
    constructor(props){
        super(props);
    }


    render(){
        console.log('rendered....')
        console.log('props -- ' + this.props.playing)
        if (this.props.playing) {
            return (
            <div class = 'container'>
                <img className = 'game' src="http://192.168.0.181:8080/results"/>
            </div>
            )
        }
        else {
            return (
            <div class = 'container'>
                <img className = 'basegame' src={basegame}/>
                <div class = 'textoverimage'>Press Start Game</div>
            </div>
            )
        }
    }
}

export default Game