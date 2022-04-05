import React, {Component} from 'react';
import './Vid.css';
import ReactPlayer from "react-player";

class Vid extends Component {

    render(){
        return (
            <div className = 'container row text-center'>
                <div className = 'title'>{this.props.title}</div>
                <ReactPlayer url = {this.props.url} controls = {true} width = '100%'/>
            </div>
        )
    }
}

export default Vid