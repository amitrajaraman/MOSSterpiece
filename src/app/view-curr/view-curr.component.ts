import { Component, OnInit } from '@angular/core';
import { FileService, MessengerService, SharedService } from '../shared.service';
import { ResultService } from '../shared.service';
import { HttpClient } from '@angular/common/http';
import { FormGroup, FormControl, Validators} from '@angular/forms';

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
  all_files:string[];
  all_values:any;
  rep:any;
  show:boolean;
  show_val:any;
  constructor(public messengerService: MessengerService,public fileService: FileService, public resultservice: ResultService, private http:HttpClient, private service: SharedService) { }

  async ngOnInit() {
    //Get the results from the data
    //this.result = this.resultservice.getMessage();
    //console.log(this.result);

    //Read the results csv file
    console.log("cammmmeeee heerereee");
    this.result = await this.http.get('../../assets/results/outpFile.txt', {responseType: 'text'}).toPromise();
    this.max = await this.http.get('../../assets/results/top.txt', {responseType: 'text'}).toPromise();
    
    this.proc();
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
    this.service.downloadFile(this.fileService.getMessage()).subscribe(
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