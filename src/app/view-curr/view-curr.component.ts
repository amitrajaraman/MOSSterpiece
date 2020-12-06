import { Component, OnInit } from '@angular/core';
import { MessengerService } from '../shared.service';
import { ResultService } from '../shared.service';
import { HttpClient } from '@angular/common/http';
import { FormGroup, FormControl, Validators} from '@angular/forms';
import { Router,NavigationEnd } from '@angular/router';

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
  constructor(private router: Router, public messengerService: MessengerService, public resultservice: ResultService, private http:HttpClient) 
  {}
  // ngOnInit(): void{}
  async ngOnInit() {
    //Get the results from the data
    //this.result = this.resultservice.getMessage();
    //console.log(this.result);

    //Read the results csv file
    this.result = this.resultservice.getres();
    this.max = this.resultservice.getmax();
    this.proc();
  }

  form = new FormGroup({
    file1: new FormControl('', Validators.required),
    file2: new FormControl('', Validators.required),
  });

  get f(){
    return this.form.controls;
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
