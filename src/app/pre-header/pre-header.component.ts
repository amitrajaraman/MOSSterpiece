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
    this.messengerService.message.subscribe(m => this.messages = m);
  }

}
