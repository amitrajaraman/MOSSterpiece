import { Component, Input, OnInit } from '@angular/core';
import { FileService, SharedService, ResultService } from 'src/app/shared.service';
import { MessengerService } from '../shared.service';
import { Router, NavigationEnd } from '@angular/router'
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-waiting',
  templateUrl: './waiting.component.html',
  styleUrls: ['./waiting.component.scss']
})
export class WaitingComponent implements OnInit {
  filename:string;
  
  constructor(private http:HttpClient, private service:SharedService, public resultservice:ResultService, public messengerService: MessengerService, private router: Router, private fileService: FileService) {
    this.filename="default";
    console.log(this.filename);
    // this.router.events.subscribe((e) => {
    //    if (e instanceof NavigationEnd) {
    //     this.filename = this.fileService.getMessage();  
    //     this.Process();
    //    }
    // });
  }
  //  ngOnInit(): void{}
  async ngOnInit(){
    this.filename = this.fileService.getMessage();
    // Waits for the processing to be completed
    await this.Process();
  }
  async Process(){
    const formdata: FormData = new FormData();
    formdata.append('file',this.filename);
    const t = await this.service.processFile(formdata).toPromise();
    console.log(this.filename);
    var res = await this.http.get('../../assets/results/outpFile.txt', {responseType: 'text'}).toPromise();
    var max = await this.http.get('../../assets/results/top.txt', {responseType: 'text'}).toPromise();
    this.resultservice.setmax(max);
    this.resultservice.setres(res);
    //reroute after process is done
    this.router.navigate(['/upload/view']);
      
  }

}
