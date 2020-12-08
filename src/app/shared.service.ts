import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { BehaviorSubject } from 'rxjs';

/*?
*The following class stores the first name and token of the user to validate logged in state
*The sites such as upload, view_results, etc. are not allowed to be visited if the token is not set
*/
@Injectable({
  providedIn: 'root'
})
export class MessengerService {
    constructor()
    {}
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

/*?
* The following class stores the filename of uploaded file
* This name is used in waiting component
*/
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

/*?
* The following class stores the result obtained from processing
* The result is essentially a zip file containing all the content that has to be downloaded/viewed
* This file is used view_current component to show the plots and prepare the interactive part of the website
*/
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

/*?
* This class is the main hub for all API calls
* All http requests to the backend are placed from this class
*/
@Injectable({
  providedIn: 'root'
})
export class SharedService {
  /*?
  * The backend url
  */
  readonly APIUrl = "http://127.0.0.1:8000/";
  readonly ZipUrl = "http://127.0.0.1:8000/media/";
  
  constructor(private http:HttpClient, private token: MessengerService) { }

  getUserList():Observable<any[]>{
    return this.http.get<any[]>(this.APIUrl + 'signupreq/');
  }
  /*?
  * API call for registration
  * Invokes UserAPI in backend
  */
  addUser(val:any){
    return this.http.post(this.APIUrl + 'signupreq/',val);
  }
  /*?
  * API call for login
  * Invokes LoginAPI in backend
  * Returns a token which is stored in MessengerService
  */
  login(val: any):Observable<any>{
    return this.http.post(this.APIUrl + 'api/login/', val);
  }
  /*?
  * API call for changing password
  * Invokes changeAPI in backend
  */
  changepw(val: any):Observable<any>{
    const headers_object =  new HttpHeaders().set("Authorization", "token " + this.token.getMessage()); 
    const httpOptions = {
          headers: headers_object
        };
    return this.http.post(this.APIUrl + 'api/password/', val, httpOptions);
  }
  /*?
  * API call for logout
  * Invokes LogoutAPI in backend
  */
  logout():Observable<any>{
    const headers_object =  new HttpHeaders().set("Authorization", "token " + this.token.getMessage()); 
    const httpOptions = {
          headers: headers_object
        };
    return this.http.post(this.APIUrl + 'api/logout/',"", httpOptions);
  }
  /*?
  * API call for uploading zip files
  * Invokes FileAPI in backend
  */
  UploadZip(val:any){
    const headers_object =  new HttpHeaders().set("Authorization", "token " + this.token.getMessage()); 
    const httpOptions = {
          headers: headers_object
        };
    return this.http.post(this.APIUrl+'api/files/', val, httpOptions);
  }
  /*?
  * API call for processing the input and returning the results
  * Invokes ProcessAPI in backend
  */
  processFile(filename:any){
    const httpOptions1 = {
    headers: new HttpHeaders({
        'Authorization': "token " + this.token.getMessage(),
        'Content-Type':  'application/json',
        'Accept': 'application/json',
    }),
    responseType: 'blob',
    requestType: 'application/octet-stream'
    };

    return this.http.post(this.APIUrl+'api/process/', filename, httpOptions1 as any);
  }

}