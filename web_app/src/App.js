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
        playing: false
      };
      this.clickStart = this.clickStart.bind(this);
    }

    clickStart(){
      console.log('Start clicked')
      this.setState({
          playing: !this.state.playing
      });
      console.log(this.state.playing);
    }

    render() {
        return (
          <div class = 'main'>
            <div class = 'container'>
              <div class = 'row'>
                <TitleHeader />
              </div>
              <div class = 'row'>
                <StartStop onClick={this.clickStart} playing={this.state.playing}></StartStop>
              </div>
              <div class = 'row justify-content-center'>
                  <div class = 'col col-md-5 text-center p-3'>
                      <Game playing={this.state.playing} />
                  </div>
                  <div class = 'col col-md-5 text-center p-3'>
                      <Stats />
                  </div>
              </div>
              <div class = 'row justify-content-center p-4'>
                <div class = 'col'>
                  <Vid title = 'vid1'/>
                </div>
                <div class = 'col'>
                  <Vid title = 'vid2'/>
                </div>
                <div class = 'col'>
                  <Vid title = 'vid3'/>
                </div>
              </div>
            </div>
          </div>
        )
    }
}
export default App

      