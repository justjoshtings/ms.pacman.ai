import React, {Component} from 'react'
import './Game.css'
import basegame from './startscreen.png'
import {useEffect, useState} from 'react'

class Game extends Component {
    constructor(props){
        super(props);
        this.state = {
            endpoint: 'http://localhost:8080',
            score: null,
            gameUrl: null
        };
       // this.getScore = this.getScore.bind(this);
        this.getFrames = this.getFrames.bind(this);
        this.validateRes = this.validateRes.bind(this);
        this.test = this.test.bind(this);
    }

    getScore() {
        console.log('getting score??')
        fetch(this.state.endpoint + '/score')
            .then(res => res.json())
            .then(res => {
                // console.log(res)
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
        fetch(this.state.endpoint + '/results')
            .then(res => console.log(res))
            .catch(err => console.log(err));
    }
    getFrames() {
        console.log('getting frames maybe')
        fetch(this.state.endpoint + '/results')
            .then(this.validateRes)
            .then(response => response.blob())
            .then(blob => {
                this.setState({gameUrl: URL.createObjectURL(blob)})
            })
    }


    render(){
        console.log('rendered....')
        console.log('props -- ' + this.props.playing)
        var endpoint = window.location.href;
        var endpoint = 'http://localhost:8080'

        if (this.props.playing) {
            return (
            <div class = 'container'>
                <img className = 'game' src={endpoint + '/results'} />
            </div>
            )
        }
        else {
            return (
            <div class = 'container'>
                <img className = 'basegame' src={basegame} />
            </div>
            )
        }
    }
}

export default Game