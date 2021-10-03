import * as React from 'react'
import {useRef, useEffect} from 'react';

const Canvas = props => {
    const draw = (ctx, props) => {
        for (var i = 0; i < props.data.length; i++) {
            for (var j = 0; j < props.data[i].length; j++) {
                var c = props.data[i][j];
                ctx.fillStyle = `rgb(${c}, ${c}, ${c})`;
                ctx.fillRect(j, i, 1, 1);
            }
        }


    }

    const canvas_ref = useRef(null);
    console.log(canvas_ref.current)
    useEffect(() => {draw(canvas_ref.current.getContext('2d'), props)}, [draw]);

    return <canvas width={props.w} height={props.h} className={props.canvasClass} ref={canvas_ref}/>
}

export default Canvas;
