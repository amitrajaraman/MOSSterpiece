import { Component, OnInit } from '@angular/core';
import { FileService, MessengerService, SharedService } from '../shared.service';
import { ResultService } from '../shared.service';
import { HttpClient } from '@angular/common/http';
import { FormGroup, FormControl, Validators} from '@angular/forms';
import { DomSanitizer } from '@angular/platform-browser';
import { saveAs } from 'file-saver';

@Component({
  selector: 'app-view-curr',
  templateUrl: './view-curr.component.html',
  styleUrls: ['./view-curr.component.scss']
})
export class ViewCurrComponent implements OnInit {
  result:any;
  max:any;
  values:string[];
  files:string[];
  filename: string;
  fileData: string;
  all_files:string[];
  all_values:any;
  pic1: any;
  pic2: any;
  rep:any;
  show:boolean;
  show_val:any;
  constructor(public resultService: ResultService, private sanitizer: DomSanitizer, public messengerService: MessengerService,public fileService: FileService, public resultservice: ResultService, private http:HttpClient, private service: SharedService) { }


  async ngOnInit() {
    this.fileData = '';
    this.unzipping();
  }

  unzipping()
  {
    const jsZip = require('jszip');
    const promises = [];
    let counter = 0;
    jsZip.loadAsync(this.resultservice.getMessage()).then((zip) => {

    
    zip.files["outpImg.png"].async('base64').then((fileData) => { 
          this.pic1 = this.sanitizer.bypassSecurityTrustUrl(
            'data:image/png;base64,' + fileData);
        });
    zip.files["outpHeatmap.png"].async('base64').then((fileData) => {
        this.pic2 = this.sanitizer.bypassSecurityTrustUrl(
            'data:image/png;base64,' + fileData);
        });
    Object.keys(zip.files).forEach(function (file) {
      if(file.split('.')[1]=="txt"){
        console.log(file);
        promises.push(zip.file(file).async("string"));
      }
    });
    var that = this;
    Promise.all(promises).then(function (data) {
      console.log("----------------------");
      that.result = data[0];
      console.log(that.result);
      that.max = data[1];
      that.proc();
    });
    
    });
  }
  

  form = new FormGroup({
    file1: new FormControl('', Validators.required),
    file2: new FormControl('', Validators.required),
  });

  get f(){
    return this.form.controls;
  }
  Download(){
    console.log("downloading...");
    let data = this.resultService.getMessage();
    console.log(data);
    const blob = new Blob([data]);
    const file = new File([blob], 'data.zip');
    saveAs(file); 
  }

  submit(){
    console.log(this.form.value.file1);
    console.log(this.form.value.file2);
    var i = this.all_files.indexOf(this.form.value.file1);
    var j = this.all_files.indexOf(this.form.value.file2);
    if(i==-1 || j==-1){
      this.show = false;
      window.alert("Please select the files!");
    }
    else{
      this.show = true;
      this.show_val = this.all_values[i][j];
    }
  }

  proc():void{
    var val = this.max.split("\n");
    this.values = val[0].split(",");
    this.files = val[1].split(",");
    this.rep = Array(this.values.length).fill(0).map((x,i)=>i);

    val = this.result.split("\n");
    this.all_files = val[0].split(",");

    this.all_values = new Array(this.all_files.length);

    for(let i=1; i<=this.all_files.length; i++){
      this.all_values[i-1] = val[i].split(",");
    }
  }
}