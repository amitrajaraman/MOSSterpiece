import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MessengerService, SharedService } from '../shared.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {
  user:string;
  constructor(public messengerService: MessengerService, private router: Router, private service: SharedService) {  }

  //A very bad way of getting the user's data; too bad!
  ngOnInit():void{
    //if all else fails, send a get req to backend and get username
    this.user = this.messengerService.getName();
  }

  setGlobalValue(value: string) {
    this.messengerService.setMessage(value);
  }

  reroute_onLogout():void{
    this.service.logout().subscribe(
      (res)=> {
           window.alert("Logged out");
          this.setGlobalValue("");
          // sessionStorage. 
         }
       );
     }

}
