import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MessengerService {
    constructor(){}
    private messageSource: BehaviorSubject<string> = new BehaviorSubject(''); 
    public message = this.messageSource.asObservable();

    public setMessage(value: string) {
        this.messageSource.next(value);
    }
}


@Injectable({
  providedIn: 'root'
})
export class SharedService {
  readonly APIUrl = "http://127.0.0.1:8000/";
  readonly ZipUrl = "http://127.0.0.1:8000/media/";
  httpOptions = {
    headers: new HttpHeaders({ 'Authorization': `Token ${btoa(AuthService.getToken())}` })
  };
  constructor(private http:HttpClient, private token: MessengerService) { }

  getUserList():Observable<any[]>{
    return this.http.get<any[]>(this.APIUrl + 'signupreq/');
  }

  addUser(val:any){
    return this.http.post(this.APIUrl + 'signupreq/',val);
  }

  login(val: any):Observable<any>{
    return this.http.post(this.APIUrl + 'api/login/', val);
  }

  logout(val: any):Observable<any>{

    return this.http.post(this.APIUrl + 'api/logout/', val);
  }
  //Once working, add functionalities here for PUT,DELETE and the such!

  UploadZip(val:any){
    return this.http.post(this.APIUrl+'SaveFile',val);
  }



}