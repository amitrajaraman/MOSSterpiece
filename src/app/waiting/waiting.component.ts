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
  zip: string;
  constructor(private service:SharedService, private resultService:ResultService, public messengerService: MessengerService, private router: Router, private fileService: FileService) {  }

  async ngOnInit(){
    this.Process();
  }

  Process(){
    this.zip = this.fileService.getMessage();
    if(this.zip==undefined){
      window.alert("Please upload a zip file.")
    }
    else{
      const formdata = {"file": this.zip};
      this.service.processFile(formdata).subscribe(
        (res)=>
        {
          const blob = new Blob([res], {
            type: 'application/zip'
          });
          this.resultService.setMessage(blob);
          // console.log(blob);
          // const file = res["body"];
          // console.log(file);
          this.router.navigate(['/upload/view']);
        },
      );

    }
  }
}