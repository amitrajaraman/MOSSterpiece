import { Component, Input, OnInit } from '@angular/core';
import { SharedService } from 'src/app/shared.service';
import { MessengerService } from '../shared.service';
import { Router } from '@angular/router';
import { saveAs } from 'file-saver';
import { HttpResponse } from '@angular/common/http';

@Component({
  selector: 'app-file-upload',
  templateUrl: './file-upload.component.html',
  styleUrls: ['./file-upload.component.scss']
})


export class FileUploadComponent implements OnInit {

  zip: any;
  messages: string;
  download : boolean;
  constructor(private service:SharedService, private messengerService: MessengerService, private router: Router) { }

  ngOnInit(): void {
    this.zip = undefined;
    this.messengerService.message.subscribe(m => this.messages = m);
    this.download = false;
  }

  @Input() emp:any;
  ZipFileName:string;
  ZipPath:string;

  updateZip(event){
    this.zip = event;
  }

  Download(){
    this.service.downloadFile(this.ZipPath).subscribe(
      (blob)=> {
        console.log("downloaded");
        saveAs(blob, 'download.zip');
      },
      
      (error) => {console.log("failed")}
    )
  }
  uploadZip(){
    if(this.zip==undefined){
      window.alert("Please upload a zip file.");
    }
    else{
      var file = this.zip.target.files[0];
      const formdata: FormData=new FormData();
      formdata.append('file',file,file.name);

      this.service.UploadZip(formdata).subscribe(
        (data:any)=>{
        this.ZipFileName = data.file_name;
        this.ZipPath=this.service.ZipUrl+this.ZipFileName;
        window.alert("Uploaded Successfully!");
        console.log(this.ZipFileName);
        this.download = true;
      },
      (error) =>
      {
        console.log("upload failed");
      }
      )
      
     
    }
  }

}
