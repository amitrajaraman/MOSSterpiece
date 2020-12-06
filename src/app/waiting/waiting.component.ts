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
  
  constructor(private service:SharedService, private resultservice:ResultService, public messengerService: MessengerService, private router: Router, private fileService: FileService) {  }

  async ngOnInit(){
    this.Process();
  }

  async Process(){
    this.filename = this.fileService.getMessage();
    if(this.filename!=""){
      const formdata = {"file": this.filename};
      const t = await this.service.processFile(formdata).toPromise();
    }
    //reroute after process is done
    this.router.navigate(['/upload/view']);
  }
}