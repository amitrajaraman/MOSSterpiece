import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MessengerService, SharedService } from '../shared.service';

@Component({
  selector: 'app-pre-header',
  templateUrl: './pre-header.component.html',
  styleUrls: ['./pre-header.component.scss']
})
export class PreHeaderComponent implements OnInit {

  messages: string;
  /**
   * Mostly simple css and html that route to different pages, 
   * also has log out functionality after a user has logged in
   * @param messengerService 
   * @param router 
   * @param service 
   */
  constructor(public messengerService: MessengerService, private router: Router, private service: SharedService) { }
  /**Sets global value to user parameters to use in other places e.g. profile */
  setGlobalValue(value: string) {
    this.messengerService.setMessage(value);
  }
  /**Reroutes to landing page if this button is pressed, invokes log out */
  reroute_onLogout():void{
     this.service.logout().subscribe(
       (res)=> {
            window.alert("Logged out");
           this.setGlobalValue(""); 
          }
        );
      }


  ngOnInit(): void {
    this.messengerService.message.subscribe(m => this.messages = m);
  }

}
