import React, {Component} from 'react'
import './Stats.css'

class Stats extends Component {
    constructor(props){
        super(props);
        this.state = {
            score: this.props.score,
            avg_time: 0,
            avg_score: 0
        }
        this.get_stats = this.get_stats.bind(this);
    }

    get_stats(){
        console.log(this.props.endpoint)
        fetch(this.props.endpoint + '/avg')
            .then(res => res.json())
            .then(res => {
                console.log(res)
                this.setState({
                    avg_time: res.avg_time.toFixed(2),
                    avg_score: res.avg_score.toFixed(2)})
            }).catch(err => console.log(err));
    }

    render(){

        return (
            <div className = 'container box'>
                <div className = 'row justify-content-start'>
                    <div className = "col">
                        <p className = 'score'>LATEST SCORE: <span className="num">{this.props.score}</span></p>
                    </div>
                </div>
                <div className = 'row justify-content-start'>
                    <p className='score'>Average Model Score: <span className="num">{this.props.avg_score}</span> points</p>
                    <p className='score'>Average Time Alive: <span className="num">{this.props.avg_time}</span> seconds</p>
                </div>

            </div>
        )
    }

}

export default Stats