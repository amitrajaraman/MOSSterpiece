import React from "react";
import "../components/global.css";
import Header from "../components/header";

function changeColor(e) {
    e.target.style.background = '#4682B4';
  }
  
  function defaultColor(e){
    e.target.style.background = ' rgb(20, 16, 56)';
  }

export default () => {
    return (
    <>
        <Header />
        <div class="h1">Welcome back!</div>
        <form action="login" method="post" class="form">
        <div class = "section">
            <label> Username </label>
            <input type="text" name="username" placeholder="Username" required/>
            <label> Password </label>
            <input type="password" name="password" placeholder="Password" required/><br/>
            <button type="submit" onMouseOver={changeColor} onMouseLeave={defaultColor}>Login</button>
        </div>
        </form>
    </>
    );
}