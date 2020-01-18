import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
@Injectable({
  providedIn: 'root'
})
export class MainService {
  baseUrl = 'http://localhost:443'

  constructor(private http: HttpClient) { }

  public startGame(){
    return this.http.get(`${this.baseUrl}/start`, {responseType: 'text'});
  }
}
