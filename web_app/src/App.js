import React, {Component} from 'react';
import './App.css'
import TitleHeader from './TitleHeader'
import StartStop from './StartStop';
import Game from './Game';
import Stats from './Stats';
import Vid from './Vid';
import './fonts/crackman/crackman back.ttf';
import './fonts/crackman/crackman front.ttf';
import './fonts/crackman/crackman.ttf';
import randommodel from './randommodel.mp4';
import okmodel from './80kSteps.mp4'
import medplot from './plots/Median Plot.png';
import rangeplot from './plots/Range Plot.png';


class App extends Component {
    constructor(props){
      super(props);
      this.state = {
          playing: false,
          score:0,
          //endpoint: 'http://localhost:8080',
          endpoint: window.location.href,
          avg_score: 0,
          avg_time: 0
      };
      this.clickStart = this.clickStart.bind(this);
      this.get_stats = this.get_stats.bind(this);
      //this.get_stats();
    }

    clickStart(){
      console.log('Start clicked');
      if(!this.state.playing){
          this.setState({
              score:'. . .'
          })
      }
      this.setState({
          playing: !this.state.playing
      });
      console.log(this.state.playing);
    }

    clickStop(){
        console.log('Stop clicked')
        window.location.reload(false);
    }

    get_stats(){
        fetch(this.state.endpoint + '/avg')
            .then(res => res.json())
            .then(res => {
                this.setState({
                    avg_time: res.avg_time.toFixed(2),
                    avg_score: res.avg_score.toFixed(2),
                    score: res.last_score})
            }).catch(err => console.log(err));
    }
    componentDidMount() {
        this.get_stats();
    }

    render() {
        return (
          <div className = 'main'>
            <div className = 'container'>
              <div className = 'row'>
                <TitleHeader />
              </div>
              <div className = 'row'>
                <StartStop onStart={this.clickStart} onStop = {this.clickStop} playing={this.state.playing} />
              </div>
              <div className = 'row justify-content-center'>
                  <div className = 'col col-md-7 text-center p-3'>
                      <Game playing={this.state.playing} endpoint = {this.state.endpoint}/>
                  </div>
                  <div className = 'col col-md-5 p-3'>
                      <Stats playing = {this.state.playing} endpoint = {this.state.endpoint } score = {this.state.score} avg_score = {this.state.avg_score} avg_time = {this.state.avg_time}/>
                  </div>
              </div>
                <div className = 'row justify-content-center'>
                    <div className = 'col-6'>
                        <img className = 'medplot' src = {medplot} alt = ''/>
                    </div>
                    <div className = 'col-6'>
                        <img className = 'medplot' src = {rangeplot} alt = ''/>
                    </div>
                </div>
              <div className = 'row justify-content-center p-4'>
                <div className = 'col col-4'>
                  <Vid title = 'Random Model' url = {randommodel}/>
                </div>
                <div className = 'col col-4'>
                  <Vid title = 'Trained 80k Steps' url = {okmodel}/>
                </div>
              </div>
            </div>
          </div>
        )
    }
}
export default App

      