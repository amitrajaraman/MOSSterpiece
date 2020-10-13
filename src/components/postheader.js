import React from "react";
import "../components/global.css";

function changeBackground(e) {
  e.target.style.color = '#4682B4';
}

function defaultColor(e){
  e.target.style.color = 'white';
}

function LogOut(){
  if(window.confirm("Are you sure you want to log out?")){
    window.location.href = "/";
  }
}


export default () => {
  return(
    <div class="header">
    <div class="container">
            <a href="/postlogin/profile" onMouseOver={changeBackground} onMouseLeave={defaultColor}>Profile</a>
            <a href='/postlogin/upload' onMouseOver={changeBackground} onMouseLeave={defaultColor}>Upload</a>
            <a href="/postlogin/view" onMouseOver={changeBackground} onMouseLeave={defaultColor}>View Previous Results</a>
            <span style={{paddingLeft:"50px"}}onMouseOver={changeBackground} onMouseLeave={defaultColor} onClick={LogOut}>Log Out</span>
    </div>
    <div class="title">MOSSterpiece</div>
</div>

  );
}