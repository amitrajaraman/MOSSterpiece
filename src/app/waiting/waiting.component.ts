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
  
  constructor(private service:SharedService, private resultservice:ResultService, public messengerService: MessengerService, private router: Router, private fileService: FileService) {
    this.filename="default";
    console.log(this.filename);
  }

  async ngOnInit(){
    this.filename = this.fileService.getMessage();
    // Waits for the processing to be completed
    await this.Process();
  }

  async Process(){
    const formdata: FormData = new FormData();
    formdata.append('file',this.filename);
    const t = await this.service.processFile(formdata).toPromise();
    var blob = new Blob([t]);
    //Set obtained data in messenger service
    this.resultservice.setMessage(blob);
    //reroute after process is done
    this.router.navigate(['/upload/view']);
      
  }

}
