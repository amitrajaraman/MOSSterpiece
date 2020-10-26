import { Component, Input, OnInit } from '@angular/core';
import { HttpEventType, HttpErrorResponse } from '@angular/common/http';
import { of } from 'rxjs';  
import { catchError, map } from 'rxjs/operators';  
import { UploadService } from  '../file-upload.service';
import {SharedService} from 'src/app/shared.service';

@Component({
  selector: 'app-file-upload',
  templateUrl: './file-upload.component.html',
  styleUrls: ['./file-upload.component.scss']
})


export class FileUploadComponent implements OnInit {

  constructor(private service:SharedService) { }

  ngOnInit(): void {
  }

  @Input() emp:any;
  ZipFileName:string;
  ZipPath:string;

  uploadZip(event){
    var file = event.target.files[0];
    const formdata: FormData=new FormData();
    formdata.append('uploadedFile',file,file.name);

    this.service.UploadZip(formdata).subscribe((data:any)=>{
      this.ZipFileName = data.toString();
      this.ZipPath=this.service.ZipUrl+this.ZipFileName;
    })
  }

}
