
import React from 'react';

class TextStack extends React.Component {
    render() {
        const textItems = ['Remote Job 1', 'Remote Job 2', 'Remote Job 3', 'Remote Job 4', 'Remote Job 5'];

        const itemStyle = {
            boxShadow: '0px 4px 8px 0px rgba(0, 0, 0, 0.2)',
            padding: '10px',
            margin: '10px 0',
            radius: '5px',
        };

        return (
            <div>
                {textItems.map((item, index) => (
                    <p key={index} style={itemStyle}>
                        {item}
                    </p>
                ))}
            </div>
        );
    }
}

export default TextStack;