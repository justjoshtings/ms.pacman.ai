import React, {Component} from 'react';
import './StartStop.css';

class StartStop extends Component {

    render(){
        if (this.props.playing){
            return (
                <div className = 'container'>
                    <div className='row justify-content-md-center p-3'>
                        <div className = 'col col-4 text-center'>
                            <button type="button" className="btn btn-secondary stop mr-1" onClick={this.props.onStop}>Stop Game</button>
                        </div>
                    </div>
                </div>
            )
        }
        else {
            return (
                <div className = 'container'>
                    <div className='row justify-content-md-center p-3'>
                        <div className = 'col col-2 text-center'>
                            <button type="button" className="btn btn-success start" onClick={this.props.onStart}>Start Game</button>
                        </div>
                    </div>
                </div>
            )
        }
    }

}

export default StartStop