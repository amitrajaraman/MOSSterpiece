import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Contact } from './contact';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class GetpostService {

  private dataURL = 'https://cs251-outlab-6.herokuapp.com/initial_values/';
  private postURL = 'https://cs251-outlab-6.herokuapp.com/add_new_feedback/';
  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  constructor(private http: HttpClient) { }

  getData(): Observable<Contact> {
    return this.http.get<Contact>(this.dataURL);
  }

  postData(data: Contact): Observable<Contact> {
    return this.http.post<Contact>(this.postURL, data, this.httpOptions)
  }
}
