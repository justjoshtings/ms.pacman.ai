import React, {Component} from 'react'
import './Stats.css'

class Stats extends Component {
    constructor(props){
        super(props);
        this.state = {
            endpoint: 'http://localhost:8080',
            score: this.props.score
        }
    }

    render(){
        var endpoint = window.location.href;
        var endpoint = 'http://localhost:8080'
        return (
            <div class = 'container'>
                {/*<img className = 'statsimg' src={endpoint+"/stats"} />*/}
                <div className = 'row justify-content-start'>
                    <p className = 'score'>SCORE: {this.props.score}</p>
                </div>
                <div className = 'row justify-content-start pastScores'>
                    <p className='score'>Average Model Score: </p>
                </div>

            </div>
        )
    }

}

export default Stats