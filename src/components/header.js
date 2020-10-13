import React from "react";
import "./global.css";

function changeBackground(e) {
  e.target.style.color = '#4682B4';
}

function defaultColor(e){
  e.target.style.color = 'white';
}

export default () => {
  return(
    <>
    <div class="header">
    <div class="container">
            <a href="/aboutus" onMouseOver={changeBackground} onMouseLeave={defaultColor}>About Us</a>
            <a href='/signup' onMouseOver={changeBackground} onMouseLeave={defaultColor}>Sign Up</a>
            <a href="/login" onMouseOver={changeBackground} onMouseLeave={defaultColor}>Login</a>
    </div>
    <div class="title">MOSSterpiece
      </div>
</div>
    </>
  );
}
