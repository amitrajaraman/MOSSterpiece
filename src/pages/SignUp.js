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
            <div class="h1">Sign Up Today!</div>
            <form action="register" method="post" class="form">
                <div class="section">
                    <label> First Name </label>
                    <input type="text" placeholder="First Name" required /><br />
                    <label> Last Name </label>
                    <input type="text" placeholder="Last Name" required /><br />
                    <label> Username </label>
                    <input type="text" placeholder="Username" required /><br />
                    <label> Email </label>
                    <input type="email" placeholder="abc@xyz.com" required /><br />
                    <label> Password </label>
                    <input type="password" placeholder="*********" required /><br />
                    <label> Confirm Password </label>
                    <input type="password" placeholder="*********" required /><br />
                    <button type="submit" onMouseOver={changeColor} onMouseLeave={defaultColor}>Submit</button>
                </div>
            </form>

        </>
    );
}