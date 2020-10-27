import { Component, Input, OnInit } from '@angular/core';
import { HttpEventType, HttpErrorResponse } from '@angular/common/http';
import { of } from 'rxjs';  
import { catchError, map } from 'rxjs/operators';  
import { UploadService } from  '../file-upload.service';
import { SharedService } from 'src/app/shared.service';
import { MessengerService } from '../shared.service';
import { Router } from '@angular/router';


@Component({
  selector: 'app-file-upload',
  templateUrl: './file-upload.component.html',
  styleUrls: ['./file-upload.component.scss']
})


export class FileUploadComponent implements OnInit {

  zip: any;
  messages: string;

  constructor(private service:SharedService, private messengerService: MessengerService, private router: Router) { }

  ngOnInit(): void {
    this.zip = undefined;
    this.messengerService.message.subscribe(m => this.messages = m);
  }

  @Input() emp:any;
  ZipFileName:string;
  ZipPath:string;

  updateZip(event){
    this.zip = event;
  }

  uploadZip(){
    if(this.zip==undefined){
      window.alert("Please upload a zip file.");
    }
    else{
      var file = this.zip.target.files[0];
      const formdata: FormData=new FormData();
      formdata.append('uploadedFile',file,file.name);

      this.service.UploadZip(formdata).subscribe((data:any)=>{
        this.ZipFileName = data.toString();
        this.ZipPath=this.service.ZipUrl+this.ZipFileName;
      })

      window.alert("Uploaded Successfully!");
    }
  }

}
