import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
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
    public getMessage(): string{ return this.messageSource.value}
}


@Injectable({
  providedIn: 'root'
})
export class SharedService {
  readonly APIUrl = "http://127.0.0.1:8000/";
  readonly ZipUrl = "http://127.0.0.1:8000/media/";
  
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

  changepw(val: any):Observable<any>{
    return this.http.put(this.APIUrl + 'api/login/', val);
  }


  logout():Observable<any>{
    const headers_object =  new HttpHeaders().set("Authorization", "token " + this.token.getMessage()); 
    const httpOptions = {
          headers: headers_object
        };
    return this.http.post(this.APIUrl + 'api/logout/',"", httpOptions);
  }
  //Once working, add functionalities here for PUT,DELETE and the such!

  UploadZip(val:any){
    const headers_object =  new HttpHeaders().set("Authorization", "token " + this.token.getMessage()); 
    const httpOptions = {
          headers: headers_object
        };
    return this.http.post(this.APIUrl+'api/files/',val, httpOptions);
  }

  downloadFile(path:string): any{
    const headers_object =  new HttpHeaders().set("Authorization", "token " + this.token.getMessage()); 
    const httpOptions = {
          headers: headers_object
        };
    const x= this.http.get(this.APIUrl+'api/files/?path=' + path, httpOptions);
    // console.log(x);
    return x;
  }

  processFile(filename:any):any{
    const headers_object =  new HttpHeaders().set("Authorization", "token " + this.token.getMessage()); 
    const httpOptions = {
          headers: headers_object
        };
    const data = this.http.post(this.APIUrl+'api/process/',filename,httpOptions);
    return data;
  }

}