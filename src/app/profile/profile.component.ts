import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MessengerService, SharedService } from '../shared.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
/**Just your basic profile page with your name and some buttons to push */
export class ProfileComponent implements OnInit {
  /**to store the name of the user */
  user:string;
  constructor(public messengerService: MessengerService, private router: Router, private service: SharedService) {  }

  ngOnInit():void{
    this.user = this.messengerService.getName();
  }
  
  setGlobalValue(value: string) {
    this.messengerService.setMessage(value);
  }
  /**to log out when this button is pressed */
  reroute_onLogout():void{
    this.service.logout().subscribe(
      (res)=> {
           window.alert("Logged out");
          this.setGlobalValue("");
         }
       );
     }

}
