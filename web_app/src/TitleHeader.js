import React, {Component} from 'react';
import './TitleHeader.css';
import pacman from './mspacmanlogo.jpeg'
// import './fonts/crackman/crackman.ttf';

class TitleHeader extends Component {

    render(){
        return (
            <div className = 'container'>
                <div className = 'row p-3'>
                    <div className = 'col-3'>
                        <img className='logo' src = {pacman}/>
                    </div>
                    <div className = 'col-9'>
                        <p className = 'display-4'><span className='text-center words dqn'>DQN </span> <span className = 'agent'> Agent Plays </span> <span className = 'words pacman'> Ms.Pacman</span></p>
                    </div>
                </div>
            </div>
        )
    }

}

export default TitleHeader