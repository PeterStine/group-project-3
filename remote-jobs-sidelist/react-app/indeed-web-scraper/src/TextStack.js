
import React from 'react';

class TextStack extends React.Component {
    render() {
        const textItems = ['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5'];

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