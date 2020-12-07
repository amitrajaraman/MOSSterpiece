import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MessengerService {
    constructor()
    {

    }
    private messageSource: BehaviorSubject<string> = new BehaviorSubject(''); 
    public message = this.messageSource.asObservable();
    private userSource: BehaviorSubject<string> = new BehaviorSubject(''); 
    public userMessage = this.userSource.asObservable();

    public setName(value: string){
      sessionStorage.setItem('name',value);
    }

    public getName(): string{
      // console.log(sessionStorage.getItem("token"));
      if (sessionStorage.getItem("name") === null) return "";
      return sessionStorage.getItem('name');
    }

    public setMessage(value: string) {
        sessionStorage.setItem('token', value);
      }
    public getMessage(): string{
      // console.log(sessionStorage.getItem("token"));
      if (sessionStorage.getItem("token") === null) return "";
      return sessionStorage.getItem('token');
    }
}

@Injectable({
  providedIn: 'root'
})
export class FileService {
  constructor(){}
    private fileSource: BehaviorSubject<string> = new BehaviorSubject('');     
    public file = this.fileSource.asObservable();

    public setMessage(value: string) {
        this.fileSource.next(value);
      }
    public getMessage(): string{
      return this.fileSource.value;
    }
}

@Injectable({
  providedIn: 'root'
})
export class ResultService {
  constructor(){}
    private fileSource: BehaviorSubject<Blob> = new BehaviorSubject(new Blob());     
    public file = this.fileSource.asObservable();

    public setMessage(value: Blob) {
        this.fileSource.next(value);
      }
    public getMessage(): Blob{
      return this.fileSource.value;
    }
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
    const headers_object =  new HttpHeaders().set("Authorization", "token " + this.token.getMessage()); 
    const httpOptions = {
          headers: headers_object
        };
    return this.http.post(this.APIUrl + 'api/password/', val, httpOptions);
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
    return this.http.post(this.APIUrl+'api/files/', val, httpOptions);
  }

  viewFile(path:string): Observable<any>{
    const headers_object =  new HttpHeaders().set("Authorization", "token " + this.token.getMessage()); 
    const httpOptions = {
          headers: headers_object
        };
    const x = this.http.get(this.APIUrl+'api/file/?path=' + path, httpOptions);
    return x;
  }

  downloadFile(path:string): Observable<any>{
    const headers_object =  new HttpHeaders().set("Authorization", "token " + this.token.getMessage()); 
    const httpOptions = {
          headers: headers_object,
          
        };
    console.log(path);
    const x= this.http.post(
      this.APIUrl+'api/file/?path=' + path, 
    { headers_object, responseType: 'blob'});
    return x;
  }

  processFile(filename:any){
    const headers_object =  new HttpHeaders().set("Authorization", "token " + this.token.getMessage()); 
    const httpOptions = {
          headers: headers_object
        };
    return this.http.post(this.APIUrl+'api/process/', filename, httpOptions);
  }

}