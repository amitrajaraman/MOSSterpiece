import { Component, Input, OnInit } from '@angular/core';
import { FileService, ResultService, SharedService } from 'src/app/shared.service';
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
  download : boolean;
  constructor(private resultService: ResultService, private service:SharedService, public messengerService: MessengerService, private router: Router, private fileService: FileService) { }

  ngOnInit(): void {
    this.zip = undefined;
    this.download = false;
  }

  @Input() emp:any;
  ZipFileName:string;
  ZipPath:string;
  ZipName:string;

  updateZip(event){
    this.zip = event;
  }


  //For now, assume that the uploaded stuff is right. tl;dr open folder, take inputs, pass to Amit's .py file
  Process(){
    if(this.zip==undefined){
      window.alert("Please upload a zip file.");
    }
    this.router.navigate(['/upload/waiting']);
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
        this.fileService.setMessage(this.ZipFileName);
        window.alert("Uploaded Successfully!");
        this.download = true;
      },
      (error) =>
      {
        console.log("upload failed");
      }
      );
      
     
    }
  }

}