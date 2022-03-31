import React, {Component} from 'react';
import './App.css'
import { useEffect } from 'react';
import TitleHeader from './TitleHeader'
import StartStop from './StartStop';
import { useState } from 'react';
import axios from 'axios';
import Game from './Game';
import Stats from './Stats';
import Vid from './Vid';
import './fonts/crackman/crackman back.ttf';
import './fonts/crackman/crackman front.ttf';
import './fonts/crackman/crackman.ttf';


class App extends Component {
    constructor(props){
      super(props);
  
      this.state = {
          playing: false,
          score:0,
          endpoint: 'http://localhost:8080'
      };
      this.clickStart = this.clickStart.bind(this);
      this.handleStream = this.handleStream.bind(this);
      this.sse = null;
      this.refresh = this.refresh.bind(this);
    }

    clickStart(){
      console.log('Start clicked');
      if(!this.state.playing){
          this.setState({
              score:0
          })
      }
      this.setState({
          playing: !this.state.playing
      });
      console.log(this.state.playing);
    }

    refresh(){
        window.location.reload(false);
    }

    handleStream(e){
        console.log(e.data)
        this.setState({score:e.data})
    }

    componentDidMount() {
        console.log('mounted and started listening to stream')
        console.log(this.state.endpoint)
        const sse = new EventSource(this.state.endpoint + '/scorestream')
        sse.onmessage = e => this.handleStream(e)
        this.sse = sse
    }

    render() {
        return (
          <div className = 'main'>
            <div className = 'container'>
              <div className = 'row'>
                <TitleHeader />
              </div>
              <div className = 'row'>
                <StartStop onClick={this.clickStart} onRefresh = {this.refresh} playing={this.state.playing} />
              </div>
              <div className = 'row justify-content-center'>
                  <div className = 'col col-md-7 text-center p-3'>
                      <Game playing={this.state.playing} />
                  </div>
                  <div className = 'col col-md-5 text-center p-3'>
                      <Stats playing = {this.state.playing} score = {this.state.score}/>
                  </div>
              </div>
              <div className = 'row justify-content-center p-4'>
                <div className = 'col'>
                  <Vid title = 'vid1'/>
                </div>
                <div className = 'col'>
                  <Vid title = 'vid2'/>
                </div>
                <div className = 'col'>
                  <Vid title = 'vid3'/>
                </div>
              </div>
            </div>
          </div>
        )
    }
}
export default App

      