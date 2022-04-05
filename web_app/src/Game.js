import React, {Component} from 'react';
import './Game.css';
import basegame from './startscreen.png';

class Game extends Component {
    constructor(props){
        super(props);
        this.state = {
            score: null,
            gameUrl: null
        };
        this.getFrames = this.getFrames.bind(this);
        this.validateRes = this.validateRes.bind(this);
        this.test = this.test.bind(this);
    }

    getScore() {
        console.log('getting score??')
        fetch(this.props.endpoint + '/score')
            .then(res => res.json())
            .then(res => {
                this.setState({
                    score: res.score
                })
            }).catch(err => console.log(err));

        return this.state.score
    }

    validateRes(response){
        if(!response.ok){
            throw Error(response.statusText);
        }
        return response
    }
    test() {
        console.log('testing score??')
        fetch(this.props.endpoint + '/results')
            .then(res => console.log(res))
            .catch(err => console.log(err));
    }

    getFrames() {
        console.log('getting frames maybe')
        fetch(this.props.endpoint + '/results')
            .then(response => response.blob())
            .then(res => console.log(res))
    }


    render(){
        console.log('rendered....')

        if (this.props.playing) {
            return (
            <div className = 'container'>
                <img className = 'game' src={this.props.endpoint + '/results'} alt = '' />
            </div>
            )
        }
        else {
            return (
            <div className = 'container'>
                <img className = 'basegame' src={basegame} alt = '' />
            </div>
            )
        }
    }
}

export default Game