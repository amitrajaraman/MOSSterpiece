import { Component, Input, OnInit } from '@angular/core';
import { FileService, SharedService, ResultService } from 'src/app/shared.service';
import { MessengerService } from '../shared.service';
import { Router } from '@angular/router'

@Component({
  selector: 'app-waiting',
  templateUrl: './waiting.component.html',
  styleUrls: ['./waiting.component.scss']
})
export class WaitingComponent implements OnInit {
  filename:string;
  done:boolean;
  
  constructor(private service:SharedService, private resultservice:ResultService, public messengerService: MessengerService, private router: Router, private fileService: FileService) {
    this.filename="default";
    this.done = false;
    console.log(this.filename);
  }

  async ngOnInit(){
    // Waits for the processing to be completed
    if(!this.done){await this.Process();}
  }

  async Process(){
    this.filename = this.fileService.getMessage();
    const formdata = {"file": this.filename};
    const t = await this.service.processFile(formdata).toPromise();
    //reroute after process is done
    this.router.navigate(['/upload/view']);
    this.done=true;
  }

}