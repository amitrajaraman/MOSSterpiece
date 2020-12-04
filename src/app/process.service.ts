import { Injectable } from '@angular/core';
import { HttpClient, HttpEvent, HttpErrorResponse, HttpEventType } from  '@angular/common/http';  

@Injectable({
  providedIn: 'root'
})
export class ProcessService {

  constructor(private httpClient: HttpClient) { }

  public process(formData){
    return this.httpClient.get<any>(formData, {  
      reportProgress: true,  
      observe: 'events'  
    });  
  }
}
