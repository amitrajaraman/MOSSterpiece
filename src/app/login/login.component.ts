import { Component, OnDestroy, OnInit } from '@angular/core';
import { MessengerService, SharedService } from '../shared.service';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { LoginUser } from '../User';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})

export class LoginComponent implements OnInit, OnDestroy {

  private messageSubscription: Subscription;
  public messages: string;
  form_username = new FormControl('');
  form_password = new FormControl('');

  constructor(private service:SharedService, private router: Router, private messengerService: MessengerService) { }

  ngOnInit(): void {
    this.messageSubscription = this.messengerService.message.subscribe(m => { this.messages = m });
  }

  ngOnDestroy() {
    this.messageSubscription.unsubscribe();
  }

  setGlobalValue(value: string) {
    this.messengerService.setMessage(value);
  }

  reroute_onLogin():void{
    LoginUser.user = this.form_username.value;
    this.setGlobalValue(this.form_username.value);
    this.router.navigate(['/upload']);
  }

  login():void{
      var data = {
          username: this.form_username.value,
          password: this.form_password.value
        }
        if(LoginUser.user==""){
        this.service.login(data).subscribe(
          (res)=>{
          console.log(res);
          window.alert("Login Works!");
          this.reroute_onLogin();
        },
        (error) => {
          console.log("This is backend problem")
          }
        );
      }
      else{
        window.alert("You are already logged in as "+LoginUser.user+", please signout first.");
      }
      
  }

}