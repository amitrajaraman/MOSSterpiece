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
  pic1: string;
  pic2: string;
  all_files:string[];
  all_values:any;
  rep:any;
  show:boolean;
  show_val:any;
  constructor(public messengerService: MessengerService,public fileService: FileService, public resultservice: ResultService, private http:HttpClient, private service: SharedService) { }

  async ngOnInit() {
    //Get the results from the data
    //this.result = this.resultservice.getMessage();
    let res = await this.service.viewFile("/results/outpImg.png").toPromise();
    this.pic1 = res.path
    res = await this.service.viewFile("/results/outpHeatmap.png").toPromise();
    this.pic2 = res.path;
    console.log(this.pic2);
    this.result = await this.http.get("../../../DjangoAPI/media/results/outpFile.txt");
    this.max = await this.http.get("../../../DjangoAPI/media/results/top.txt");
    console.log(this.max);
    // this.proc();
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
    console.log(this.fileService.getMessage());
    this.service.downloadFile(this.fileService.getMessage()).subscribe(
      (data:any)=> {
        // This is hack
        console.log("here");
        //  var blob = new Blob([data]);
        // console.log(blob);
        // saveAs(blob, 'download.zip');
      }

    );
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