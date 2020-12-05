import { Component, Input, OnInit } from '@angular/core';
import { FileService, SharedService } from 'src/app/shared.service';
import { MessengerService } from '../shared.service';
import { Router } from '@angular/router'

@Component({
  selector: 'app-waiting',
  templateUrl: './waiting.component.html',
  styleUrls: ['./waiting.component.scss']
})
export class WaitingComponent implements OnInit {
  filename:string;
  
  constructor(private service:SharedService, public messengerService: MessengerService, private router: Router, private fileService: FileService) {
    this.filename="default";
    console.log(this.filename);
  }

  ngOnInit(): void {
    this.filename = this.fileService.getMessage();
    
  }

  Process(){
    const formdata: FormData = new FormData();
    formdata.append('file',this.filename);
    this.service.processFile(formdata).subscribe(
      (data:any)=>{
        var blob = new Blob([data]);
        console.log(blob);
      },

      (error)=>{console.log("error")}
    )
  }

}
