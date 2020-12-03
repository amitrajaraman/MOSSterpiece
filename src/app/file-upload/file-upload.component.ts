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
  ZipName:string;

  updateZip(event){
    this.zip = event;
  }

  Download(){
    this.service.downloadFile(this.ZipFileName).subscribe(
      (data)=> {
        // This is hack
        window.open(data, "_blank");
        //  var blob = new Blob([data]);
        // console.log(blob);
        // saveAs(blob, 'download.zip');
      },
      
      (error) => {console.log("failed")}
    )
  }

  //For now, assume that the uploaded stuff is right. tl;dr open folder, take inputs, pass to Amit's .py file
  Process(){
    this.ZipPath = this.service.ZipUrl;
    const formdata: FormData = new FormData();
    formdata.append('file',this.ZipFileName);
    this.service.processFile(formdata).subscribe(
      (data:any)=>{
        var blob = new Blob([data]);
        console.log(blob);
      },

      (error)=>{console.log("error")}
    )
  }

  uploadZip(){
    //This doesn't work! able to upload non-zip as well!
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
        //Need to work on regex lol
        this.ZipName = this.ZipFileName.replace(/(.*_\s*)[^_.]*(.[a-zA-Z0-9]*$)/,"");
        window.alert("Uploaded Successfully!");
        console.log(this.ZipName);
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
