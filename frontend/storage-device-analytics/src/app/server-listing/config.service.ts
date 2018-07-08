import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/do';

@Injectable()
export class ConfigService {
  
  configUrl = '/api/devices/';
  
  constructor(private http: HttpClient) { }
  
  

  getConfig(): Observable<any> {
    return this.http.get(this.configUrl);
  }
}
