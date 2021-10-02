import * as React from 'react'
import {useRef, useEffect} from 'react';

const Canvas = props => {
    const draw = (ctx, props) => {
        for (var i = 0; i < props.data.length; i++) {
            for (var j = 0; j < props.data[i].length; j++) {
                var c = props.data[i][j];
                ctx.fillStyle = `rgb(${c}, ${c}, ${c})`;
                ctx.fillRect(props.w * j, props.h * i, props.w, props.h);
            }
        }
    }

    const canvas_ref = useRef(null);
    useEffect(() => {draw(canvas_ref.current.getContext('2d'), props)}, [draw]);

    return <canvas ref={canvas_ref}/>
}

export default Canvas;
