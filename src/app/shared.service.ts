import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SharedService {
  readonly APIUrl = "http://127.0.0.1:8000/";
  readonly ZipUrl = "http://127.0.0.1:8000/media/";

  constructor(private http:HttpClient) { }

  getUserList():Observable<any[]>{
    return this.http.get<any[]>(this.APIUrl + 'signupreq/');
  }

  addUser(val:any){
    return this.http.post(this.APIUrl + 'signupreq/',val);
  }

  //Once working, add functionalities here for PUT,DELETE and the such!

  UploadZip(val:any){
    return this.http.post(this.APIUrl+'SaveFile',val);
  }

}
