import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class MapService {
  baseUrl = 'http://localhost:443'
  constructor(private http: HttpClient) { }

  public getFrontend(){
    return this.http.get(`${this.baseUrl}/frontend`, {responseType: 'json'});
  }

  public endGame() {
    return this.http.get(`${this.baseUrl}/stop`, {responseType: 'json'});
  }

  public delay(ms: number){
    return new Promise( resolve => setTimeout(resolve, ms) );
  }
}
