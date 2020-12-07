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

  ngOnInit(){
    this.Process();
  }

  Process(){
    this.filename = this.fileService.getMessage();
    const formdata = {"file": this.filename};
    console.log(formdata);
    this.service.processFile(formdata).subscribe(
    (t)=>
    {
      console.log(t);
      //reroute after process is done
      // this.router.navigate(['/upload/view']);
    }
    );
  }
}