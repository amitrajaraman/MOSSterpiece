import { Component, OnInit } from '@angular/core';
import { MessengerService } from '../shared.service';
import { ResultService } from '../shared.service';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-view-curr',
  templateUrl: './view-curr.component.html',
  styleUrls: ['./view-curr.component.scss']
})
export class ViewCurrComponent implements OnInit {
  result:Blob;
  constructor(public messengerService: MessengerService, public resultservice: ResultService, private http:HttpClient) { }

  ngOnInit(): void {
    //Get the results from the data
    this.result = this.resultservice.getMessage();
    console.log(this.result);

    //Read the results csv file
    this.http.get('../../assets/results/outpFile.csv', {responseType: 'text'})
        .subscribe(data => console.log(data));
  }

}
