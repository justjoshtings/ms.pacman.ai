import React, {Component} from 'react';
import './TitleHeader.css';
import pacman from './mspacmanlogo.jpeg'
// import './fonts/crackman/crackman.ttf';

class TitleHeader extends Component {
    constructor(props){
        super(props);
    }

    render(){
        return (
            <div class = 'container'>
                <div class = 'row p-3'>
                    <div class = 'col-3'>
                        <img class='logo' src = {pacman}/>
                    </div>
                    <div class = 'col-9'>
                        <p class = 'display-4'><span class='text-center words dqn'>DQN </span> <span class = 'agent'> Agent Plays </span> <span class = 'words pacman'> Ms.Pacman</span></p>
                    </div>
                </div>
            </div>
        )
    }

}

export default TitleHeader