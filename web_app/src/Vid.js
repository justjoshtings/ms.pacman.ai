import React, {Component} from 'react';
import './Vid.css';
import basegame from './basegame.png';
import ReactPlayer from "react-player";
import Player from 'react';

class Vid extends Component {
    constructor(props){
        super(props);
    }


    render(){
        return (
            <div class = 'container row text-center'>
                <div className = 'title'>{this.props.title}</div>
                <ReactPlayer url = {this.props.url} controls = {true} width = '100%'/>
            </div>
        )
    }
}

export default Vid