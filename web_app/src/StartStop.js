import React, {Component} from 'react';
import './StartStop.css';

class StartStop extends Component {
    constructor(props){
        super(props);
    
    }

    render(){
        if (this.props.playing){
            return (
                <div class = 'container'>
                    <div class='row justify-content-md-center p-3'>
                        <div class = 'col col-4 text-center'>
                            <button type="button" className="btn btn-secondary stop mr-1" onClick={this.props.onClick}>Stop Game</button>
                            <button type="button" className="btn btn-primary" onClick={this.props.onRefresh}>Restart Game </button>
                        </div>
                    </div>
                </div>
            )
        }
        else {
            return (
                <div class = 'container'>
                    <div class='row justify-content-md-center p-3'>
                        <div class = 'col col-2 text-center'>
                            <button type="button" class="btn btn-success start" onClick={this.props.onClick}>Start Game</button>
                        </div>
                    </div>
                </div>
            )
        }
    }

}

export default StartStop