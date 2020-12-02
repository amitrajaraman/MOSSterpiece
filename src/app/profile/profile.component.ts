import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MessengerService, SharedService } from '../shared.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {

  constructor(private messengerService: MessengerService, private router: Router, private service: SharedService) { }

  setGlobalValue(value: string) {
    this.messengerService.setMessage(value);
  }

  reroute_onLogout():void{
    this.service.logout().subscribe(
      (res)=> {
           window.alert("Logged out");
          this.setGlobalValue(""); 
         }
       );
     }
  

  ngOnInit(): void {
  }

}
