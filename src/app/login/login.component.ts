import { Component, OnDestroy, OnInit } from '@angular/core';
import { MessengerService, SharedService } from '../shared.service';
import { FormControl, FormGroup, Validators } from '@angular/forms';
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

  constructor(private service:SharedService, private router: Router, public messengerService: MessengerService) { }

  ngOnInit(): void {
    this.messageSubscription = this.messengerService.message.subscribe(m => { this.messages = m });
  }

  ngOnDestroy() {
    this.messageSubscription.unsubscribe();
  }

  setGlobalValue(value: string) {
    this.messengerService.setMessage(value);
  }

  reroute_onLogin(value: string):void{
    this.setGlobalValue(value);
    this.router.navigate(['/profile']);
  }

  login():void{
      var data = {
          username: this.form_username.value,
          password: this.form_password.value
        }
      if(this.messages==''){
        this.service.login(data).subscribe(
          (res)=>{
          console.log(res);
          window.alert("Logged in Successfully!");
          this.reroute_onLogin(res.token);
          this.messengerService.setName(res.user.first_name);
        },
        (error) => {
          window.alert("Incorrect Username/Password.");
          console.log(error);
          }
        );
      }
      else{
        window.alert("You are already logged in, please signout first.");
      }
      
  }

}